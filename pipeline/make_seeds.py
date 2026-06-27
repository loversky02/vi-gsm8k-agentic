"""Tải GSM8K, lấy N bài làm seed (chỉ giữ đáp án số) -> seeds/gsm8k.jsonl"""
import json
import os
import re

from datasets import load_dataset

N = int(os.getenv("SEED_N", "40"))
ds = load_dataset("openai/gsm8k", "main", split="train")

os.makedirs("seeds", exist_ok=True)
out_path = "seeds/gsm8k.jsonl"
cnt = 0
with open(out_path, "w", encoding="utf-8") as f:
    for ex in ds:
        m = re.search(r"####\s*([\-\d,\.]+)", ex["answer"])
        if not m:
            continue
        ans = m.group(1).replace(",", "").strip()
        f.write(json.dumps({"question": ex["question"], "answer": ans}, ensure_ascii=False) + "\n")
        cnt += 1
        if cnt >= N:
            break

print(f"Đã ghi {cnt} seed GSM8K -> {out_path}")
