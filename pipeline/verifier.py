"""Trọng tài chính: trích + so khớp đáp án SỐ (code-execution nhẹ, không eval code lạ)."""
import re


def extract_answer(text):
    """Trích đáp án số từ output solver. Ưu tiên marker 'ĐÁP ÁN CUỐI', rồi \\boxed{}, rồi số cuối."""
    if not text:
        return None
    m = re.search(r"ĐÁP\s*ÁN\s*CUỐI\s*[:：]\s*(.+)", text, re.IGNORECASE)
    seg = m.group(1) if m else text
    m2 = re.search(r"\\boxed\{([^}]*)\}", seg)
    if m2:
        seg = m2.group(1)
    nums = re.findall(r"-?\d+(?:\.\d+)?", seg.replace(",", ""))  # bỏ dấu phẩy ngăn cách nghìn
    return nums[-1] if nums else None


def _normalize(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return s


def answers_match(a, b, tol=1e-6):
    """So khớp 2 đáp án: ưu tiên số (sai số nhỏ), fallback so chuỗi."""
    na, nb = _normalize(a), _normalize(b)
    if na is None or nb is None:
        return False
    if isinstance(na, float) and isinstance(nb, float):
        return abs(na - nb) <= tol
    return str(na) == str(nb)
