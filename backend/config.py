import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

# The assignment is designed to run with deterministic local logic.
# Do not fail the backend startup if the external Gemini API key is absent.
