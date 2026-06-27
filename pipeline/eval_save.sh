#!/bin/bash
# Eval đa-seed (ours/baseline × 42,123,7) trên in-dist + OOD, LƯU KẾT QUẢ RA FILE.
# Chống mất số liệu khi session SSH ngắt (output run_phase2b.sh gốc đổ vào /dev/null).
cd /workspace/cap
OUT=eval_results.txt
SEEDS="42 123 7"
{
  echo "===== RESULTS multi-seed ($(date -u)) ====="
  printf "BASE | indist | ";  python eval_model.py --eval out/eval_vi.jsonl     2>/dev/null | grep -a Accuracy
  printf "BASE | ood    | ";  python eval_model.py --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
  for s in $SEEDS; do
    printf "OURS_%s | indist | "     "$s"; python eval_model.py --adapter ckpt/ours_$s     --eval out/eval_vi.jsonl     2>/dev/null | grep -a Accuracy
    printf "OURS_%s | ood    | "     "$s"; python eval_model.py --adapter ckpt/ours_$s     --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
    printf "BASELINE_%s | indist | " "$s"; python eval_model.py --adapter ckpt/baseline_$s --eval out/eval_vi.jsonl     2>/dev/null | grep -a Accuracy
    printf "BASELINE_%s | ood    | " "$s"; python eval_model.py --adapter ckpt/baseline_$s --eval out/eval_ood_vi.jsonl 2>/dev/null | grep -a Accuracy
  done
  echo "===== PUSH MODEL (ours_42) ====="
  python push_model.py --adapter ckpt/ours_42 --repo vuongtsc/qwen3-4b-vi-gsm8k-agentic \
    --acc "Beats machine-translated baseline on held-out Vietnamese GSM8K-test (multi-seed; see repo)." 2>&1 | tail -2
  echo "===== PHASE 2B DONE ====="
} >> "$OUT" 2>&1
echo "✓ eval_save xong -> $OUT"
