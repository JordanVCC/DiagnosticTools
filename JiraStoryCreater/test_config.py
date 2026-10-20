import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


class CredentialConfigTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        shutil.copy2(Path(__file__).with_name("config.py"), self.root / "config.py")
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def load_config(self):
        spec = importlib.util.spec_from_file_location("isolated_config", self.root / "config.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def write_secrets(self, data):
        (self.root / "secrets.local.json").write_text(json.dumps(data), encoding="utf-8")

    def test_environment_only(self):
        os.environ.update(CONFLUENCE_PAT="test-confluence", VIRA_PAT="test-vira")
        config = self.load_config()
        self.assertEqual(config.CONFLUENCE_PAT, "test-confluence")
        self.assertEqual(config.VIRA_PAT, "test-vira")

    def test_local_file_only(self):
        self.write_secrets({"CONFLUENCE_PAT": "test-local-confluence", "VIRA_PAT": "test-local-vira"})
        config = self.load_config()
        self.assertEqual(config.CONFLUENCE_PAT, "test-local-confluence")
        self.assertEqual(config.VIRA_PAT, "test-local-vira")

    def test_environment_overrides_local_file(self):
        self.write_secrets({"CONFLUENCE_PAT": "test-local", "VIRA_PAT": "test-local-vira"})
        os.environ["CONFLUENCE_PAT"] = "test-override"
        config = self.load_config()
        self.assertEqual(config.CONFLUENCE_PAT, "test-override")
        self.assertEqual(config.VIRA_PAT, "test-local-vira")

    def test_missing_credentials_fail(self):
        with self.assertRaisesRegex(RuntimeError, "CONFLUENCE_PAT"):
            self.load_config()

    def test_invalid_local_values_fail(self):
        for value in (None, 123, "", "   "):
            with self.subTest(value=value):
                self.write_secrets({"CONFLUENCE_PAT": value})
                with self.assertRaisesRegex(RuntimeError, "missing or invalid"):
                    self.load_config()

    def test_nonobject_json_fails(self):
        self.write_secrets(["test-value"])
        with self.assertRaisesRegex(RuntimeError, "JSON object"):
            self.load_config()

    def test_malformed_json_does_not_expose_contents(self):
        (self.root / "secrets.local.json").write_text("test-private-invalid-json", encoding="utf-8")
        with self.assertRaises(RuntimeError) as captured:
            self.load_config()
        self.assertNotIn("test-private", str(captured.exception))


if __name__ == "__main__":
    unittest.main()