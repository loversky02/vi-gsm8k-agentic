"""Eval model trên eval set VN bằng BATCH generate (nhanh). Verify đáp án bằng code -> accuracy.
CHẠY TRÊN H100. Ví dụ:
  python eval_model.py                         # base zero-shot
  python eval_model.py --adapter ckpt/ours
  python eval_model.py --adapter ckpt/baseline
"""
import argparse
import json
import re

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

SYS = "Giải bài toán bằng tiếng Việt, trình bày từng bước, kết thúc bằng đúng một dòng: 'ĐÁP ÁN CUỐI: <số>'."


def extract(t):
    m = re.search(r"ĐÁP\s*ÁN\s*CUỐI\s*[:：]\s*(.+)", t)
    seg = m.group(1) if m else t
    n = re.findall(r"-?\d+(?:\.\d+)?", seg.replace(",", ""))
    return n[-1] if n else None


def match(a, b):
    try:
        return abs(float(a) - float(b)) < 1e-6
    except (TypeError, ValueError):
        return str(a) == str(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--eval", default="out/eval_vi.jsonl")
    ap.add_argument("--bs", type=int, default=32)
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(a.model)
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype="bfloat16", device_map="auto")
    if a.adapter:
        model = PeftModel.from_pretrained(model, a.adapter)
    model.eval()

    rows = [json.loads(l) for l in open(a.eval, encoding="utf-8") if l.strip()]
    ok = 0
    for i in range(0, len(rows), a.bs):
        batch = rows[i:i + a.bs]
        prompts = [tok.apply_chat_template(
            [{"role": "system", "content": SYS}, {"role": "user", "content": r["question"]}],
            tokenize=False, add_generation_prompt=True) for r in batch]
        enc = tok(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(model.device)
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=320, do_sample=False, pad_token_id=tok.pad_token_id)
        gen = out[:, enc["input_ids"].shape[1]:]
        for j, r in enumerate(batch):
            if match(extract(tok.decode(gen[j], skip_special_tokens=True)), r["final_answer"]):
                ok += 1
        print(f"  ...{min(i + a.bs, len(rows))}/{len(rows)} xong", flush=True)

    tag = a.adapter or "BASE (zero-shot)"
    print(f"[{tag}]  Accuracy: {ok}/{len(rows)} = {100 * ok / len(rows):.1f}%", flush=True)


if __name__ == "__main__":
    main()
