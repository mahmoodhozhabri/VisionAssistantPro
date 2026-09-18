# Credential-storage hardening

This branch stores provider API credentials with Windows Data Protection API
(DPAPI) rather than as recoverable plaintext in NVDA configuration.

## Security properties

- Every supported provider credential is written as `!!dpapi:v1:<base64>`.
- DPAPI uses the current Windows user scope plus Vision Assistant-specific
  optional entropy. Copying `nvda.ini` to another user or computer does not
  produce usable credentials.
- Encryption and decryption run with UI disabled. If DPAPI is unavailable or
  fails, the operation raises an error; there is no plaintext fallback.
- Existing plaintext settings are migrated before providers and file logging
  initialize. The updated NVDA configuration is saved immediately.
- Gemini quota tracking stores a truncated SHA-256 fingerprint instead of an
  API key.
- Settings backups contain DPAPI ciphertext. Consequently, a backup containing
  credentials is intentionally restorable only by the same Windows user.
- Dedicated file logs redact configured credentials, authorization headers,
  API-key headers, and common key-bearing URL query parameters.

Plaintext credentials still exist briefly in process memory when entered or
used. DPAPI protects credentials at rest; it is not a defence against malware
already running as the same Windows user or code executing inside NVDA.

## Verification

Run the focused tests from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The suite includes a real Windows DPAPI round trip, fail-closed simulations,
legacy migration checks, persistence assertions, and logging-redaction
coverage. No real API key is needed for development or testing.
