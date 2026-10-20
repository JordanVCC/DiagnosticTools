import datetime as dt
import concurrent.futures
import inspect
from collections import deque
import gzip
import io
import os
import queue
import re
import socket
import shutil
import tarfile
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from http.cookiejar import Cookie, CookieJar
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Optional compression format support
try:
    import zstandard
    HAS_ZSTANDARD = True
except ImportError:
    HAS_ZSTANDARD = False

try:
    import bz2
    HAS_BZ2 = True
except ImportError:
    HAS_BZ2 = False

try:
    import lzma
    HAS_LZMA = True
except ImportError:
    HAS_LZMA = False

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

try:
    from azure.identity import DefaultAzureCredential
    import fsspec
    import importlib.util
    HAS_AZURE = importlib.util.find_spec("adlfs") is not None
    if not HAS_AZURE:
        raise ImportError("adlfs not installed")
except ImportError:
    HAS_AZURE = False


BASE_URL = "https://drive.nuc.volvocars.net/data_nuc/"
HTTP_OPENER = None

# Network and performance tuning (HTTP mode).
DOWNLOAD_TIMEOUT_BASE_SECONDS = 30
DOWNLOAD_TIMEOUT_MAX_SECONDS = 300
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
IO_CHUNK_SIZE = 128 * 1024  # For file operations (extraction, combining)
PARALLEL_DOWNLOADS = 4
PARALLEL_SIZE_ESTIMATION = 4
DOWNLOAD_RESTART_AFTER_TIMEOUT_ATTEMPTS = 6

# Azure Blob Storage settings (used when az login has been run).
# Direct blob access bypasses the HTTP proxy for significantly higher throughput.
AZURE_STORAGE_ACCOUNT = "sys34e8eca5"
AZURE_CONTAINER = "raw-archive-storage"
AZURE_NUC_ROOT = f"{AZURE_CONTAINER}/data_nuc/public"
PARALLEL_DOWNLOADS_AZURE = 20          # Per official NUC tooling
IO_CHUNK_SIZE_AZURE = 8 * 1024 * 1024  # 8 MB, per official NUC tooling
AZURE_DOWNLOAD_RETRY_ATTEMPTS = 6
AZURE_DOWNLOAD_RETRY_MAX_SECONDS = 60.0

ARCHIVE_EXTENSIONS = (
    ".zip", ".zst", ".gz", ".bz2", ".xz",
    ".tar", ".tgz", ".tar.gz", ".tbz2", ".tar.bz2", ".txz", ".tar.xz",
    ".rar", ".7z",
)
SINGLE_DLT_COMPRESSED_EXTENSIONS = (".zst", ".gz", ".bz2", ".xz")

TIMESTAMP_PATTERN = re.compile(r"(\d{8}T\d{6})")


class DownloadCancelledError(Exception):
    pass


class NucAuthenticationError(RuntimeError):
    pass


def open_http_response(request, timeout):
    """Open a NUC request with the in-memory browser session, rejecting sign-in redirects."""
    response = (
        HTTP_OPENER.open(request, timeout=timeout)
        if HTTP_OPENER is not None
        else urllib.request.urlopen(request, timeout=timeout)
    )
    requested_host = urllib.parse.urlsplit(request.full_url).hostname
    response_host = urllib.parse.urlsplit(response.geturl()).hostname
    if response_host != requested_host:
        response.close()
        raise NucAuthenticationError(
            f"NUC authentication required while reading {request.full_url}: "
            f"redirected to {response_host}. Browser sign-in is not shared with this tool. "
            "Click 'Sign in to NUC Drive' and sign in in the browser that opens."
        )
    return response


def create_authenticated_http_opener(browser_cookies):
    """Build an HTTP opener from NUC browser cookies without saving credentials to disk."""
    cookie_jar = CookieJar()
    host = urllib.parse.urlsplit(BASE_URL).hostname
    for browser_cookie in browser_cookies:
        domain = browser_cookie["domain"]
        cookie_host = domain.lstrip(".")
        if host != cookie_host and not host.endswith("." + cookie_host):
            continue
        expires = browser_cookie.get("expires", -1)
        cookie_jar.set_cookie(Cookie(
            version=0, name=browser_cookie["name"], value=browser_cookie["value"],
            port=None, port_specified=False, domain=domain,
            domain_specified=domain.startswith("."), domain_initial_dot=domain.startswith("."),
            path=browser_cookie.get("path", "/"), path_specified=True,
            secure=browser_cookie.get("secure", False),
            expires=int(expires) if expires > 0 else None, discard=expires <= 0,
            comment=None, comment_url=None, rest={}, rfc2109=False,
        ))
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def authenticate_nuc_drive():
    """Open bundled Chromium for NUC sign-in and return a verified in-memory HTTP opener."""
    try:
        from playwright.sync_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError, sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install sign-in support with: pip install playwright") from exc
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        try:
            context = browser.new_context()
            page = context.new_page()
            page.goto(BASE_URL)
            page.wait_for_url(BASE_URL + "**", timeout=180000)
            opener = create_authenticated_http_opener(context.cookies([BASE_URL]))
            request = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
            with opener.open(request, timeout=30) as response:
                if urllib.parse.urlsplit(response.geturl()).hostname != urllib.parse.urlsplit(BASE_URL).hostname:
                    raise NucAuthenticationError("NUC sign-in did not establish a usable session. Please try again.")
            return opener
        except PlaywrightTimeoutError as exc:
            raise NucAuthenticationError(
                "NUC Drive sign-in timed out. Retry and complete sign-in within three minutes. "
                "Leave the sign-in browser open until the tool closes it automatically."
            ) from exc
        except PlaywrightError as exc:
            if "closed" in str(exc).lower():
                raise NucAuthenticationError(
                    "The sign-in browser closed before NUC Drive sign-in was verified. "
                    "Retry and leave that window open until the tool closes it automatically. "
                    "Signing in in another browser does not sign in this tool."
                ) from exc
            raise
        finally:
            browser.close()


def create_azure_fs():
    """
    Create an Azure Data Lake filesystem using DefaultAzureCredential.
    Requires 'az login' to have been completed before calling.
    adlfs is imported lazily here to avoid its atexit cleanup handler
    running on every startup even when Azure is not used.
    """
    if not HAS_AZURE:
        raise RuntimeError(
            "Azure packages not installed. Run: pip install azure-identity adlfs"
        )
    import adlfs  # noqa: F401 — lazy import registers abfs:// with fsspec
    credential = DefaultAzureCredential()

    # adlfs cleanup awaits credential.close(); make sync close methods awaitable.
    close_method = getattr(credential, "close", None)
    if callable(close_method) and not inspect.iscoroutinefunction(close_method):
        def _sync_close_wrapper():
            return close_method()

        async def _async_close_wrapper():
            maybe_awaitable = _sync_close_wrapper()
            if inspect.isawaitable(maybe_awaitable):
                await maybe_awaitable

        credential.close = _async_close_wrapper

    return fsspec.filesystem("abfs", account_name=AZURE_STORAGE_ACCOUNT, credential=credential)


def azure_list_names(fs, path: str) -> list[str]:
    """List immediate child names in an Azure path. Returns [] if path doesn't exist."""
    try:
        entries = fs.ls(path, detail=False)
        names = [e.rstrip("/").rsplit("/", 1)[-1] for e in entries]
        return [n for n in names if n]
    except FileNotFoundError:
        return []
    except Exception as exc:
        raise RuntimeError(f"Azure list failed for '{path}': {exc}") from exc


def azure_list_files(fs, path: str) -> list[tuple[str, int | None]]:
    """
    List files (not subdirectories) with their sizes in an Azure path.
    Returns list of (filename, size_bytes). Returns [] if path doesn't exist.
    """
    try:
        entries = fs.ls(path, detail=True)
        return [
            (e["name"].rstrip("/").rsplit("/", 1)[-1], e.get("size"))
            for e in entries
            if e.get("type", "").lower() not in ("directory", "dir")
        ]
    except FileNotFoundError:
        return []
    except Exception as exc:
        raise RuntimeError(f"Azure file list failed for '{path}': {exc}") from exc


def azure_find_child_name(fs, parent_path: str, target_name: str) -> str | None:
    """Resolve a child directory/file name under parent_path using case-insensitive matching."""
    if not target_name or not target_name.strip():
        return None
    target = target_name.strip().casefold()
    for name in azure_list_names(fs, parent_path):
        if name.casefold() == target:
            return name
    return None


def azure_find_dlt_dir_name(fs, vin_root_path: str) -> str | None:
    """Resolve the DLT directory name under a VIN path (exact match first, then contains)."""
    names = azure_list_names(fs, vin_root_path)
    exact = [name for name in names if name.casefold() == "dlt"]
    if exact:
        return exact[0]
    contains = [name for name in names if "dlt" in name.casefold()]
    if contains:
        return contains[0]
    return None


