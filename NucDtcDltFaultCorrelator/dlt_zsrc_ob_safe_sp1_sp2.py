import os
import re
import tempfile
from datetime import datetime
import time

import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ServiceResponseTimeoutError

# ====================================================
# CONFIGURATION
# ====================================================

ACCOUNT   = "sys34e8eca5"
CONTAINER = "default"
PREFIX = "data_nuc/data_dlt/master_v6/"

START_DATE = "2026-04-30"   # ✅ change freely
START_DATE_DT = datetime.strptime(START_DATE, "%Y-%m-%d")

OUTPUT_CSV   = "ZSRC_SP1_SP2_master_v6.csv"
OUTPUT_EXCEL = "ZSRC_SP1_SP2_master_v6.xlsx"
PROCESSED_LOG = "processed_blobs.txt"

DOWNLOAD_TIMEOUT = 180
DOWNLOAD_RETRIES = 2

# ====================================================
# REGEX DEFINITIONS
# ====================================================

VIN_RE = re.compile(r"vin=([A-HJ-NPR-Z0-9]{17})")
FILE_DATE_RE = re.compile(r"/(\d{8})T")

SRC_RE = re.compile(r"\b(SRCF|SRCL|SRCR|SRCB)\b")

# SP block capture (everything after SP1 / SP2 until next SP or end)
SP1_BLOCK_RE = re.compile(r"\bSP1\b\s+(.*?)(?=\s+SP2\b|$)")
SP2_BLOCK_RE = re.compile(r"\bSP2\b\s+(.*)$")

# Values: index:xxxx:value
SP_VALUE_RE = re.compile(r"(\d+):\d+:(-?\d+)")

# ====================================================
# AZURE CONNECTION
# ====================================================

print("Connecting to Azure Blob Storage...")
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url=f"https://{ACCOUNT}.blob.core.windows.net",
    credential=credential,
)
container = blob_service.get_container_client(CONTAINER)

# ====================================================
# LOAD PROCESSED BLOBS (RESUME SUPPORT)
# ====================================================

processed_blobs = set()
if os.path.exists(PROCESSED_LOG):
    with open(PROCESSED_LOG) as f:
        processed_blobs = set(l.strip() for l in f if l.strip())

# ====================================================
# MAIN LOOP
# ====================================================

print(f"\nScanning Parquets under {PREFIX}")
print(f"Filename date filter >= {START_DATE}\n")

processed_count = 0

try:
    for blob in container.list_blobs(name_starts_with=PREFIX):

        if not blob.name.endswith(".parquet"):
            continue
        if "/ecu=HPA/" not in blob.name:
            continue
        if blob.name in processed_blobs:
            continue

        date_m = FILE_DATE_RE.search(blob.name)
        if not date_m:
            continue

        file_date = datetime.strptime(date_m.group(1), "%Y%m%d")
        if file_date < START_DATE_DT:
            continue

        vin_m = VIN_RE.search(blob.name)
        vin = vin_m.group(1) if vin_m else None

        print(f"Processing: {blob.name}")

        with tempfile.TemporaryDirectory() as tmp:
            local_file = os.path.join(tmp, "file.parquet")

            success = False
            for _ in range(DOWNLOAD_RETRIES):
                try:
                    downloader = container.download_blob(blob.name, timeout=DOWNLOAD_TIMEOUT)
                    with open(local_file, "wb") as f:
                        for chunk in downloader.chunks():
                            f.write(chunk)
                    success = True
                    break
                except ServiceResponseTimeoutError:
                    print("⚠️ Download timeout, retrying...")

            if not success:
                print("❌ Skipping due to download failure")
                continue

            # Read only required columns
            df = pd.read_parquet(
                local_file,
                columns=["application_id", "timestamp", "message"],
            )

            hits = df[
                (df["application_id"] == "ZSRC") &
                df["message"].str.contains("SP1", na=False)
            ]

            if hits.empty:
                with open(PROCESSED_LOG, "a") as f:
                    f.write(blob.name + "\n")
                processed_blobs.add(blob.name)
                continue

            rows = []

            for _, r in hits.iterrows():
                msg = r["message"]

                src_m = SRC_RE.search(msg)
                if not src_m:
                    continue

                row = {
                    "VIN": vin,
                    "Timestamp": r["timestamp"],
                    "Camera": src_m.group(1),
                }

                # ---------- SP1 ----------
                sp1_m = SP1_BLOCK_RE.search(msg)
                if sp1_m:
                    for i, v in SP_VALUE_RE.findall(sp1_m.group(1)):
                        row[f"SP1_{i}"] = int(v)

                # ---------- SP2 ----------
                sp2_m = SP2_BLOCK_RE.search(msg)
                if sp2_m:
                    for i, v in SP_VALUE_RE.findall(sp2_m.group(1)):
                        row[f"SP2_{i}"] = int(v)

                rows.append(row)

            if rows:
                out_df = pd.DataFrame(rows)
                csv_exists = os.path.exists(OUTPUT_CSV)
                out_df.to_csv(
                    OUTPUT_CSV,
                    mode="a",
                    header=not csv_exists,
                    index=False,
                )

            with open(PROCESSED_LOG, "a") as f:
                f.write(blob.name + "\n")
            processed_blobs.add(blob.name)
            processed_count += 1

except KeyboardInterrupt:
    print("\n🛑 Interrupted by user")
finally:
    print(f"\n✅ Processed {processed_count} parquet files")

    if os.path.exists(OUTPUT_CSV):
        print("📄 Generating Excel from CSV...")
        pd.read_csv(OUTPUT_CSV).to_excel(OUTPUT_EXCEL, index=False)
        print(f"✅ Excel available: {OUTPUT_EXCEL}")
    else:
        print("⚠️ No CSV generated (no data found)")