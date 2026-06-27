#!/bin/bash
# KHÔI PHỤC 2B: 5/6 ckpt đã xong (kể cả ours_7). Chỉ còn baseline_7 -> rồi eval + push.
# Chạy trong tmux (daemon độc lập SSH) để không chết khi session ngắt.
cd /workspace/cap
echo "[rest] bắt đầu $(date -u)" >> rest.log
if [ ! -f ckpt/baseline_7/adapter_model.safetensors ]; then
  echo "[rest] TRAIN baseline_7 ..." >> rest.log
  python train_sft.py --data out/baseline_vi.jsonl --out ckpt/baseline_7 --seed 7 >> rest.log 2>&1
  echo "[rest] baseline_7 xong $(date -u)" >> rest.log
fi
echo "[rest] EVAL (14 cấu hình) + PUSH model -> eval_results.txt ..." >> rest.log
bash eval_save.sh >> rest.log 2>&1
echo "[rest] ===== HOÀN TẤT $(date -u) =====" >> rest.log