def format_bytes(num_bytes: int) -> str:
    """Convert bytes to human-readable format (B, KB, MB, GB, TB, PB)."""
    if not isinstance(num_bytes, int):
        raise TypeError(f"Expected int, got {type(num_bytes).__name__}")
    if num_bytes < 0:
        raise ValueError(f"Expected non-negative value, got {num_bytes}")
    if num_bytes < 1024:
        return f"{num_bytes} B"
    units = ["KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        value /= 1024.0
        if value < 1024.0:
            return f"{value:.1f} {unit}"
    return f"{value:.1f} PB"


class LinkParser(HTMLParser):
    """HTML parser for extracting <a> href links from directory listings."""
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        href = None
        for key, value in attrs:
            if key.lower() == "href":
                href = value
                break
        if href:
            self.links.append(href)


def fetch_links(url: str) -> list[tuple[str, str, bool]]:
    """Fetch directory links from URL. Returns list of (name, absolute_url, is_directory)."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError(f"Invalid URL: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with open_http_response(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} while reading {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while reading {url}: {exc.reason}") from exc

    parser = LinkParser()
    parser.feed(html)

    results = []
    for href in parser.links:
        if href.startswith("?"):
            continue
        absolute = urllib.parse.urljoin(url, href)
        name = href.strip("/").split("/")[-1]
        if name in {"", ".", ".."}:
            continue
        is_dir = href.endswith("/")
        results.append((name, absolute, is_dir))

    dedup = {}
    for item in results:
        dedup[(item[0].lower(), item[1], item[2])] = item
    return list(dedup.values())


def find_child_dir(parent_url: str, target_name: str) -> str | None:
    """Find a directory by name under parent URL (case-insensitive)."""
    if not target_name or not target_name.strip():
        return None
    target = target_name.lower()
    for name, url, is_dir in fetch_links(parent_url):
        if is_dir and name.lower() == target:
            return url
    return None


def find_child_dir_numeric(parent_url: str, value: int) -> str | None:
    """Find directory by numeric value (matches '1', '01', '001', etc.)."""
    if value < 0:
        return None
    target = str(value)
    target2 = f"{value:02d}"

    for name, url, is_dir in fetch_links(parent_url):
        if not is_dir:
            continue
        normalized = name.strip().lstrip("0") or "0"
        if name == target or name == target2 or normalized == target:
            return url
    return None


def find_dlt_dir(vin_url: str) -> str | None:
    """Find DLT directory: exact match 'dlt' first, then any directory containing 'dlt'."""
    links = fetch_links(vin_url)
    exact = [url for name, url, is_dir in links if is_dir and name.lower() == "dlt"]
    if exact:
        return exact[0]

    contains = [url for name, url, is_dir in links if is_dir and "dlt" in name.lower()]
    if contains:
        return contains[0]

    return None


def parse_filename_timestamp(file_name: str) -> dt.datetime | None:
    """Extract and parse timestamp from filename (YYYYMMDDTHHMMSS format)."""
    if not file_name or not isinstance(file_name, str):
        return None
    match = TIMESTAMP_PATTERN.search(file_name)
    if not match:
        return None
    try:
        return dt.datetime.strptime(match.group(1), "%Y%m%dT%H%M%S")
    except (ValueError, IndexError):
        return None


def is_archive_candidate_name(file_name: str) -> bool:
    """Check if a filename likely represents an archive/compressed payload."""
    if not file_name:
        return False
    low = file_name.lower()
    return any(low.endswith(ext) for ext in ARCHIVE_EXTENSIONS)


def is_supported_dlt_payload_name(file_name: str) -> bool:
    """Check if filename is either a raw .dlt or an archive that may contain DLT files."""
    if not file_name:
        return False
    low = file_name.lower()
    return low.endswith(".dlt") or is_archive_candidate_name(low)


def daterange(start_date: dt.date, end_date: dt.date):
    """Iterate through dates from start_date to end_date (inclusive)."""
    if not isinstance(start_date, dt.date) or not isinstance(end_date, dt.date):
        raise TypeError("start_date and end_date must be datetime.date objects")
    if end_date < start_date:
        raise ValueError(f"end_date {end_date} must be >= start_date {start_date}")
    cur = start_date
    one_day = dt.timedelta(days=1)
    while cur <= end_date:
        yield cur
        cur += one_day


def is_timeout_error(exc: Exception) -> bool:
    """Check if exception represents a timeout error."""
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, socket.timeout):
        return True
    if isinstance(exc, urllib.error.URLError):
        reason = str(getattr(exc, "reason", exc)).lower()
        return "timed out" in reason or "timeout" in reason
    return False


def is_transient_network_error(exc: Exception) -> bool:
    """Detect network failures that are usually recoverable via retry."""
    if is_timeout_error(exc):
        return True

    if isinstance(exc, urllib.error.HTTPError):
        # Retry common temporary server-side failures.
        return exc.code in {408, 429, 500, 502, 503, 504}

    text = str(exc).lower()
    # Azure/aiohttp timeouts are often wrapped in generic Exceptions with timeout wording.
    if "timeout" in text or "timed out" in text:
        return True

    transient_markers = (
        "connection reset",
        "connection aborted",
        "connection refused",
        "remote end closed connection",
        "temporarily unavailable",
        "temporary failure",
        "network is unreachable",
        "name or service not known",
        "timeout on reading data from socket",
        "server timeout",
        "read timeout",
    )
    return any(marker in text for marker in transient_markers)


def get_compression_format(file_path: Path) -> str | None:
    """Detect compression format by magic bytes, with extension fallback. Returns format string or None."""
    if not file_path.exists():
        return None
    
    file_name_lower = file_path.name.lower()
    
    try:
        with file_path.open("rb") as f:
            magic = f.read(8)
        
        # Check magic bytes
        if magic.startswith(b"PK"):  # ZIP
            return "zip"
        elif magic.startswith(b"\x1f\x8b"):  # GZIP
            return "gz"
        elif magic.startswith(b"BZ"):  # BZIP2
            return "bz2"
        elif magic.startswith(b"\xfd7zXZ\x00"):  # XZ/LZMA
            return "xz"
        elif magic.startswith(b"\x28\xb5\x2f\xfd"):  # ZSTANDARD
            return "zst"
        elif magic.startswith(b"Rar!\x1a\x07"):  # RAR 5.0+
            return "rar"
        elif magic.startswith(b"Rar!\x1a\x07\x00"):  # RAR 4.0
            return "rar"
        elif magic.startswith(b"7z\xbc\xaf\x27\x1c"):  # 7Z
            return "7z"
    except Exception:
        pass
    
    # Fallback to extension-based detection
    if file_name_lower.endswith(".zip"):
        return "zip"
    elif file_name_lower.endswith(".tar.gz") or file_name_lower.endswith(".tgz"):
        return "tar.gz"
    elif file_name_lower.endswith(".tar.bz2") or file_name_lower.endswith(".tbz2"):
        return "tar.bz2"
    elif file_name_lower.endswith(".tar.xz") or file_name_lower.endswith(".txz"):
        return "tar.xz"
    elif file_name_lower.endswith(".tar"):
        return "tar"
    elif file_name_lower.endswith(".gz"):
        return "gz"
    elif file_name_lower.endswith(".bz2"):
        return "bz2"
    elif file_name_lower.endswith(".xz"):
        return "xz"
    elif file_name_lower.endswith(".zst"):
        return "zst"
    elif file_name_lower.endswith(".rar"):
        return "rar"
    elif file_name_lower.endswith(".7z"):
        return "7z"
    
    return None


def is_archive_file(file_path: Path) -> bool:
    """Check if file is any supported archive/compression format."""
    return get_compression_format(file_path) is not None


def is_valid_dlt_file(path: Path) -> bool:
    """Check that path is a real, non-empty regular file (rejects stray directories/empty placeholders)."""
    return path.is_file() and path.stat().st_size > 0


def remove_stray_path(path: Path) -> None:
    """Remove a directory or file left at a location where a DLT file was expected."""
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)


def get_single_file_dlt_counterpart_path(file_name: str, output_dir: Path) -> Path | None:
    """Get expected .dlt path for single-file compressed DLT payloads (e.g., file.dlt.zst -> file.dlt)."""
    if not file_name or not isinstance(file_name, str):
        return None
    low = file_name.lower()
    for ext in SINGLE_DLT_COMPRESSED_EXTENSIONS:
        marker = ".dlt" + ext
        if low.endswith(marker):
            return output_dir / file_name[: -len(ext)]
    return None


def get_remote_file_size(url: str, retries: int = 2) -> int | None:
    """Fetch Content-Length header from remote file. Returns size in bytes or None if unknown."""
    if not url or not isinstance(url, str):
        return None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        try:
            with open_http_response(req, timeout=45) as response:
                header_value = response.headers.get("Content-Length")
                if not header_value:
                    return None
                return int(header_value)
        except NucAuthenticationError:
            raise
        except Exception as exc:
            if attempt >= retries:
                return None
            if is_timeout_error(exc):
                time.sleep(0.6 * attempt)
            else:
                return None
    return None


def ensure_unique_path(path: Path) -> Path:
    """Return original path if it doesn't exist, otherwise return path_N suffix."""
    if not path.exists():
        return path
    if not isinstance(path, Path):
        raise TypeError(f"Expected Path, got {type(path).__name__}")
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
        if counter > 10000:  # Safety check to avoid infinite loops
            raise RuntimeError(f"Could not find unique path variant for {path} (tried up to {counter} variants)")


def get_local_file_size(path: Path) -> int:
    """Get size of local file in bytes. Returns 0 if file doesn't exist or error occurs."""
    try:
        return path.stat().st_size
    except (OSError, ValueError):
        return 0


def download_file(
    url: str,
    destination: Path,
    on_chunk=None,
    retries: int | None = None,
    resume_offset: int = 0,
    cancel_event: threading.Event | None = None,
    on_timeout_retry=None,
):
    destination.parent.mkdir(parents=True, exist_ok=True)
    current_offset = max(0, resume_offset)
    timeout_attempts_without_completion = 0

    attempt = 0
    while True:
        attempt += 1
        if cancel_event and cancel_event.is_set():
            raise DownloadCancelledError("Download canceled by user.")

        request_timeout = min(
            DOWNLOAD_TIMEOUT_MAX_SECONDS,
            DOWNLOAD_TIMEOUT_BASE_SECONDS + (attempt - 1) * 10,
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
        }
        if current_offset > 0:
            headers["Range"] = f"bytes={current_offset}-"
        req = urllib.request.Request(url, headers=headers)

        try:
            with open_http_response(req, timeout=request_timeout) as response:
                status_code = response.getcode()

                # If server ignores Range and returns full content, restart from zero.
                if current_offset > 0 and status_code == 200:
                    current_offset = 0

                open_mode = "ab" if current_offset > 0 else "wb"
                with destination.open(open_mode) as handle:
                    if open_mode == "ab":
                        handle.seek(0, os.SEEK_END)

                    while True:
                        if cancel_event and cancel_event.is_set():
                            raise DownloadCancelledError("Download canceled by user.")
                        chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                        if not chunk:
                            break
                        handle.write(chunk)
                        if on_chunk is not None:
                            on_chunk(len(chunk))
                    # Ensure file is flushed to disk
                    handle.flush()
                    os.fsync(handle.fileno())
            timeout_attempts_without_completion = 0
            return
        except DownloadCancelledError:
            raise
        except urllib.error.HTTPError as exc:
            if exc.code == 416 and current_offset > 0:
                # Requested range not satisfiable often means file is already complete.
                return

            should_retry = is_transient_network_error(exc) and (retries is None or attempt < retries)
            if not should_retry:
                raise

            if is_timeout_error(exc):
                timeout_attempts_without_completion += 1

            current_offset = get_local_file_size(destination)
            # Exponential backoff with jitter to avoid thundering herd across parallel workers.
            wait_s = min(60.0, (2.0 ** min(attempt, 6)) + (time.monotonic() % 2.0))

            if (
                timeout_attempts_without_completion >= DOWNLOAD_RESTART_AFTER_TIMEOUT_ATTEMPTS
                and current_offset > 0
            ):
                if on_timeout_retry is not None:
                    on_timeout_retry(
                        f"Repeated timeouts — restarting from byte 0 (was at {format_bytes(current_offset)}). "
                        f"Retrying in {wait_s:.1f}s..."
                    )
                current_offset = 0
                timeout_attempts_without_completion = 0
            elif on_timeout_retry is not None:
                on_timeout_retry(
                    f"Network error after {request_timeout}s (attempt {attempt}). Retrying in {wait_s:.1f}s..."
                )
            if cancel_event and cancel_event.wait(wait_s):
                raise DownloadCancelledError("Download canceled by user.")
        except Exception as exc:
            if cancel_event and cancel_event.is_set():
                raise DownloadCancelledError("Download canceled by user.") from exc
            should_retry = is_transient_network_error(exc) and (retries is None or attempt < retries)
            if not should_retry:
                raise

            if is_timeout_error(exc):
                timeout_attempts_without_completion += 1

            current_offset = get_local_file_size(destination)
            # Exponential backoff with jitter to avoid thundering herd across parallel workers.
            wait_s = min(60.0, (2.0 ** min(attempt, 6)) + (time.monotonic() % 2.0))

            if (
                timeout_attempts_without_completion >= DOWNLOAD_RESTART_AFTER_TIMEOUT_ATTEMPTS
                and current_offset > 0
            ):
                if on_timeout_retry is not None:
                    on_timeout_retry(
                        f"Repeated timeouts — restarting from byte 0 (was at {format_bytes(current_offset)}). "
                        f"Retrying in {wait_s:.1f}s..."
                    )
                current_offset = 0
                timeout_attempts_without_completion = 0
            elif on_timeout_retry is not None:
                on_timeout_retry(
                    f"Network error after {request_timeout}s (attempt {attempt}). Retrying in {wait_s:.1f}s..."
                )
            if cancel_event and cancel_event.wait(wait_s):
                raise DownloadCancelledError("Download canceled by user.")


def extract_dlt_files_from_archive(archive_path: Path, output_dir: Path, skip_existing: bool):
    """
    Universal archive extractor for DLT files.
    Handles: zip, gzip, bzip2, xz, zstandard, tar formats.
    Returns: (extracted_count, skipped_count, found_count, extracted_paths)
    """
    fmt = get_compression_format(archive_path)
    
    if fmt == "zip":
        return _extract_zip(archive_path, output_dir, skip_existing)
    elif fmt in ("gz", "bz2", "xz", "zst"):
        return _extract_compressed_single(archive_path, output_dir, skip_existing, fmt)
    elif fmt in ("tar", "tar.gz", "tar.bz2", "tar.xz"):
        return _extract_tar(archive_path, output_dir, skip_existing)
    else:
        raise ValueError(f"Unsupported archive format: {fmt} ({archive_path.name})")


def _extract_zip(zip_path: Path, output_dir: Path, skip_existing: bool) -> tuple[int, int, int, list[Path]]:
    """Extract DLT files from ZIP archive. Returns (extracted_count, skipped_count, found_count, paths)."""
    extracted_count = 0
    skipped_count = 0
    found_dlt_count = 0
    extracted_paths = []

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"File is not a valid ZIP archive: {zip_path}")
    
    with zipfile.ZipFile(zip_path, "r") as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            member_name = member.filename
            if not member_name.lower().endswith(".dlt"):
                continue
            
            found_dlt_count += 1
            target_name = Path(member_name).name
            if not target_name:
                continue
            
            target_path = output_dir / target_name
            if target_path.exists() and not is_valid_dlt_file(target_path):
                remove_stray_path(target_path)
            if skip_existing and target_path.exists():
                skipped_count += 1
                extracted_paths.append(target_path)
                continue
            if not skip_existing and target_path.exists():
                target_path = ensure_unique_path(target_path)
            
            output_dir.mkdir(parents=True, exist_ok=True)
            with archive.open(member, "r") as source, target_path.open("wb") as target:
                shutil.copyfileobj(source, target, length=IO_CHUNK_SIZE)
            extracted_count += 1
            extracted_paths.append(target_path)
    
    return extracted_count, skipped_count, found_dlt_count, extracted_paths


