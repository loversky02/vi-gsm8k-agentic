#!/bin/bash
# Chạy trọn giai đoạn 2 trên pod: cài deps -> SFT x2 -> eval x3.
set -e
cd /workspace/cap

echo "===== [1/6] Cài deps (torch đã có sẵn trong image) ====="
pip install -q transformers peft trl accelerate datasets

echo "===== [2/6] SFT trên DATA CỦA TA (agentic) ====="
python train_sft.py --data out/gsm8k_clean.jsonl --out ckpt/ours

echo "===== [3/6] SFT trên BASELINE (data dịch) ====="
python train_sft.py --data out/baseline_vi.jsonl --out ckpt/baseline

echo "===== [4/6] EVAL: BASE (zero-shot) ====="
python eval_model.py

echo "===== [5/6] EVAL: OURS ====="
python eval_model.py --adapter ckpt/ours

echo "===== [6/6] EVAL: BASELINE ====="
python eval_model.py --adapter ckpt/baseline

echo "===== HOÀN TẤT GIAI ĐOẠN 2 ====="
