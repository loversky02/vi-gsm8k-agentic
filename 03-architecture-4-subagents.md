# 03 — Kiến trúc 4 subagent & Chọn model API

[← 02 Bối cảnh VN](02-vietnamese-data-landscape.md) · Tiếp: [04 — Orchestrator code vs LLM →](04-orchestrator-code-vs-llm.md)

> Quyết định: dùng **API** cho gọn (không vận hành cụm). Training thì dùng GPU nhà.
> Số liệu giá tính tới **06/2026** — biến động nhanh, luôn check lại rate card trước khi chốt.

## Map 4 vai trò → model

| Vai trò | Yêu cầu cốt lõi | Đề xuất chính | Bản tiết kiệm | Giá (in/out /1M tok) |
|---|---|---|---|---|
| **1. Challenger** (sinh đề VN) | Tiếng Việt tự nhiên + đa dạng + đủ khó | **Gemini 3.1 Pro** | Qwen 3.7 Max | $2 / $12 · (~$1.25) |
| **2. Strong solver** (tạo lời giải = ground-truth) | Math/reasoning mạnh **nhất** | **GPT-5.5** | DeepSeek V4 Pro | $5 / $30 · (rẻ hơn ~10×) |
| **3. Weak solver** (đo độ khó) | Cố tình **yếu hơn** + rẻ + nhanh | **DeepSeek V4 Flash** | Gemini 3.1 Flash-Lite | $0.14 / $0.28 · $0.10 / $0.40 |
| **4. Verifier / Judge** (chấm) | Cẩn thận + **khác họ** solver + hiểu VN | **Claude Opus 4.8** | Gemini 3.1 Pro | $5 / $25 · $2 / $12 |

### Cấu hình "nhẹ nhàng" mặc định
4 họ khác nhau, chỉ 1 chỗ đắt:

```
Challenger  = Gemini 3.1 Pro
Strong      = GPT-5.5         (muốn cắt tiền → DeepSeek V4 Pro)
Weak        = DeepSeek V4 Flash
Verifier    = Claude Opus 4.8
Orchestrator= CODE (không phải model — xem file 04)
```

## 5 nguyên tắc / bẫy (quan trọng hơn việc chọn model)

1. **Verifier ≠ Strong solver (phải chéo họ).** Cùng model ⇒ *self-preference bias* (thiên vị lời giải của chính nó) ⇒ điểm chấm ảo.
2. **Weak solver phải thật sự yếu.** Mục đích là tạo **gradient độ khó**: đề nào weak cũng giải được ⇒ quá dễ ⇒ loại. Đừng phí model mạnh, cũng đừng vô tình chọn model gần ngang strong.
3. **Toán có đáp án ⇒ trọng tài chính là code-execution / so khớp đáp án số, KHÔNG phải LLM-judge.** LLM judge sai âm thầm trên toán rất nhiều. Đáp án kiểm chứng được là gốc; LLM judge chỉ là lớp phụ (chấm cách trình bày, lời giải có hợp lý không). **GPU mạnh không cứu được điểm này.**
4. **Dồn "ngân sách tiếng Việt" vào Challenger + Verifier.** Đây là 2 chỗ ngôn ngữ thực sự quan trọng. Solver ưu tiên reasoning — vẫn giải đúng dù tiếng Việt không hoàn hảo.
5. **Giá biến động + lưu ý tokenizer.** Opus từ 4.7+ dùng tokenizer mới, có thể sinh **+35% token** cho cùng văn bản ⇒ chi phí thực cao hơn bảng giá.

## Bảng giá tham khảo (06/2026, in/out per 1M tok)

| Model | Giá | Ghi chú |
|-------|-----|---------|
| GPT-5.5 | $5 / $30 | ~tuyệt đối trên AIME 2026; $0.50 cached input |
| Claude Opus 4.8 | $5 / $25 | tokenizer mới +~35% token |
| Gemini 3.1 Pro | $2 / $12 | tăng $4/$18 khi >200K tok |
| Gemini 3 Flash | $0.50 / $3 | rẻ, nhanh |
| Gemini 3.1 Flash-Lite | $0.10 / $0.40 | một trong các API rẻ nhất |
| DeepSeek V4 Flash | $0.14 / $0.28 | cached $0.0028; context 1M |
| DeepSeek V4 (base) | ~$0.435 / $0.87 | gần frontier, rẻ |
| Qwen 3.7 Max | ~$1.25 /M | rẻ nhất top-10; **#1 tiếng Việt SEA-HELM** |

## Ghi chú tiếng Việt (từ research)

- **Qwen** dẫn đầu bảng **text** SEA-HELM cho tiếng Việt (điểm top ~65).
- **Gemini 2.5-Pro** mạnh ở **Vision/OCR** tiếng Việt.
- **Claude 4.6 Sonnet** & **GPT-5.4** dẫn đầu **dịch** sang tiếng Việt.

**Nguồn:** [LLM Leaderboard 2026](https://www.clickrank.ai/llm-leaderboard/) ·
[Chinese/open models (BenchLM)](https://benchlm.ai/blog/posts/best-chinese-llm) ·
[SEA-HELM](https://leaderboard.sea-lion.ai/) ·
[Open LLM for Vietnamese](https://www.siliconflow.com/articles/en/best-open-source-LLM-for-Vietnamese) ·
[API pricing (BenchLM)](https://benchlm.ai/llm-pricing) ·
[API pricing Jun 2026 (DevTk)](https://devtk.ai/en/blog/ai-api-pricing-comparison-2026/)
