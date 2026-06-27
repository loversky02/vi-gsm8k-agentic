# Pipeline vòng trong — Agentic Self-Instruct (toán tiếng Việt)

Sinh dữ liệu instruction-tuning toán tiếng Việt theo sơ đồ ở [../10-pipeline-inner-loop.md](../docs/10-pipeline-inner-loop.md).

## Cấu trúc

```
config.py        # 4 vai trò -> model + tham số
prompts.py       # prompt tiếng Việt cho 4 subagent
schema.py        # dataclass Seed / Sample
llm_client.py    # gọi litellm (+ chế độ MOCK)
verifier.py      # trích & so khớp đáp án số (trọng tài chính)
subagents.py     # challenge / solve / verify_cot
orchestrator.py  # vòng lặp + GATE đo độ khó
run.py           # entry point
seeds/sample.jsonl
```

## 1. Chạy thử (MOCK — không cần API key)

```bash
cd pipeline
AUTODATA_MOCK=1 python3 run.py --n 5
```
→ kiểm tra logic GATE + verifier chạy đúng, in thống kê + 1 mẫu ví dụ.

## 2. Chạy thật

```bash
pip install -r requirements.txt
cp .env.example .env      # rồi điền API key (xem 2 cách A/B trong file)
python3 run.py --n 50 --out out/dataset.jsonl
```

⚠️ **Không dán API key vào chat.** Chỉ điền vào file `.env` (đã nên cho vào .gitignore).

## GATE (đo độ khó — xem orchestrator.py)

Giữ mẫu khi: **strong PASS ∧ weak FAIL ∧ verify PASS ∧ không trùng**.
Thống kê lý do loại in ra cuối mỗi lần chạy (too_easy / strong_mismatch / duplicate / bad_cot).

## Cần chỉnh trước khi chạy thật

- **Model ID** trong `config.py` / `.env` cho khớp tên hiện hành (vd `gpt-5.5`, `claude-opus-4-8`).
- Thay `seeds/sample.jsonl` bằng seed GSM8K thật (nhiều hơn) khi sinh số lượng lớn.
