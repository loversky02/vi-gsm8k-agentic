#!/bin/bash
# Watcher: đợi train baseline_7 (train cuối) xong -> kill script gốc (output đổ /dev/null)
# -> chạy eval_save.sh (eval + push, LƯU FILE). Chạy detach (nohup) nên không chết theo session.
cd /workspace/cap
echo "[watcher] bắt đầu chờ, $(date -u)" >> watcher.log
# Đợi tới khi ckpt baseline_7 đã lưu xong VÀ không còn tiến trình train_sft nào chạy
while [ ! -f ckpt/baseline_7/adapter_model.safetensors ] || pgrep -f "train_sft.py" >/dev/null; do
  sleep 30
done
echo "[watcher] train xong lúc $(date -u) -> dừng script gốc, chạy eval_save" >> watcher.log
pkill -f run_phase2b.sh
pkill -f eval_model.py
sleep 3
bash eval_save.sh >> watcher.log 2>&1
echo "[watcher] HOÀN TẤT $(date -u)" >> watcher.log