def _extract_compressed_single(archive_path: Path, output_dir: Path, skip_existing: bool, fmt: str) -> tuple[int, int, int, list[Path]]:
    """
    Extract single-file compressed format (gzip, bzip2, xz, zstandard).
    Returns (extracted_count, skipped_count, found_count, paths).
    """
    extracted_count = 0
    skipped_count = 0
    found_dlt_count = 0
    extracted_paths = []
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine output filename
    stem = archive_path.stem
    if stem.endswith(".tar"):
        # tar.gz, tar.bz2, etc. - extract as tar
        return _extract_tar_from_stream(archive_path, output_dir, skip_existing, fmt)
    else:
        # Single file - likely a DLT file with compression
        output_name = stem if stem else archive_path.name.rsplit(".", 1)[0]
        if not output_name.lower().endswith(".dlt"):
            output_name += ".dlt"
        
        output_path = output_dir / output_name
        if output_path.exists() and not is_valid_dlt_file(output_path):
            remove_stray_path(output_path)
        if skip_existing and output_path.exists():
            return 0, 1, 1, [output_path]
        if not skip_existing and output_path.exists():
            output_path = ensure_unique_path(output_path)
        
        try:
            _decompress_file(archive_path, output_path, fmt)
            return 1, 0, 1, [output_path]
        except Exception as e:
            # If decompression fails, try to use the file as-is
            try:
                if archive_path.stat().st_size > 0:
                    # Copy the file as-is and assume it's the DLT content
                    with archive_path.open("rb") as src, output_path.open("wb") as dst:
                        shutil.copyfileobj(src, dst, length=IO_CHUNK_SIZE)
                    return 1, 0, 1, [output_path]
            except Exception as fallback_exc:
                raise ValueError(
                    f"Failed to decompress {archive_path.name}: {e}. "
                    f"Also failed to use as raw file: {fallback_exc}"
                ) from e


def _extract_tar(tar_path: Path, output_dir: Path, skip_existing: bool) -> tuple[int, int, int, list[Path]]:
    """Extract DLT files from TAR archive (including tar.gz, tar.bz2, tar.xz). Returns (extracted, skipped, found, paths)."""
    extracted_count = 0
    skipped_count = 0
    found_dlt_count = 0
    extracted_paths = []
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine tar mode
    if tar_path.name.endswith(".tar.gz") or tar_path.name.endswith(".tgz"):
        mode = "r:gz"
    elif tar_path.name.endswith(".tar.bz2") or tar_path.name.endswith(".tbz2"):
        mode = "r:bz2"
    elif tar_path.name.endswith(".tar.xz") or tar_path.name.endswith(".txz"):
        mode = "r:xz"
    else:
        mode = "r"
    
    try:
        with tarfile.open(tar_path, mode) as archive:
            for member in archive.getmembers():
                if member.isdir():
                    continue
                if not member.name.lower().endswith(".dlt"):
                    continue
                
                found_dlt_count += 1
                target_name = Path(member.name).name
                if not target_name:
                    continue
                
                target_path = output_dir / target_name
                if target_path.exists() and not is_valid_dlt_file(target_path):
                    remove_stray_path(target_path)
                if skip_existing and target_path.exists():
                    skipped_count += 1
                    extracted_paths.append(target_path)
                    continue
                if not skip_existing and target_path.exists():
                    target_path = ensure_unique_path(target_path)
                
                # Extract file
                f = archive.extractfile(member)
                if f:
                    try:
                        with f, target_path.open("wb") as out:
                            shutil.copyfileobj(f, out, length=IO_CHUNK_SIZE)
                        extracted_count += 1
                        extracted_paths.append(target_path)
                    finally:
                        f.close()
    except Exception as e:
        raise ValueError(f"Failed to extract tar archive {tar_path.name}: {e}") from e
    
    return extracted_count, skipped_count, found_dlt_count, extracted_paths


def _extract_tar_from_stream(archive_path: Path, output_dir: Path, skip_existing: bool, fmt: str) -> tuple[int, int, int, list[Path]]:
    """Extract DLT files from tar archive compressed with gzip/bzip2/xz. Returns (extracted, skipped, found, paths)."""
    extracted_count = 0
    skipped_count = 0
    found_dlt_count = 0
    extracted_paths = []
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Decompress to stream
        decompressed_data = _decompress_to_bytes(archive_path, fmt)
        
        # Open as tar from stream
        with tarfile.open(fileobj=io.BytesIO(decompressed_data)) as archive:
            for member in archive.getmembers():
                if member.isdir():
                    continue
                if not member.name.lower().endswith(".dlt"):
                    continue
                
                found_dlt_count += 1
                target_name = Path(member.name).name
                if not target_name:
                    continue
                
                target_path = output_dir / target_name
                if target_path.exists() and not is_valid_dlt_file(target_path):
                    remove_stray_path(target_path)
                if skip_existing and target_path.exists():
                    skipped_count += 1
                    extracted_paths.append(target_path)
                    continue
                if not skip_existing and target_path.exists():
                    target_path = ensure_unique_path(target_path)
                
                f = archive.extractfile(member)
                if f:
                    try:
                        with f, target_path.open("wb") as out:
                            shutil.copyfileobj(f, out, length=IO_CHUNK_SIZE)
                        extracted_count += 1
                        extracted_paths.append(target_path)
                    except Exception as e:
                        raise ValueError(f"Failed to extract member {member.name}: {e}") from e
    except Exception as e:
        raise ValueError(f"Failed to extract tar from {archive_path.name}: {e}") from e
    
    return extracted_count, skipped_count, found_dlt_count, extracted_paths


def _decompress_file(compressed_path: Path, output_path: Path, fmt: str) -> None:
    """Decompress a single file using the specified format."""
    decompressed = _decompress_to_bytes(compressed_path, fmt)
    with output_path.open("wb") as f:
        f.write(decompressed)


def _decompress_to_bytes(compressed_path: Path, fmt: str) -> bytes:
    """Decompress file to bytes."""
    with compressed_path.open("rb") as f:
        data = f.read()
    
    if fmt == "gz":
        return gzip.decompress(data)
    elif fmt == "bz2" and HAS_BZ2:
        return bz2.decompress(data)
    elif fmt == "xz" and HAS_LZMA:
        return lzma.decompress(data)
    elif fmt == "zst" and HAS_ZSTANDARD:
        try:
            # Try standard decompression first
            dctx = zstandard.ZstdDecompressor()
            return dctx.decompress(data)
        except Exception as e1:
            # Try with max_output_size for larger files
            try:
                dctx = zstandard.ZstdDecompressor()
                return dctx.decompress(data, max_output_size=1024*1024*1024)  # 1GB max
            except Exception as e2:
                # Try streaming decompression
                try:
                    dctx = zstandard.ZstdDecompressor()
                    reader = dctx.stream_reader(io.BytesIO(data), closefd=False)
                    return reader.read()
                except Exception as e3:
                    raise ValueError(f"Failed to decompress zstd file with multiple methods: {e1}, {e2}, {e3}")
    else:
        raise ValueError(f"Unsupported or unavailable format: {fmt}")


