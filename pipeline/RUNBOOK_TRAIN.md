# Giai đoạn 2 — Runbook training (chạy trên H100)

## Đã chuẩn bị sẵn (local, không cần GPU)

| File | Nội dung |
|------|----------|
| `out/gsm8k_clean.jsonl` | **Data của ta** — 1.465 mẫu agentic |
| `out/baseline_vi.jsonl` | **Baseline** — ~1.465 GSM8K dịch thẳng sang VN |
| `out/eval_vi.jsonl` | **Eval** — 200 GSM8K *test* dịch VN (held-out) |
| `train_sft.py` · `eval_model.py` | Script SFT + eval |
| `requirements_train.txt` | Deps cho training |

## Trên H100 (FPT)

```bash
# 1. Copy thư mục pipeline/ lên VM (scp / git / FPT notebook upload)
# 2. Cài deps
python -m venv .venv && . .venv/bin/activate
pip install -r requirements_train.txt

# 3. SFT × 2 (mỗi run ~1–2h)
python train_sft.py --data out/gsm8k_clean.jsonl  --out ckpt/ours
python train_sft.py --data out/baseline_vi.jsonl  --out ckpt/baseline

# 4. Eval × 3 (verify đáp án bằng code)
python eval_model.py                         # BASE zero-shot
python eval_model.py --adapter ckpt/ours     # data của ta
python eval_model.py --adapter ckpt/baseline # data dịch

# 5. So accuracy — KỲ VỌNG:  ours  >  baseline  >  base
```

## Chi phí & thời gian
- ~5h H100 (1× H100 ≈ $2.54/h) ≈ **~$13** — free credit FPT phủ.

## Nếu kết quả tốt (ours > baseline)
→ Thêm vào dataset card HF + (tùy chọn) chạy GRPO để đẩy thêm.

## Lưu ý
- Model: `Qwen/Qwen3-4B-Instruct-2507` (đổi `--model` nếu muốn bản khác).
- Cách đưa data lên VM gọn nhất: `huggingface-cli upload` 3 file lên 1 repo riêng rồi `wget`, hoặc scp trực tiếp.
