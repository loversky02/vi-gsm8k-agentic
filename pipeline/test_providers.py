"""Gọi thử 1 lần mỗi subagent để chẩn đoán đường ống. KHÔNG in key."""
from dotenv import load_dotenv
load_dotenv()

from llm_client import call_llm  # noqa: E402

PROMPT = [{"role": "user", "content": "Trả lời đúng một từ: OK"}]

for role in ["challenger", "strong", "weak", "verifier"]:
    try:
        out = call_llm(role, PROMPT)
        print(f"[OK]  {role:10s} -> {repr((out or '')[:60])}")
    except Exception as e:
        import traceback
        print(f"[LỖI] {role:10s} -> {str(e)[:160]}")
        print("    " + "\n    ".join(traceback.format_exc().strip().splitlines()[-6:]))
