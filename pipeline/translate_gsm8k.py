"""Dịch GSM8K sang tiếng Việt (chạy local, không cần GPU).
--mode eval     : chỉ dịch đề  -> {question, final_answer}  (held-out eval set)
--mode baseline : dịch đề+lời giải -> {question, chain_of_thought, final_answer}  (data dịch máy để so baseline)
"""
import argparse
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

load_dotenv()
for _k in ("GEMINI_API_KEY", "DEEPSEEK_API_KEY"):
    if os.environ.get(_k):
        os.environ[_k] = os.environ[_k].encode("ascii", "ignore").decode().strip()

MODEL = os.getenv("M_TRANSLATE", "gemini/gemini-2.5-flash")

EVAL_P = ("Dịch bài toán sau sang tiếng Việt tự nhiên, giữ NGUYÊN mọi con số. "
          "Chỉ trả về bản dịch đề bài, KHÔNG giải.\n\n{q}")
BASE_P = '''Dịch đề bài và lời giải toán sau sang tiếng Việt tự nhiên, giữ nguyên mọi con số và phép tính.
Trả về DUY NHẤT một JSON:
{{"question": "<đề tiếng Việt>", "chain_of_thought": "<lời giải tiếng Việt, kết thúc bằng dòng: ĐÁP ÁN CUỐI: {num}>"}}

ĐỀ: {q}
LỜI GIẢI: {sol}'''


def gsm_num(ans):
    m = re.search(r"####\s*([\-\d,\.]+)", ans)
    return m.group(1).replace(",", "").strip() if m else None


def gsm_reason(ans):
    return re.sub(r"####.*", "", ans, flags=re.S).strip()


def llm(text):
    from litellm import completion
    last = None
    for _ in range(3):
        try:
            return completion(model=MODEL, messages=[{"role": "user", "content": text}],
                              temperature=0.3).choices[0].message.content
        except Exception as e:
            last = e
    raise last


def _json(t):
    m = re.search(r"\{.*\}", t or "", re.S)
    try:
        return json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=["eval", "baseline"], required=True)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.inp, encoding="utf-8") if l.strip()]
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    fout = open(a.out, "w", encoding="utf-8")
    lock = threading.Lock()

    def task(idx, r):
        num = gsm_num(r["answer"])
        if num is None:
            return None
        if a.mode == "eval":
            qv = llm(EVAL_P.format(q=r["question"])).strip()
            return {"id": f"vi-eval-{idx:04d}", "question": qv, "final_answer": num,
                    "lang": "vi", "source": "gsm8k-test"}
        d = _json(llm(BASE_P.format(q=r["question"], sol=gsm_reason(r["answer"]), num=num)))
        if not d.get("question") or not d.get("chain_of_thought"):
            return None
        return {"id": f"vi-base-{idx:04d}", "question": d["question"],
                "chain_of_thought": d["chain_of_thought"], "final_answer": num,
                "lang": "vi", "source": "gsm8k-train-translated"}

    ok = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(task, i, r) for i, r in enumerate(rows)]
        for fu in as_completed(futs):
            try:
                res = fu.result()
            except Exception:
                res = None
            if res:
                with lock:
                    fout.write(json.dumps(res, ensure_ascii=False) + "\n")
                    fout.flush()
                    ok += 1
    fout.close()
    print(f"Dịch xong ({a.mode}): {ok}/{len(rows)} -> {a.out}")


if __name__ == "__main__":
    main()
