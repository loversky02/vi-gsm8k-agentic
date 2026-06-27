#!/bin/bash
# Giai đoạn 2B trên pod: multi-seed train (ours+baseline ×3 seed) + eval (in-dist + OOD) + push model.
cd /workspace/cap
pip install -q transformers peft trl accelerate datasets huggingface_hub
SEEDS="42 123 7"

for s in $SEEDS; do
  echo "### TRAIN ours_$s"
  python train_sft.py --data out/gsm8k_clean.jsonl --out ckpt/ours_$s --seed $s 2>&1 | tail -1
  echo "### TRAIN baseline_$s"
  python train_sft.py --data out/baseline_vi.jsonl --out ckpt/baseline_$s --seed $s 2>&1 | tail -1
done

echo "##### RESULTS #####"
echo -n "BASE | indist | "; python eval_model.py --eval out/eval_vi.jsonl 2>/dev/null | grep -a Accuracy
echo -n "BASE | ood    | "; python eval_model.py --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
for s in $SEEDS; do
  echo -n "OURS_$s | indist | ";     python eval_model.py --adapter ckpt/ours_$s     --eval out/eval_vi.jsonl     2>/dev/null | grep -a Accuracy
  echo -n "OURS_$s | ood    | ";     python eval_model.py --adapter ckpt/ours_$s     --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
  echo -n "BASELINE_$s | indist | "; python eval_model.py --adapter ckpt/baseline_$s --eval out/eval_vi.jsonl     2>/dev/null | grep -a Accuracy
  echo -n "BASELINE_$s | ood    | "; python eval_model.py --adapter ckpt/baseline_$s --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
done

echo "##### PUSH MODEL (ours seed 42) #####"
python push_model.py --adapter ckpt/ours_42 --repo vuongtsc/qwen3-4b-vi-gsm8k-agentic --acc "Trained on the agentic dataset; beats machine-translated baseline on held-out Vietnamese GSM8K-test (see dataset card for the full table)." 2>&1 | tail -2

echo "##### PHASE 2B DONE #####"
