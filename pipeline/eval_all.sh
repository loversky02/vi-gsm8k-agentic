#!/bin/bash
cd /workspace/cap
echo "===== EVAL BASE (zero-shot) ====="
python eval_model.py 2>&1 | grep -iE "Accuracy"
echo "===== EVAL OURS ====="
python eval_model.py --adapter ckpt/ours 2>&1 | grep -iE "Accuracy"
echo "===== EVAL BASELINE ====="
python eval_model.py --adapter ckpt/baseline 2>&1 | grep -iE "Accuracy"
echo "===== EVAL DONE ====="
