"""Thử các tên model Gemini xem key truy cập được bản nào. KHÔNG in key."""
import os

from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY", "").encode("ascii", "ignore").decode().strip()

from litellm import completion  # noqa: E402

CANDIDATES = [
    "gemini-3-pro", "gemini-3-pro-preview", "gemini-3.0-pro", "gemini-3-flash",
    "gemini-2.5-pro", "gemini-2.5-flash",
]
for m in CANDIDATES:
    try:
        completion(model=f"gemini/{m}", messages=[{"role": "user", "content": "Nói đúng một từ: OK"}])
        print(f"[OK]    {m}")
    except Exception as e:
        print(f"[không] {m}: {str(e)[:90]}")
