import json
import importlib.util
import os
from pathlib import Path
import unittest
from unittest import mock


MODULE_PATH = (
    Path(__file__).parents[1]
    / "addon"
    / "globalPlugins"
    / "visionAssistant"
    / "utils"
    / "secure_credentials.py"
)
SPEC = importlib.util.spec_from_file_location("secure_credentials", MODULE_PATH)
secure_credentials = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(secure_credentials)


FAKE_SECRET = "synthetic-test-credential"


class SecureCredentialTests(unittest.TestCase):
    def test_dpapi_round_trip(self):
        if os.name != "nt":
            self.skipTest("DPAPI is available only on Windows")
        protected = secure_credentials.protect_credential(FAKE_SECRET)
        self.assertTrue(protected.startswith(secure_credentials.DPAPI_PREFIX))
        self.assertNotIn(FAKE_SECRET, protected)
        self.assertEqual(FAKE_SECRET, secure_credentials.unprotect_credential(protected))

    def test_protection_failure_has_no_plaintext_fallback(self):
        with mock.patch.object(
            secure_credentials,
            "_protect_bytes",
            side_effect=OSError("simulated DPAPI failure"),
        ):
            with self.assertRaises(secure_credentials.CredentialProtectionError):
                secure_credentials.protect_credential(FAKE_SECRET)

    def test_plaintext_is_rejected_by_unprotect(self):
        with self.assertRaises(secure_credentials.CredentialProtectionError):
            secure_credentials.unprotect_credential(FAKE_SECRET)

    def test_migration_removes_plaintext_from_serialized_config(self):
        configuration = {field: "" for field in secure_credentials.CREDENTIAL_FIELDS}
        configuration["api_key"] = FAKE_SECRET
        configuration["banned_gemini_keys"] = json.dumps(
            {f"{FAKE_SECRET}::gemini-test": 1234567890}
        )
        with mock.patch.object(secure_credentials, "_protect_bytes", return_value=b"ciphertext"):
            changed = secure_credentials.migrate_credentials(configuration)
        self.assertTrue(changed)
        serialized = json.dumps(configuration)
        self.assertNotIn(FAKE_SECRET, serialized)
        self.assertTrue(configuration["api_key"].startswith(secure_credentials.DPAPI_PREFIX))
        self.assertIn("sha256:", configuration["banned_gemini_keys"])

    def test_failed_migration_does_not_partially_update_credentials(self):
        configuration = {field: "" for field in secure_credentials.CREDENTIAL_FIELDS}
        configuration["api_key"] = "first-secret"
        configuration["openai_api_key"] = "second-secret"
        with mock.patch.object(
            secure_credentials,
            "_protect_bytes",
            side_effect=[b"first-ciphertext", OSError("simulated failure")],
        ):
            with self.assertRaises(secure_credentials.CredentialProtectionError):
                secure_credentials.migrate_credentials(configuration)
        self.assertEqual("first-secret", configuration["api_key"])
        self.assertEqual("second-secret", configuration["openai_api_key"])

    def test_restore_keeps_credentials_decryptable_by_current_user(self):
        protected = secure_credentials.DPAPI_PREFIX + "current-user-ciphertext"
        configuration = {"api_key": protected, "openai_api_key": ""}
        with mock.patch.object(
            secure_credentials,
            "unprotect_credential",
            return_value=FAKE_SECRET,
        ):
            unavailable = secure_credentials.prepare_restored_credentials(configuration)
        self.assertEqual((), unavailable)
        self.assertEqual(protected, configuration["api_key"])

    def test_restore_clears_credentials_from_another_windows_user(self):
        protected = secure_credentials.DPAPI_PREFIX + "foreign-ciphertext"
        configuration = {
            "api_key": protected,
            "openai_api_key": "",
            "active_provider": "gemini",
        }
        with mock.patch.object(
            secure_credentials,
            "unprotect_credential",
            side_effect=secure_credentials.CredentialProtectionError("foreign DPAPI data"),
        ):
            unavailable = secure_credentials.prepare_restored_credentials(configuration)
        self.assertEqual(("api_key",), unavailable)
        self.assertEqual("", configuration["api_key"])
        self.assertEqual("gemini", configuration["active_provider"])

    def test_restore_protects_legacy_plaintext_before_applying_it(self):
        configuration = {"api_key": FAKE_SECRET, "openai_api_key": ""}
        with mock.patch.object(
            secure_credentials,
            "_protect_bytes",
            return_value=b"restored-ciphertext",
        ):
            unavailable = secure_credentials.prepare_restored_credentials(configuration)
        self.assertEqual((), unavailable)
        self.assertNotIn(FAKE_SECRET, json.dumps(configuration))
        self.assertTrue(configuration["api_key"].startswith(secure_credentials.DPAPI_PREFIX))

    def test_protected_backup_keeps_dpapi_and_contains_no_plaintext(self):
        protected = secure_credentials.DPAPI_PREFIX + "backup-ciphertext"
        configuration = {"api_key": protected, "openai_api_key": ""}
        with mock.patch.object(
            secure_credentials,
            "unprotect_credential",
            return_value=FAKE_SECRET,
        ):
            secure_credentials.prepare_backup_credentials(configuration, protect=True)
        self.assertEqual(protected, configuration["api_key"])
        self.assertNotIn(FAKE_SECRET, json.dumps(configuration))

    def test_portable_backup_exports_plaintext_from_dpapi(self):
        protected = secure_credentials.DPAPI_PREFIX + "backup-ciphertext"
        configuration = {"api_key": protected, "openai_api_key": ""}
        with mock.patch.object(
            secure_credentials,
            "unprotect_credential",
            return_value=FAKE_SECRET,
        ):
            secure_credentials.prepare_backup_credentials(configuration, protect=False)
        self.assertEqual(FAKE_SECRET, configuration["api_key"])
        self.assertNotIn(secure_credentials.DPAPI_PREFIX, json.dumps(configuration))

    def test_redaction_covers_known_secrets_headers_and_urls(self):
        text = (
            f"secret={FAKE_SECRET} Authorization: Bearer abc123 "
            "x-goog-api-key: xyz789 https://example.test/?key=query-secret&ok=1"
        )
        redacted = secure_credentials.redact_text(text, [FAKE_SECRET])
        for secret in (FAKE_SECRET, "abc123", "xyz789", "query-secret"):
            self.assertNotIn(secret, redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_redaction_values_include_dpapi_envelope_and_each_configured_key(self):
        protected = secure_credentials.DPAPI_PREFIX + "ciphertext"
        plaintext = "first-test-key, second-test-key\nthird-test-key"
        with mock.patch.object(
            secure_credentials,
            "unprotect_credential",
            return_value=plaintext,
        ):
            values = secure_credentials.credential_redaction_values(protected)
        for sensitive_value in (
            protected,
            plaintext,
            "first-test-key",
            "second-test-key",
            "third-test-key",
        ):
            self.assertIn(sensitive_value, values)
        rendered = secure_credentials.redact_text(
            " ".join((protected, plaintext, "first-test-key", "second-test-key", "third-test-key")),
            values,
        )
        for sensitive_value in values:
            self.assertNotIn(sensitive_value, rendered)


if __name__ == "__main__":
    unittest.main()
