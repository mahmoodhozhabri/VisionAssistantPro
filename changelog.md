## Changes for 6.1.2

*   **Duplicate Label Pre-Check**: Fixed an issue in single labeling where the duplicate check used old coordinate keys, causing NVDA to make duplicate AI requests for already labeled objects instead of announcing the existing label.
*   **Document Chat for Non-Gemini Providers**: Fixed a strict API key check in Document Chat (`on_ask`) to ensure that users on OpenAI, Groq, or local Custom providers (like Ollama) can successfully chat with documents without being blocked.
*   **Fast Chrome OCR Translation**: Restored the free, keyless translation API for Chrome OCR. Translating extracted text now bypasses Gemini AI, saving API quotas and speeding up the translation process.
*   **CAPTCHA Alphanumeric Filter**: Corrected the filtering logic in the CAPTCHA solver to ensure non-alphanumeric characters are properly cleaned in all situations.
*   **Command Layer Help Update**: Corrected the status announcement shortcut in the help menu from `L` to `I`, and added both labeling commands (`L` and `Shift+L`) to the list.