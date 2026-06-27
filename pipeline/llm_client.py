"""Gọi LLM qua litellm (1 interface cho mọi nhà). Có chế độ MOCK để test không cần API key."""
import json
import os
import time

from config import MOCK, ROLES


def _mock(role, idx):
    """Trả output giả nhất quán để demo GATE: ~1/3 đề 'quá dễ' bị loại, còn lại giữ."""
    expected = 7 + idx
    if role == "challenger":
        return json.dumps(
            {"question": f"Một cửa hàng có {10 + idx} kg gạo, bán đi 3 kg. Hỏi còn lại bao nhiêu kg?",
             "final_answer": str(expected), "topic": "phép trừ"},
            ensure_ascii=False)
    if role == "strong":
        return f"Cửa hàng còn: {10 + idx} - 3 = {expected} kg.\nĐÁP ÁN CUỐI: {expected}"
    if role == "weak":
        ans = expected if idx % 3 == 0 else expected + 5  # idx%3==0 -> weak đúng -> 'quá dễ' -> loại
        return f"Nhẩm nhanh.\nĐÁP ÁN CUỐI: {ans}"
    if role == "verifier":
        return json.dumps({"valid": True, "reason": "Các bước hợp lệ"}, ensure_ascii=False)
    return ""


def call_llm(role, messages, idx=0):
    cfg = ROLES[role]
    if MOCK:
        return _mock(role, idx)
    from litellm import completion  # import trễ: chế độ MOCK không cần cài litellm
    kwargs = {"model": cfg["model"], "messages": messages}
    if cfg.get("temperature") is not None:     # vài model (gpt-5/claude qua router) không nhận temperature
        kwargs["temperature"] = cfg["temperature"]
    if cfg.get("api_base"):                       # endpoint tuỳ biến (vd 9router)
        kwargs["api_base"] = cfg["api_base"]
    if cfg.get("api_key_env"):                    # key riêng cho endpoint đó
        k = os.getenv(cfg["api_key_env"])
        if k:
            kwargs["api_key"] = k
    last = None
    for attempt in range(3):
        try:
            r = completion(**kwargs)
            return r.choices[0].message.content
        except Exception as e:  # retry với backoff
            last = e
            time.sleep(2 * (attempt + 1))
    raise last