def combine_dlt_files(source_paths: list[Path], combined_output_path: Path) -> None:
    """Combine multiple DLT files into a single DLT file. Preserves order of source_paths."""
    if not source_paths:
        raise ValueError("No source files to combine")
    if not isinstance(combined_output_path, Path):
        raise TypeError(f"combined_output_path must be Path, got {type(combined_output_path).__name__}")
    
    combined_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Verify all source files exist and are readable
    for src in source_paths:
        if not isinstance(src, Path):
            raise TypeError(f"Expected Path in source_paths, got {type(src).__name__}")
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        if not src.is_file():
            raise ValueError(f"Source path is not a file: {src}")
    
    try:
        with combined_output_path.open("wb") as combined:
            for src in source_paths:
                with src.open("rb") as handle:
                    shutil.copyfileobj(handle, combined, length=IO_CHUNK_SIZE)
    except Exception as e:
        # Clean up partial output on error
        try:
            combined_output_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise RuntimeError(f"Failed to combine DLT files into {combined_output_path}: {e}") from e


class DateTimeSelector(ttk.LabelFrame):
    def __init__(self, parent, title: str, default_time=None):
        super().__init__(parent, text=title)
        self.columnconfigure(0, weight=1)

        now = dt.datetime.now().replace(microsecond=0)
        if default_time is not None:
            now = now.replace(hour=default_time[0], minute=default_time[1], second=default_time[2])

        row = ttk.Frame(self)
        row.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        row.columnconfigure(4, weight=1)

        ttk.Label(row, text="Date").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.date_var = tk.StringVar(value=now.strftime("%Y-%m-%d"))
        self.date_entry = DateEntry(
            row,
            date_pattern="yyyy-mm-dd",
            textvariable=self.date_var,
            width=14,
        )
        self.date_entry.grid(row=0, column=1, sticky="w")
        ttk.Label(row, text="Format: YYYY-MM-DD").grid(row=0, column=2, sticky="w", padx=(10, 0))

        time_row = ttk.Frame(self)
        time_row.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        time_row.columnconfigure(12, weight=1)

        ttk.Label(time_row, text="Time").grid(row=0, column=0, sticky="w", padx=(0, 6))

        self.hour_var = tk.StringVar(value=f"{now.hour:02d}")
        rounded_minute = (now.minute // 5) * 5
        self.minute_var = tk.StringVar(value=f"{rounded_minute:02d}")
        self.second_var = tk.StringVar(value="00")

        self.hour_combo = ttk.Combobox(
            time_row,
            width=4,
            textvariable=self.hour_var,
            state="normal",
            values=[f"{v:02d}" for v in range(24)],
        )
        self.hour_combo.grid(row=0, column=1, sticky="w")

        ttk.Label(time_row, text=":").grid(row=0, column=2, sticky="w", padx=3)

        self.minute_combo = ttk.Combobox(
            time_row,
            width=4,
            textvariable=self.minute_var,
            state="normal",
            values=[f"{v:02d}" for v in range(0, 60, 5)],
        )
        self.minute_combo.grid(row=0, column=3, sticky="w")

        ttk.Label(time_row, text=":").grid(row=0, column=4, sticky="w", padx=3)

        self.second_combo = ttk.Combobox(
            time_row,
            width=4,
            textvariable=self.second_var,
            state="normal",
            values=[f"{v:02d}" for v in range(60)],
        )
        self.second_combo.grid(row=0, column=5, sticky="w")

        ttk.Label(time_row, text="24h (HH:MM:SS)").grid(row=0, column=6, sticky="w", padx=(10, 0))
        ttk.Button(time_row, text="Now", command=self.set_now).grid(row=0, column=7, padx=(10, 0), sticky="w")

    def set_now(self):
        now = dt.datetime.now().replace(microsecond=0)
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.hour_var.set(f"{now.hour:02d}")
        self.minute_var.set(f"{(now.minute // 5) * 5:02d}")
        self.second_var.set("00")

    def _parse_component(self, value: str, label: str, lower: int, upper: int):
        text = value.strip()
        if text == "":
            raise ValueError(f"{label} is required.")
        try:
            number = int(text)
        except ValueError as exc:
            raise ValueError(f"{label} must be a number from {lower} to {upper}.") from exc
        if number < lower or number > upper:
            raise ValueError(f"{label} must be between {lower} and {upper}.")
        return number

    def get_datetime(self):
        try:
            date_part = dt.datetime.strptime(self.date_var.get().strip(), "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("Date must use YYYY-MM-DD format.") from exc

        hour = self._parse_component(self.hour_var.get(), "Hour", 0, 23)
        minute = self._parse_component(self.minute_var.get(), "Minute", 0, 59)
        second = self._parse_component(self.second_var.get(), "Second", 0, 59)

        return dt.datetime(date_part.year, date_part.month, date_part.day, hour, minute, second)


class DownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NUC DLT Window Downloader")
        self.geometry("1000x720")
        self.minsize(900, 620)

        if DateEntry is None:
            messagebox.showerror(
                "Missing dependency",
                "The calendar date picker requires 'tkcalendar'.\n\n"
                "Install it with: py -3 -m pip install tkcalendar",
            )
            self.destroy()
            return

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.option_add("*Font", "{Segoe UI} 10")
        bg_main = "#1e1e1e"
        bg_panel = "#252526"
        border = "#3c3c3c"
        fg_main = "#d4d4d4"
        fg_muted = "#9da1a6"
        accent = "#0e639c"

        self.configure(bg=bg_main)
        style.configure("Card.TFrame", background=bg_main)
        style.configure("TFrame", background=bg_main)
        style.configure(
            "Header.TLabel",
            font="{Segoe UI} 17 bold",
            foreground=fg_main,
            background=bg_main,
        )
        style.configure(
            "SubHeader.TLabel",
            font="{Segoe UI} 10",
            foreground=fg_muted,
            background=bg_main,
        )
        style.configure("TLabel", padding=1, foreground=fg_main, background=bg_main)
        style.configure(
            "TButton",
            padding=6,
            foreground=fg_main,
            background=bg_panel,
            bordercolor=border,
            focusthickness=1,
            focuscolor=accent,
        )
        style.map(
            "TButton",
            background=[("active", "#2a2d2e"), ("pressed", "#31363b")],
            foreground=[("disabled", "#7f848e")],
        )
        style.configure(
            "Accent.TButton",
            padding=6,
            foreground="#ffffff",
            background=accent,
            bordercolor=accent,
            focusthickness=1,
            focuscolor=accent,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#1177bb"), ("pressed", "#0b4f7a")],
            foreground=[("disabled", "#c7c7c7")],
        )
        style.configure(
            "TLabelframe",
            padding=8,
            background=bg_panel,
            foreground=fg_main,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
            relief="solid",
        )
        style.configure("TLabelframe.Label", font="{Segoe UI} 10 bold", foreground=fg_main, background=bg_panel)
        style.configure(
            "TEntry",
            fieldbackground="#1f1f1f",
            foreground=fg_main,
            insertcolor=fg_main,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
        )
        style.configure(
            "TCombobox",
            fieldbackground="#1f1f1f",
            foreground=fg_main,
            background=bg_panel,
            bordercolor=border,
            arrowcolor=fg_main,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#1f1f1f")],
            foreground=[("readonly", fg_main)],
            selectbackground=[("readonly", "#1f1f1f")],
            selectforeground=[("readonly", fg_main)],
        )
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#2d2d30",
            background=accent,
            bordercolor=border,
            lightcolor=accent,
            darkcolor=accent,
        )

        self.option_add("*Text.background", "#1f1f1f")
        self.option_add("*Text.foreground", fg_main)
        self.option_add("*Text.insertBackground", fg_main)
        self.option_add("*Text.selectBackground", "#264f78")

        self.log_queue = queue.Queue()
        self.ui_queue = queue.Queue()
        self.worker_thread = None
        self.vin_loader_thread = None
        self.all_vins = []
        self.cancel_event = threading.Event()
        self.speed_state_lock = threading.Lock()
        self.azure_fs = None  # Set by _load_vins_worker if Azure auth succeeds
        self._drain_queue_after_id = None

        self._build_ui()
        self._drain_queue_after_id = self.after(150, self._drain_queues)
        self._start_vin_refresh()
        
        # Register cleanup handler on window close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _build_ui(self):
        outer = ttk.Frame(self, style="Card.TFrame")
        outer.pack(fill="both", expand=True)
        outer.rowconfigure(0, weight=1)
        outer.rowconfigure(1, weight=0)
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=0)

        self.scroll_canvas = tk.Canvas(
            outer,
            background="#1e1e1e",
            highlightthickness=0,
            borderwidth=0,
            xscrollincrement=12,
            yscrollincrement=12,
        )
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew")

        v_scroll = ttk.Scrollbar(outer, orient="vertical", command=self.scroll_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        h_scroll = ttk.Scrollbar(outer, orient="horizontal", command=self.scroll_canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.scroll_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        root = ttk.Frame(self.scroll_canvas, style="Card.TFrame", padding=16)
        self._canvas_window = self.scroll_canvas.create_window((0, 0), window=root, anchor="nw")

        def _on_root_configure(_event=None):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        def _on_canvas_configure(event):
            requested_width = root.winfo_reqwidth()
            target_width = max(requested_width, event.width - 20)
            self.scroll_canvas.itemconfigure(self._canvas_window, width=target_width)
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        def _on_mouse_wheel(event):
            widget_class = event.widget.winfo_class()
            # Let input/dropdown widgets consume wheel events themselves.
            if widget_class in {"TCombobox", "Combobox", "Listbox", "Text", "Entry", "TEntry", "Spinbox"}:
                return
            if event.state & 0x0001:
                self.scroll_canvas.xview_scroll(int(-event.delta / 120), "units")
            else:
                self.scroll_canvas.yview_scroll(int(-event.delta / 120), "units")
            return "break"

        root.bind("<Configure>", _on_root_configure)
        self.scroll_canvas.bind("<Configure>", _on_canvas_configure)
        self.bind_all("<MouseWheel>", _on_mouse_wheel)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=0)
        root.rowconfigure(4, weight=1)

        header = ttk.Frame(root, style="Card.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="NUC DLT Window Downloader", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Select VIN and a precise date-time window to download matching DLT files.",
            style="SubHeader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        top = ttk.LabelFrame(root, text="Inputs")
        top.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        top.columnconfigure(0, weight=0)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=0)
        top.columnconfigure(3, weight=0)
        top.columnconfigure(4, weight=0)

        ttk.Label(top, text="VIN").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.vin_var = tk.StringVar()
        self.vin_combo = ttk.Combobox(top, textvariable=self.vin_var)
        self.vin_combo.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self.vin_combo.bind("<KeyRelease>", self._on_vin_keyrelease)
        self.vin_combo.bind("<<ComboboxSelected>>", self._on_vin_selected)
        self.vin_status_var = tk.StringVar(value="VIN list not loaded")
        ttk.Label(top, textvariable=self.vin_status_var).grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.refresh_vins_button = ttk.Button(top, text="Refresh VINs", command=self._start_vin_refresh)
        self.refresh_vins_button.grid(row=0, column=3, padx=8, pady=8)
        self.sign_in_button = ttk.Button(top, text="Sign in to NUC Drive", command=self._start_http_sign_in)
        self.sign_in_button.grid(row=0, column=4, padx=8, pady=8)

        ttk.Label(top, text="Variant").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.variant_var = tk.StringVar(value="HPA")
        ttk.Combobox(top, textvariable=self.variant_var, values=["HPA", "HPB"], width=8, state="readonly").grid(
            row=1, column=1, padx=8, pady=8, sticky="w"
        )

        ttk.Label(top, text="Output Folder").grid(row=2, column=0, padx=8, pady=8, sticky="w")
        default_output = Path(__file__).resolve().parent / "downloads"
        self.output_var = tk.StringVar(value=str(default_output))
        ttk.Entry(top, textvariable=self.output_var).grid(row=2, column=1, columnspan=3, padx=8, pady=8, sticky="ew")
        ttk.Button(top, text="Browse", command=self._browse_output).grid(row=2, column=4, padx=8, pady=8)

        self.skip_existing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Skip existing files", variable=self.skip_existing_var).grid(
            row=3, column=0, columnspan=2, padx=8, pady=(0, 8), sticky="w"
        )
        self.combine_dlt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Combine all DLT files into one", variable=self.combine_dlt_var).grid(
            row=4, column=0, columnspan=2, padx=8, pady=(0, 8), sticky="w"
        )
        ttk.Label(top, text="Tip: You can type VIN, date, and time values manually.").grid(
            row=4, column=2, columnspan=2, padx=8, pady=(0, 8), sticky="w"
        )



        time_row = ttk.Frame(root)
        time_row.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        time_row.columnconfigure(0, weight=1)
        time_row.columnconfigure(1, weight=1)
        time_row.rowconfigure(0, weight=0)

        self.start_selector = DateTimeSelector(time_row, "Start Date/Time", default_time=(0, 0, 0))
        self.start_selector.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.end_selector = DateTimeSelector(time_row, "End Date/Time", default_time=(23, 59, 59))
        self.end_selector.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        actions = ttk.Frame(root)
        actions.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        actions.columnconfigure(0, weight=0)
        actions.columnconfigure(1, weight=0)
        actions.columnconfigure(2, weight=0)
        actions.columnconfigure(3, weight=0)
        actions.columnconfigure(4, weight=1)
        actions.columnconfigure(5, weight=0)
        actions.rowconfigure(0, weight=0)
        self.download_button = ttk.Button(actions, text="Download Logs", command=self.start_download)
        self.download_button.configure(style="Accent.TButton")
        self.download_button.grid(row=0, column=0, sticky="w")
        self.stop_button = ttk.Button(actions, text="Stop", command=self.stop_download, state="disabled")
        self.stop_button.grid(row=0, column=1, sticky="w", padx=(8, 0))
        ttk.Button(actions, text="Clear Log", command=self._clear_log).grid(row=0, column=2, sticky="w", padx=(8, 0))

        self.progress_status_var = tk.StringVar(value="Idle")
        ttk.Label(actions, textvariable=self.progress_status_var).grid(row=0, column=3, sticky="w", padx=(12, 0))

        self.progress = ttk.Progressbar(actions, mode="determinate", maximum=100, value=0, length=260)
        self.progress.grid(row=0, column=5, sticky="e")

        log_frame = ttk.LabelFrame(root, text="Operation Log")
        log_frame.grid(row=4, column=0, sticky="nsew", pady=(12, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=0)

        self.log_text = tk.Text(log_frame, wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.log_text.configure(
            background="#1f1f1f",
            foreground="#d4d4d4",
            insertbackground="#d4d4d4",
            selectbackground="#264f78",
            relief="flat",
            borderwidth=0,
        )
        self.log_text.configure(state="disabled")

    def _on_vin_selected(self, _event=None):
        self._filter_vin_values(self.vin_var.get().strip())

    def _on_vin_keyrelease(self, _event=None):
        self._filter_vin_values(self.vin_var.get().strip())

    def _filter_vin_values(self, query: str):
        if not self.all_vins:
            return

        q = query.lower()
        if not q:
            filtered = self.all_vins
        else:
            starts = [vin for vin in self.all_vins if vin.lower().startswith(q)]
            contains = [vin for vin in self.all_vins if q in vin.lower() and not vin.lower().startswith(q)]
            filtered = starts + contains

        self.vin_combo["values"] = filtered[:300]

    def _start_http_sign_in(self):
        if (self.worker_thread and self.worker_thread.is_alive()) or (
            self.vin_loader_thread and self.vin_loader_thread.is_alive()
        ):
            messagebox.showinfo("Please wait", "Wait for the current operation to finish before signing in.")
            return
        self.sign_in_button.configure(state="disabled")
        self.refresh_vins_button.configure(state="disabled")
        self.log("Sign in to NUC Drive in the Chromium window that opens (3-minute timeout). Leave it open until it closes automatically.")
        self.vin_loader_thread = threading.Thread(target=self._http_sign_in_worker, daemon=True)
        self.vin_loader_thread.start()

    def _http_sign_in_worker(self):
        global HTTP_OPENER
        try:
            HTTP_OPENER = authenticate_nuc_drive()
            self.azure_fs = None
            self.log("NUC Drive signed in. Using drive listings for current and archived logs.")
            self._load_vins_worker()
        except Exception as exc:
            self.log(f"NUC Drive sign-in failed: {exc}")
            self.ui_queue.put(("vin_error", str(exc)))
            self.ui_queue.put(("dialog", "error", "NUC Drive sign-in failed", str(exc)))
        finally:
            self.ui_queue.put(("sign_in_ready",))

    def _start_vin_refresh(self):
        if self.vin_loader_thread and self.vin_loader_thread.is_alive():
            return

        self.refresh_vins_button.configure(state="disabled")
        self.vin_status_var.set("VIN list: loading...")
        self._set_progress_mode("indeterminate")
        self.progress_status_var.set("Loading VIN list...")
        self.vin_loader_thread = threading.Thread(target=self._load_vins_worker, daemon=True)
        self.vin_loader_thread.start()

    def _load_vins_worker(self):
        """Load VIN list from NUC drive (runs in background thread)."""
        # Try Azure first — direct blob storage is faster and eliminates HTTP timeouts.
        if HAS_AZURE and HTTP_OPENER is None:
            try:
                fs = create_azure_fs()
                vins = sorted(azure_list_names(fs, AZURE_NUC_ROOT))
                if vins:
                    self.azure_fs = fs
                    self.ui_queue.put(("vin_loaded", vins))
                    self.log(
                        f"Azure Blob Storage connected ({AZURE_STORAGE_ACCOUNT}) — "
                        f"{PARALLEL_DOWNLOADS_AZURE} parallel workers, {IO_CHUNK_SIZE_AZURE // (1024*1024)} MB buffer."
                    )
                    return
            except Exception as azure_exc:
                self.log(f"Azure connection failed (run 'az login' to enable fast mode): {azure_exc}")

        # HTTP fallback
        try:
            links = fetch_links(BASE_URL)
            vins = sorted([name for name, _url, is_dir in links if is_dir])
            self.ui_queue.put(("vin_loaded", vins))
            self.log(
                f"HTTP mode ({PARALLEL_DOWNLOADS} parallel workers). "
                "Run 'az login' then refresh to enable fast Azure mode."
            )
        except Exception as exc:
            self.ui_queue.put(("vin_error", str(exc)))

    def _set_loaded_vins(self, vins):
        self.all_vins = vins
        self.vin_combo["values"] = vins[:300]
        self.vin_status_var.set(f"VIN list: {len(vins)} loaded")
        if not self.worker_thread or not self.worker_thread.is_alive():
            self.refresh_vins_button.configure(state="normal")
        self._set_progress_mode("determinate", maximum=100, value=0)
        self.progress_status_var.set("Idle")
        self.log(f"Loaded {len(vins)} VIN folders from NUC drive.")

    def _set_vin_load_error(self, err: str):
        self.vin_status_var.set("VIN list: load failed")
        if not self.worker_thread or not self.worker_thread.is_alive():
            self.refresh_vins_button.configure(state="normal")
        self._set_progress_mode("determinate", maximum=100, value=0)
        self.progress_status_var.set("VIN load failed")
        self.log(f"Failed to load VIN list: {err}")

    def _browse_output(self):
        selected = filedialog.askdirectory(initialdir=self.output_var.get() or os.getcwd())
        if selected:
            self.output_var.set(selected)

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _append_log(self, text: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def log(self, msg: str):
        timestamp = dt.datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {msg}")

    def _drain_queues(self):
        """Process queued messages from worker threads. Scheduled periodically."""
        if not self.winfo_exists():
            return
        
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self._append_log(msg)
        except queue.Empty:
            pass

        try:
            while True:
                action = self.ui_queue.get_nowait()
                self._handle_ui_action(action)
        except queue.Empty:
            pass

        if self.winfo_exists():
            try:
                self._drain_queue_after_id = self.after(150, self._drain_queues)
            except tk.TclError:
                # Window destroyed between winfo_exists check and after call
                self._drain_queue_after_id = None

    def _on_closing(self):
        """Handle window close event: cleanup threads and resources."""
        # Cancel pending queue drain
        if self._drain_queue_after_id is not None:
            self.after_cancel(self._drain_queue_after_id)
            self._drain_queue_after_id = None
        
        # Signal cancellation to worker thread
        self.cancel_event.set()
        
        # Wait for worker thread to finish (with timeout)
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        
        # Wait for VIN loader thread to finish (with timeout)
        if self.vin_loader_thread and self.vin_loader_thread.is_alive():
            self.vin_loader_thread.join(timeout=2.0)
        
        # Destroy window
        self.destroy()

    def _handle_ui_action(self, action):
        name = action[0]
        if name == "vin_loaded":
            self._set_loaded_vins(action[1])
        elif name == "vin_error":
            self._set_vin_load_error(action[1])
        elif name == "sign_in_ready":
            self.sign_in_button.configure(state="normal")
        elif name == "set_running":
            self.set_running(action[1])
        elif name == "progress_mode":
            _name, mode, maximum, value = action
            self._set_progress_mode(mode, maximum=maximum, value=value)
        elif name == "progress_value":
            _name, value, status = action
            self.progress.configure(value=value)
            if status is not None:
                self.progress_status_var.set(status)
        elif name == "dialog":
            _name, level, title, message = action
            if level == "info":
                messagebox.showinfo(title, message)
            else:
                messagebox.showerror(title, message)

    def _set_progress_mode(self, mode: str, maximum: int = 100, value: int = 0):
        if mode == "indeterminate":
            self.progress.configure(mode="indeterminate")
            self.progress.start(10)
            return

        self.progress.stop()
        self.progress.configure(mode="determinate", maximum=max(1, maximum), value=max(0, value))

    def stop_download(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.cancel_event.set()
            self.stop_button.configure(state="disabled")
            self.progress_status_var.set("Cancel requested...")
            self.log("Stop requested by user. Canceling current operation...")

    def _raise_if_cancelled(self):
        if self.cancel_event.is_set():
            raise DownloadCancelledError("Download canceled by user.")

    def set_running(self, running: bool):
        if running:
            self.download_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.refresh_vins_button.configure(state="disabled")
        else:
            self.download_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            if not self.vin_loader_thread or not self.vin_loader_thread.is_alive():
                self.refresh_vins_button.configure(state="normal")
            self._set_progress_mode("determinate", maximum=100, value=0)
            self.progress_status_var.set("Idle")

    def start_download(self):
        if self.vin_loader_thread and self.vin_loader_thread.is_alive():
            messagebox.showinfo(
                "Please wait",
                "VIN list is still loading. Please wait for it to complete or try again in a few seconds.",
            )
            return

        vin = self.vin_var.get().strip()
        if not vin:
            messagebox.showerror("Missing VIN", "Please enter a VIN number.")
            return

        try:
            start_dt = self.start_selector.get_datetime()
            end_dt = self.end_selector.get_datetime()
        except ValueError as exc:
            messagebox.showerror("Invalid date/time", f"Please fix date/time values.\n\n{exc}")
            return

        if end_dt < start_dt:
            messagebox.showerror("Invalid window", "End date/time must be equal to or after start date/time.")
            return

        variant = self.variant_var.get().strip().upper()
        if variant not in {"HPA", "HPB"}:
            messagebox.showerror("Invalid variant", "Variant must be HPA or HPB.")
            return

        output_raw = self.output_var.get().strip()
        if not output_raw:
            messagebox.showerror("Missing output folder", "Please choose an output folder.")
            return
        output_dir = Path(output_raw)

        self.cancel_event.clear()
        self.set_running(True)
        self._set_progress_mode("determinate", maximum=100, value=0)
        self.progress_status_var.set("Preparing...")
        self.log("Starting download process...")

        self.worker_thread = threading.Thread(
            target=self._run_download,
            args=(
                vin,
                variant,
                start_dt,
                end_dt,
                output_dir,
                self.skip_existing_var.get(),
                self.combine_dlt_var.get(),
            ),
            daemon=True,
        )
        self.worker_thread.start()

    def _run_download(
        self,
        vin,
        variant,
        start_dt,
        end_dt,
        output_dir: Path,
        skip_existing: bool,
        combine_dlt: bool,
    ):
        """
        Main download worker thread (runs in background).
        Orchestrates file discovery, parallel downloads, extraction, and combining.
        """
        global HTTP_OPENER
        downloaded = 0
        skipped_existing = 0
        extracted_dlt = 0
        removed_archives = 0
        dlt_files_for_combine = []

        try:
            total_days = (end_dt.date() - start_dt.date()).days + 1
            self._raise_if_cancelled()

            # Snapshot Azure FS state; determines worker count and download path for this run.
            azure_fs = self.azure_fs if HTTP_OPENER is None else None
            parallel_workers = PARALLEL_DOWNLOADS_AZURE if azure_fs is not None else PARALLEL_DOWNLOADS

            expected_total_bytes = 0
            unknown_size_count = 0
            sized_matches: list = []

            if azure_fs is not None:
                # === AZURE PATH: direct blob storage — no HTML scraping, sizes come free from ls() ===
                azure_vin = azure_find_child_name(azure_fs, AZURE_NUC_ROOT, vin)
                if not azure_vin:
                    raise RuntimeError(
                        f"VIN '{vin}' was not found in Azure container '{AZURE_STORAGE_ACCOUNT}'."
                    )

                vin_root_path = f"{AZURE_NUC_ROOT}/{azure_vin}"
                azure_dlt_dir = azure_find_dlt_dir_name(azure_fs, vin_root_path)
                if not azure_dlt_dir:
                    raise RuntimeError("Could not find a DLT folder for the selected VIN in Azure.")

                variant_root = f"{vin_root_path}/{azure_dlt_dir}"
                azure_variant = azure_find_child_name(azure_fs, variant_root, variant)
                if not azure_variant:
                    raise RuntimeError(
                        f"Could not find variant folder '{variant}' under Azure DLT path for VIN '{vin}'."
                    )

                variant_azure_path = f"{variant_root}/{azure_variant}"
                self.log(f"Azure mode | {AZURE_STORAGE_ACCOUNT}/{variant_azure_path}")
                self.log("Scanning dates and collecting matching files...")
                self.ui_queue.put(("progress_mode", "determinate", max(1, total_days), 0))

                for day_index, day in enumerate(daterange(start_dt.date(), end_dt.date()), start=1):
                    self._raise_if_cancelled()
                    self.ui_queue.put(("progress_value", day_index, f"Scanning {day_index}/{total_days} day(s)..."))
                    day_path = f"{variant_azure_path}/{day.year:04d}/{day.month:02d}/{day.day:02d}"
                    for file_name, file_size in azure_list_files(azure_fs, day_path):
                        if not is_supported_dlt_payload_name(file_name):
                            continue
                        file_ts = parse_filename_timestamp(file_name)
                        if file_ts is None:
                            continue
                        if start_dt <= file_ts <= end_dt:
                            sized_matches.append((file_name, f"{day_path}/{file_name}", day, file_size))
                            if file_size is not None:
                                expected_total_bytes += file_size
                            else:
                                unknown_size_count += 1

            else:
                # === HTTP PATH: web directory listing + parallel HEAD requests for sizes ===
                self.log(f"HTTP mode | Looking up VIN '{vin}' in {BASE_URL}")
                vin_url = find_child_dir(BASE_URL, vin)
                if not vin_url:
                    raise RuntimeError(f"VIN '{vin}' was not found in the directory listing.")

                self.log(f"VIN directory: {vin_url}")
                dlt_url = find_dlt_dir(vin_url)
                if not dlt_url:
                    raise RuntimeError("Could not find a DLT folder for the selected VIN.")

                self.log(f"DLT directory: {dlt_url}")
                variant_url = find_child_dir(dlt_url, variant)
                if not variant_url:
                    raise RuntimeError(f"Could not find variant folder '{variant}' under DLT.")

                self.log(f"Variant directory: {variant_url}")
                self.log("Scanning dates and collecting matching files...")
                self.ui_queue.put(("progress_mode", "determinate", max(1, total_days), 0))

                http_matches: list = []
                for day_index, day in enumerate(daterange(start_dt.date(), end_dt.date()), start=1):
                    self._raise_if_cancelled()
                    self.ui_queue.put(("progress_value", day_index, f"Scanning {day_index}/{total_days} day(s)..."))
                    year_url = find_child_dir_numeric(variant_url, day.year)
                    if not year_url:
                        continue
                    month_url = find_child_dir_numeric(year_url, day.month)
                    if not month_url:
                        continue
                    day_url = find_child_dir_numeric(month_url, day.day)
                    if not day_url:
                        continue
                    try:
                        day_links = fetch_links(day_url)
                    except NucAuthenticationError:
                        raise
                    except Exception as day_exc:
                        self.log(f"Skipping day {day.isoformat()} due to error: {day_exc}")
                        continue
                    for file_name, file_url, is_dir in day_links:
                        if is_dir:
                            continue
                        if not is_supported_dlt_payload_name(file_name):
                            continue
                        file_ts = parse_filename_timestamp(file_name)
                        if file_ts is None:
                            continue
                        if start_dt <= file_ts <= end_dt:
                            http_matches.append((file_name, file_url, day))

                if http_matches:
                    self.log(f"Found {len(http_matches)} matching file(s). Estimating sizes...")
                    self.ui_queue.put(("progress_mode", "determinate", len(http_matches), 0))
                    sorted_http = sorted(http_matches, key=lambda x: x[0])

                    def estimate_single_file(args):
                        file_name, file_url, day, idx = args
                        self._raise_if_cancelled()
                        remote_size = get_remote_file_size(file_url)
                        return (file_name, file_url, day, remote_size, idx)

                    with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_SIZE_ESTIMATION) as executor:
                        futures = [
                            executor.submit(estimate_single_file, (fn, fu, d, i))
                            for i, (fn, fu, d) in enumerate(sorted_http, start=1)
                        ]
                        for future in concurrent.futures.as_completed(futures):
                            self._raise_if_cancelled()
                            fn, fu, d, remote_size, i = future.result()
                            self.ui_queue.put(("progress_value", i, f"Estimating size {i}/{len(http_matches)}..."))
                            if remote_size is None:
                                unknown_size_count += 1
                            else:
                                expected_total_bytes += remote_size
                            sized_matches.append((fn, fu, d, remote_size))

            sized_matches.sort(key=lambda x: x[0])
            total_files = len(sized_matches)

            if not sized_matches:
                if azure_fs is not None:
                    self.log(
                        "No matches in Azure archive storage. Checking NUC Drive instead. "
                        "Complete sign-in in the Chromium window that opens (3-minute timeout). "
                        "Leave it open until it closes automatically."
                    )
                    self.ui_queue.put(("progress_value", 0, "Waiting for NUC Drive sign-in in Chromium..."))
                    HTTP_OPENER = authenticate_nuc_drive()
                    self.azure_fs = None
                    self._raise_if_cancelled()
                    self.log("NUC Drive sign-in verified. Retrying this download using Drive listings.")
                    return self._run_download(
                        vin, variant, start_dt, end_dt, output_dir, skip_existing, combine_dlt,
                    )
                self.log("No matching DLT files found for the selected time window.")
                self.ui_queue.put(("dialog", "info", "Completed", "No matching DLT files found for the selected time window."))
                return

            mode_tag = f"Azure/{PARALLEL_DOWNLOADS_AZURE} workers" if azure_fs is not None else f"HTTP/{PARALLEL_DOWNLOADS} workers"
            self.log(f"Found {total_files} matching file(s) [{mode_tag}].")

            if unknown_size_count == 0:
                self.log(f"Total download size: {format_bytes(expected_total_bytes)}")
            else:
                self.log(
                    f"Total download size: "
                    f"{format_bytes(expected_total_bytes)} + {unknown_size_count} file(s) with unknown size"
                )

            total_known_bytes_to_download = 0
            unknown_transfer_count = 0
            for file_name, _file_url, _day, remote_size in sized_matches:
                # If a matching decompressed .dlt already exists, this compressed source is skipped.
                existing_dlt_counterpart = get_single_file_dlt_counterpart_path(file_name, output_dir)
                if existing_dlt_counterpart is not None and existing_dlt_counterpart.exists():
                    continue

                local_path = output_dir / file_name
                if skip_existing and local_path.exists():
                    if remote_size is None:
                        continue
                    local_size = get_local_file_size(local_path)
                    if local_size < remote_size:
                        total_known_bytes_to_download += (remote_size - local_size)
                    continue

                if remote_size is None:
                    unknown_transfer_count += 1
                else:
                    total_known_bytes_to_download += remote_size

            if unknown_transfer_count == 0:
                self.log(f"Remaining download size: {format_bytes(total_known_bytes_to_download)}")
            else:
                self.log(
                    "Remaining download size: "
                    f"{format_bytes(total_known_bytes_to_download)} + {unknown_transfer_count} file(s) with unknown size"
                )

            if unknown_transfer_count == 0 and total_known_bytes_to_download > 0:
                self.ui_queue.put(("progress_mode", "determinate", total_known_bytes_to_download, 0))
            else:
                self.ui_queue.put(("progress_mode", "indeterminate", 100, 0))

            download_started_at = time.monotonic()
            speed_monitor_stop = threading.Event()
            speed_state = {
                "total": len(sized_matches),
                "active_workers": 0,
                "completed_files": 0,
                "downloaded_bytes": 0,  # Thread-safe via lock
            }
            speed_metrics = {
                "ema_bps": 0.0,
                "samples": deque([(download_started_at, 0)]),  # rolling (time, total_bytes)
                "last_emit_ts": 0.0,
                "eta_seconds": None,  # Model ETA from throughput
                "eta_display_seconds": None,  # UI ETA that should tick down smoothly
            }

            def emit_speed_update():
                with self.speed_state_lock:
                    total_state = speed_state["total"]
                    active_workers_state = speed_state["active_workers"]
                    completed_state = speed_state["completed_files"]
                    downloaded_state = speed_state["downloaded_bytes"]  # Protected by lock

                if unknown_transfer_count == 0 and total_known_bytes_to_download > 0:
                    total_status = f"{format_bytes(downloaded_state)} / {format_bytes(total_known_bytes_to_download)}"
                    progress_value = downloaded_state
                else:
                    total_status = f"{format_bytes(downloaded_state)} downloaded"
                    progress_value = 0

                now_ts = time.monotonic()
                elapsed = max(now_ts - download_started_at, 1e-6)

                # Emit roughly once per second so ETA naturally ticks down 1s at a time.
                prev_emit_ts = speed_metrics["last_emit_ts"]
                if now_ts - prev_emit_ts < 0.95:
                    return
                speed_metrics["last_emit_ts"] = now_ts
                emit_dt = (now_ts - prev_emit_ts) if prev_emit_ts > 0.0 else 1.0

                samples: deque = speed_metrics["samples"]
                samples.append((now_ts, downloaded_state))
                window_seconds = 60.0
                while len(samples) > 2 and (now_ts - samples[0][0]) > window_seconds:
                    samples.popleft()

                # Speed from rolling 60-second window (responsive to recent changes).
                window_dt = max(now_ts - samples[0][0], 1e-6)
                window_db = max(0, downloaded_state - samples[0][1])
                rolling_window_bps = window_db / window_dt

                # Cumulative average speed (very stable, long-term trend).
                cumulative_bps = downloaded_state / elapsed

                # Blend: 75% cumulative (stable) + 25% rolling window (responsive).
                # This avoids startup lag while maintaining long-window stability.
                blended_bps = (0.75 * cumulative_bps) + (0.25 * rolling_window_bps)

                # Apply EMA to the blended speed for additional smoothing.
                prev_ema = speed_metrics["ema_bps"]
                ema_alpha = 0.20
                if prev_ema <= 0.0:
                    ema_bps = blended_bps
                else:
                    ema_bps = ((1.0 - ema_alpha) * prev_ema) + (ema_alpha * blended_bps)
                speed_metrics["ema_bps"] = max(0.0, ema_bps)

                speed_status = f"{format_bytes(int(max(0.0, rolling_window_bps)))}/s"
                est_speed_status = f"{format_bytes(int(max(0.0, ema_bps)))}/s"

                eta_status = "--"
                if (
                    unknown_transfer_count == 0
                    and total_known_bytes_to_download > 0
                    and ema_bps > 0.1
                    and elapsed >= 15.0
                    and downloaded_state >= 2 * 1024 * 1024
                ):
                    remaining_bytes = max(0, total_known_bytes_to_download - downloaded_state)

                    # Throughput model ETA (target).
                    raw_eta_seconds = remaining_bytes / ema_bps

                    # First layer: smooth the target ETA itself.
                    prev_eta = speed_metrics["eta_seconds"]
                    if prev_eta is None:
                        model_eta_seconds = raw_eta_seconds
                    else:
                        max_change = max(2.0, prev_eta * 0.03)
                        lower = max(0.0, prev_eta - max_change)
                        upper = prev_eta + max_change
                        model_eta_seconds = min(max(raw_eta_seconds, lower), upper)

                    speed_metrics["eta_seconds"] = model_eta_seconds

                    # Second layer: display ETA is a real countdown with small corrections
                    # toward the model ETA. This prevents jumps and avoids counting up.
                    prev_display_eta = speed_metrics["eta_display_seconds"]
                    if prev_display_eta is None:
                        display_eta_seconds = model_eta_seconds
                    else:
                        # Base behavior: countdown in wall-clock time.
                        display_eta_seconds = max(0.0, prev_display_eta - emit_dt)

                        # Slow correction toward model ETA (minor nudges only).
                        error = model_eta_seconds - display_eta_seconds
                        if error > 0.0:
                            # If model is higher, allow only tiny upward correction.
                            correction = min(error, 0.20 * emit_dt)
                        else:
                            # If model is lower, allow slightly stronger downward correction.
                            correction = max(error, -0.60 * emit_dt)
                        display_eta_seconds += correction

                        # Hard per-update bounds to prevent visible jumps.
                        min_allowed = max(0.0, prev_display_eta - (1.4 * emit_dt))
                        max_allowed = prev_display_eta + (0.3 * emit_dt)
                        display_eta_seconds = min(max(display_eta_seconds, min_allowed), max_allowed)

                    speed_metrics["eta_display_seconds"] = display_eta_seconds
                    remaining_seconds = int(max(0.0, display_eta_seconds))
                    hours = remaining_seconds // 3600
                    minutes = (remaining_seconds % 3600) // 60
                    seconds = remaining_seconds % 60
                    eta_status = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    speed_metrics["eta_seconds"] = None
                    speed_metrics["eta_display_seconds"] = None

                status = (
                    f"Files: {completed_state}/{total_state} (active: {active_workers_state}) | "
                    f"Total: {total_status} | Current: {speed_status} | Avg: {est_speed_status} | ETA: {eta_status}"
                )
                self.ui_queue.put(("progress_value", progress_value, status))

            def speed_monitor():
                while not speed_monitor_stop.wait(0.25):
                    emit_speed_update()

            monitor_thread = threading.Thread(target=speed_monitor, daemon=True)
            monitor_thread.start()

            try:
                # Parallel download worker function
                def process_single_file(args):
                    idx, file_name, file_url, _day, remote_size = args
                    result = {
                        "idx": idx,
                        "file_name": file_name,
                        "downloaded": 0,
                        "extracted": 0,
                        "skipped": 0,
                        "removed_archives": 0,
                        "extracted_paths": [],
                        "errors": [],
                    }
                    worker_registered = False
                    
                    try:
                        with self.speed_state_lock:
                            speed_state["active_workers"] += 1
                        worker_registered = True
                        self._raise_if_cancelled()
                        
                        # Check for existing DLT counterpart
                        existing_dlt_counterpart = get_single_file_dlt_counterpart_path(file_name, output_dir)
                        if existing_dlt_counterpart is not None and existing_dlt_counterpart.exists():
                            if is_valid_dlt_file(existing_dlt_counterpart):
                                result["skipped"] += 1
                                result["extracted_paths"].append(existing_dlt_counterpart)
                                self.log(
                                    f"[{idx}/{total_files}] Skipped compressed file because matching DLT exists: "
                                    f"{existing_dlt_counterpart.name}"
                                )
                                return result
                            else:
                                self.log(
                                    f"[{idx}/{total_files}] Found stray/invalid path at expected DLT location "
                                    f"(removing and re-extracting): {existing_dlt_counterpart}"
                                )
                                try:
                                    remove_stray_path(existing_dlt_counterpart)
                                except OSError as cleanup_exc:
                                    self.log(f"Could not remove stray path {existing_dlt_counterpart}: {cleanup_exc}")
                        
                        # Determine path and existing state
                        local_path = output_dir / file_name
                        local_exists = local_path.exists()
                        local_size = get_local_file_size(local_path) if local_exists else 0
                        existing_is_archive = local_exists and is_archive_file(local_path)
                        resume_offset = 0
                        needs_download = True
                        archive_candidate = is_archive_candidate_name(file_name) or existing_is_archive
                        
                        # Check skip_existing logic
                        if skip_existing and local_exists:
                            if remote_size is not None and local_size < remote_size:
                                resume_offset = local_size
                                self.log(
                                    f"[{idx}/{total_files}] Resuming partial file: {file_name} "
                                    f"({format_bytes(local_size)} already present)"
                                )
                            elif remote_size is not None and local_size == remote_size:
                                if archive_candidate:
                                    needs_download = False
                                    self.log(f"[{idx}/{total_files}] Using existing archive: {local_path}")
                                else:
                                    result["skipped"] += 1
                                    if local_path.suffix.lower() == ".dlt":
                                        result["extracted_paths"].append(local_path)
                                    self.log(f"[{idx}/{total_files}] Skipped existing: {local_path}")
                                    return result
                            else:
                                if archive_candidate:
                                    needs_download = False
                                    self.log(f"[{idx}/{total_files}] Using existing archive: {local_path}")
                                else:
                                    result["skipped"] += 1
                                    if local_path.suffix.lower() == ".dlt":
                                        result["extracted_paths"].append(local_path)
                                    self.log(f"[{idx}/{total_files}] Skipped existing: {local_path}")
                                    return result
                        
                        if not skip_existing and local_path.exists():
                            local_path = ensure_unique_path(local_path)
                        
                        self.log(
                            f"[{idx}/{total_files}] {'Downloading' if needs_download else 'Processing existing archive'}: {file_name}"
                        )
                        
                        # Download if needed
                        if needs_download:
                            if azure_fs is not None:
                                # Azure download: resumable retries from a .part file for transient socket/read timeouts.
                                temp_path = local_path.with_name(local_path.name + ".part")

                                # If we previously started this file, resume from .part.
                                if resume_offset > 0 and local_path.exists() and not temp_path.exists():
                                    try:
                                        local_path.replace(temp_path)
                                    except OSError:
                                        pass

                                partial_size = get_local_file_size(temp_path) if temp_path.exists() else 0
                                if remote_size is not None and partial_size > remote_size:
                                    temp_path.unlink(missing_ok=True)
                                    partial_size = 0

                                try:
                                    attempts = 0
                                    while True:
                                        self._raise_if_cancelled()
                                        try:
                                            with azure_fs.open(file_url, "rb") as source, temp_path.open("ab") as target:
                                                if partial_size > 0:
                                                    try:
                                                        source.seek(partial_size)
                                                    except Exception:
                                                        # Fallback if seek is not supported by stream wrapper.
                                                        remaining_skip = partial_size
                                                        while remaining_skip > 0:
                                                            skip_chunk = source.read(min(IO_CHUNK_SIZE_AZURE, remaining_skip))
                                                            if not skip_chunk:
                                                                raise RuntimeError("Failed to skip to resume offset")
                                                            remaining_skip -= len(skip_chunk)

                                                while True:
                                                    self._raise_if_cancelled()
                                                    chunk = source.read(IO_CHUNK_SIZE_AZURE)
                                                    if not chunk:
                                                        break
                                                    target.write(chunk)
                                                    partial_size += len(chunk)
                                                    with self.speed_state_lock:
                                                        speed_state["downloaded_bytes"] += len(chunk)
                                            break
                                        except DownloadCancelledError:
                                            raise
                                        except Exception as exc:
                                            if not is_transient_network_error(exc) or attempts >= AZURE_DOWNLOAD_RETRY_ATTEMPTS:
                                                raise
                                            attempts += 1
                                            wait_s = min(
                                                AZURE_DOWNLOAD_RETRY_MAX_SECONDS,
                                                (2 ** min(attempts, 6)) + (time.monotonic() % 2.0),
                                            )
                                            self.log(
                                                f"[{idx}/{total_files}] Azure retry {attempts}/{AZURE_DOWNLOAD_RETRY_ATTEMPTS} "
                                                f"for {file_name} in {wait_s:.1f}s: {exc}"
                                            )
                                            if self.cancel_event.wait(wait_s):
                                                raise DownloadCancelledError("Download canceled by user.")

                                    temp_path.replace(local_path)
                                    result["downloaded"] += 1
                                except DownloadCancelledError:
                                    raise
                                except Exception as exc:
                                    # Keep partial file so next run can resume rather than restart.
                                    raise RuntimeError(f"Azure download failed for {file_name}: {exc}") from exc
                            else:
                                # HTTP download: manual retry/resume logic
                                def on_chunk(chunk_len):
                                    with self.speed_state_lock:
                                        speed_state["downloaded_bytes"] += chunk_len

                                download_file(
                                    file_url,
                                    local_path,
                                    on_chunk=on_chunk,
                                    retries=None,
                                    resume_offset=resume_offset,
                                    cancel_event=self.cancel_event,
                                    on_timeout_retry=lambda msg, i=idx: self.log(f"[{i}/{total_files}] {msg}"),
                                )
                                result["downloaded"] += 1
                        
                        self._raise_if_cancelled()
                        emit_speed_update()
                        
                        # Archive detection and extraction
                        file_exists = local_path.exists()
                        is_archive_by_content = False
                        if file_exists:
                            try:
                                is_archive_by_content = is_archive_file(local_path)
                            except Exception as archive_check_exc:
                                self.log(f"[{idx}/{total_files}] Error checking if file is archive: {archive_check_exc}")
                        
                        is_archive = archive_candidate or is_archive_by_content
                        
                        self.log(
                            f"[{idx}/{total_files}] File check: name={file_name}, "
                            f"exists={file_exists}, is_archive_format={is_archive_candidate_name(file_name)}, "
                            f"is_archive_content={is_archive_by_content}, is_archive={is_archive}"
                        )
                        
                        if is_archive and file_exists:
                            self.log(f"[{idx}/{total_files}] Detected archive. Extracting DLT files...")
                            try:
                                extracted_now, skipped_now, found_now, extracted_paths = extract_dlt_files_from_archive(
                                    local_path, output_dir, skip_existing
                                )
                                result["extracted"] += extracted_now
                                result["skipped"] += skipped_now
                                result["extracted_paths"].extend(extracted_paths)
                                if found_now == 0:
                                    self.log(f"[{idx}/{total_files}] No .dlt files found inside archive: {local_path.name}")
                                else:
                                    self.log(
                                        f"[{idx}/{total_files}] Extracted {extracted_now} DLT file(s), "
                                        f"found {found_now} total in archive (skipped existing: {skipped_now})"
                                    )
                            except Exception as extract_exc:
                                result["errors"].append(f"Extraction failed: {extract_exc}")
                                self.log(f"[{idx}/{total_files}] Error extracting archive {local_path.name}: {extract_exc}")
                                self.log(f"Extraction error details: {traceback.format_exc()[:500]}")
                            
                            # Clean up archive file
                            try:
                                if local_path.exists():
                                    local_path.unlink(missing_ok=True)
                                    result["removed_archives"] += 1
                                    self.log(f"[{idx}/{total_files}] Removed archive file: {local_path.name}")
                                else:
                                    self.log(f"[{idx}/{total_files}] Archive file already missing: {local_path.name}")
                            except OSError as unlink_exc:
                                self.log(f"Could not remove archive {local_path.name}: {unlink_exc}")
                        elif file_exists and local_path.suffix.lower() == ".dlt":
                            result["extracted_paths"].append(local_path)
                            self.log(f"[{idx}/{total_files}] Tracking DLT file for combine: {local_path.name}")
                        else:
                            suffix = local_path.suffix.lower() if file_exists else "n/a"
                            self.log(f"[{idx}/{total_files}] File not processed (not archive, not .dlt): {file_name} (suffix: {suffix})")
                        
                        self._raise_if_cancelled()
                        emit_speed_update()
                        
                    except Exception as worker_exc:
                        result["errors"].append(str(worker_exc))
                        self.log(f"[{idx}/{total_files}] Unexpected error processing {file_name}: {worker_exc}")
                        self.log(f"Error details: {traceback.format_exc()[:500]}")
                    finally:
                        if worker_registered:
                            with self.speed_state_lock:
                                speed_state["active_workers"] = max(0, speed_state["active_workers"] - 1)
                    
                    return result
                
                # Launch parallel downloads using ThreadPoolExecutor
                with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_workers) as executor:
                    futures = [
                        executor.submit(process_single_file, (idx, file_name, file_url, _day, remote_size))
                        for idx, (file_name, file_url, _day, remote_size) in enumerate(sized_matches, start=1)
                    ]
                    
                    # Collect results as they complete (order doesn't matter)
                    for future in concurrent.futures.as_completed(futures):
                        self._raise_if_cancelled()
                        try:
                            result = future.result()
                            # Aggregate results safely
                            with self.speed_state_lock:
                                downloaded += result["downloaded"]
                                extracted_dlt += result["extracted"]
                                removed_archives += result["removed_archives"]
                                skipped_existing += result["skipped"]
                                dlt_files_for_combine.extend(result["extracted_paths"])
                                speed_state["completed_files"] += 1
                        except Exception as result_exc:
                            self.log(f"Error collecting result from parallel download: {result_exc}")
            finally:
                speed_monitor_stop.set()
                monitor_thread.join(timeout=1.0)

            self._raise_if_cancelled()
            self.log(f"Preparing combine phase: {len(dlt_files_for_combine)} total DLT file(s) tracked.")
            resolved_candidates = sorted({p.resolve() for p in dlt_files_for_combine if p.exists()}, key=lambda p: p.name.lower())
            unique_dlt_paths = [p for p in resolved_candidates if is_valid_dlt_file(p)]
            invalid_paths = [p for p in resolved_candidates if not is_valid_dlt_file(p)]
            if invalid_paths:
                self.log(
                    f"Ignoring {len(invalid_paths)} stray/invalid path(s) that are not real DLT files "
                    f"(directories or empty placeholders left by a previous run): "
                    + ", ".join(p.name for p in invalid_paths)
                )
                for stray in invalid_paths:
                    try:
                        remove_stray_path(stray)
                    except OSError as cleanup_exc:
                        self.log(f"Could not remove stray path {stray}: {cleanup_exc}")
            self.log(f"Found {len(unique_dlt_paths)} existing DLT file(s) ready to combine.")
            combined_file_path = None
            if combine_dlt and unique_dlt_paths:
                combined_name = (
                    f"combined_{vin}_{variant}_"
                    f"{start_dt.strftime('%Y%m%dT%H%M%S')}_to_{end_dt.strftime('%Y%m%dT%H%M%S')}.dlt"
                )
                combined_file_path = output_dir / combined_name
                if combined_file_path.exists():
                    combined_file_path = ensure_unique_path(combined_file_path)
                self.log(f"Combining {len(unique_dlt_paths)} DLT file(s) into: {combined_file_path.name}")
                self._raise_if_cancelled()
                try:
                    combine_dlt_files(unique_dlt_paths, combined_file_path)
                    self.log(f"Successfully created combined DLT file: {combined_file_path.name}")
                except Exception as combine_exc:
                    self.log(f"Error combining DLT files: {combine_exc}")
                    combined_file_path = None
            elif not combine_dlt:
                self.log("DLT combine is disabled for this run.")
            else:
                self.log(f"No DLT files available to combine for this run. (Tracked: {len(dlt_files_for_combine)}, Existing: {len(unique_dlt_paths)})")

            summary = (
                f"Completed. Downloaded: {downloaded}, "
                f"Extracted DLT: {extracted_dlt}, "
                f"Removed archives: {removed_archives}, "
                f"Skipped existing: {skipped_existing}, Total matched: {total_files}, "
                f"Combined file: {combined_file_path.name if combined_file_path else 'not created'}"
            )
            self.log(summary)
            self.ui_queue.put(("dialog", "info", "Completed", summary))

        except DownloadCancelledError as exc:
            self.log(str(exc))
            self.ui_queue.put(("dialog", "info", "Canceled", "Download canceled by user."))
        except Exception as exc:
            self.log(f"Error: {exc}")
            self.ui_queue.put(("dialog", "error", "Download failed", str(exc)))
        finally:
            self.ui_queue.put(("set_running", False))


def main():
    app = DownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
