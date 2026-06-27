"""Tải GSM8K: test (eval) + train (baseline), tránh trùng 40 seed đã dùng cho data agentic."""
import json
import os

from datasets import load_dataset

os.makedirs("seeds", exist_ok=True)

# Eval = GSM8K test (held-out hoàn toàn, không dùng để train)
test = list(load_dataset("openai/gsm8k", "main", split="test"))[:200]
with open("seeds/gsm8k_test200.jsonl", "w", encoding="utf-8") as f:
    for ex in test:
        f.write(json.dumps({"question": ex["question"], "answer": ex["answer"]}, ensure_ascii=False) + "\n")

# Baseline = 1465 bài GSM8K train (lấy lệch khỏi 40 seed đầu để công bằng)
train = list(load_dataset("openai/gsm8k", "main", split="train"))[100:100 + 1465]
with open("seeds/gsm8k_train1465.jsonl", "w", encoding="utf-8") as f:
    for ex in train:
        f.write(json.dumps({"question": ex["question"], "answer": ex["answer"]}, ensure_ascii=False) + "\n")

print(f"✓ eval test: {len(test)} -> seeds/gsm8k_test200.jsonl")
print(f"✓ baseline train: {len(train)} -> seeds/gsm8k_train1465.jsonl")
