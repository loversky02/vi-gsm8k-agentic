"""Cấu hình 4 subagent + tham số pipeline.

Model string theo định dạng litellm.
- Challenger (Gemini) + Weak (DeepSeek): key trực tiếp (GEMINI_API_KEY / DEEPSEEK_API_KEY).
- Strong (GPT) + Verifier (Claude): qua 9router tự host (OpenAI-compatible), cùng ROUTER_API_KEY.
"""
import os

# Làm sạch API key dán từ web: loại ký tự ẩn non-ASCII gây lỗi header httpx.
for _k in ("GEMINI_API_KEY", "DEEPSEEK_API_KEY", "ROUTER_API_KEY", "OPENAI_API_KEY"):
    _v = os.environ.get(_k)
    if _v:
        os.environ[_k] = _v.encode("ascii", "ignore").decode().strip()

MOCK = os.getenv("AUTODATA_MOCK", "0") == "1"

# 9router (tự host) — endpoint OpenAI-compatible cho GPT + Claude
ROUTER_BASE = os.getenv("ROUTER_API_BASE", "https://9router-production-e72e.up.railway.app/v1")

# Vai trò -> cấu hình. api_base/api_key_env chỉ cần cho endpoint tuỳ biến (9router).
ROLES = {
    # Challenger = DeepSeek chat (Gemini đã cạn credit; deepseek-chat rẻ + cache 75% + tiếng Việt tốt)
    "challenger": {"model": os.getenv("M_CHALLENGER", "deepseek/deepseek-chat"), "temperature": 1.0},
    "strong": {
        "model": os.getenv("M_STRONG", "openai/cx/gpt-5.5"),            # GPT-5.5 qua 9router
        "api_base": ROUTER_BASE,
        "api_key_env": "ROUTER_API_KEY",
        "temperature": 1.0,    # GPT-5 chỉ hỗ trợ temperature=1
    },
    "weak": {"model": os.getenv("M_WEAK", "deepseek/deepseek-chat"), "temperature": 0.8},
    "verifier": {
        "model": os.getenv("M_VERIFIER", "openai/cc/claude-opus-4-8"),  # Claude qua 9router
        "api_base": ROUTER_BASE,
        "api_key_env": "ROUTER_API_KEY",
        "temperature": None,   # Claude qua router không nhận temperature
    },
}

MAX_REFINE = int(os.getenv("AUTODATA_MAX_REFINE", "2"))  # số vòng refine tối đa (chống đốt token)
