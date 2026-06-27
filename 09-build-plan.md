# 09 — Quyết định build & Kế hoạch MVP

[← 08 Chi phí](08-cost-estimate.md) · [Về README →](README.md)

> Chốt 2026-06-26. Hạ tầng: **2× H100**, ngân sách GPU **~1tr5** (~11h). Domain: **Toán**.

## 4 quyết định thiết kế (đã research)

| # | Quyết định | Chốt | Vì sao |
|---|---|---|---|
| Base model | SFT/GRPO | **Qwen3-4B-Instruct-2507** | #1–2 fine-tuning; multilingual (VN); thinking-mode toán (check Qwen3.5-4B nếu có) |
| Phạm vi | Loại toán | **GSM8K-level** (đáp án số) + tự tăng khó | Verify code chắc nhất |
| Cách sinh đề ⭐ | seed vs scratch | **SEED-BASED** | from-scratch dễ nhảm/trùng |
| Validation | tập vàng | VMLU-STEM + dịch ~300 GSM8K | xem [05 Q1](05-meta-optimizer.md) |

## Pipeline sinh đề (MetaMath + Evol-Instruct + persona)

1. **Seed** — GSM8K dịch sang tiếng Việt, giữ đáp án số.
2. **Bootstrap** (MetaMath) — Challenger viết lại đề từ nhiều góc nhìn.
3. **Evolve** (Evol-Instruct in-depth) — tăng độ khó có kiểm soát (thêm ràng buộc, nhiều bước).
4. **Persona** — gắn bối cảnh VN đa dạng (chợ, lúa, học phí…) → chống trùng + bản địa hoá.
5. **Filter** quality-diversity → verify code → giữ.

> Backup base model: **Phi-4-mini (3.8B)** rất mạnh MATH; **Gemma 3 4B** đa ngôn ngữ.

## Schema dataset

```json
{
  "id": "vi-gsm-000123",
  "question": "<đề toán tiếng Việt>",
  "chain_of_thought": "<lời giải từng bước, tiếng Việt>",
  "final_answer": "42",
  "verify": { "method": "code-exec", "passed": true },
  "difficulty": { "strong_pass": true, "weak_fail": true },
  "topic": "tỉ lệ phần trăm",
  "source_seed": "gsm8k:train:417",
  "lang": "vi"
}
```
Tối thiểu: `question + chain_of_thought + final_answer` (verify được). Còn lại là metadata.

## Kế hoạch MVP khít 1tr5 (2× H100 ~11h)

| Việc | Thời gian |
|---|---|
| SFT Qwen3-4B LoRA (~1.5k mẫu) | ~1h |
| GRPO (no-KL) | ~4h |
| Baseline (data dịch + self-instruct thường) | ~3h |
| Eval + benchmark + buffer | ~2h |
| **Tổng** | **~10h** ✅ |

- **Data MVP: ~1.5k mẫu giữ lại** (sinh ~3k, lọc ~50%). API ~$15–25 (tính riêng).
- ⚠️ **Meta-opt → giai đoạn 2** (với 1tr5 ưu tiên chứng minh vòng trong trước). Meta-opt chủ yếu tốn API.
- 💡 Nếu 1tr5 là **tổng** (gồm API): giảm còn ~1k mẫu, bỏ 1 baseline.

## Chứng minh chất lượng (so 3 cách trên cùng eval)

1. Data **dịch máy** (baseline a)
2. **Self-instruct thường** (baseline b)
3. **Agentic Self-Instruct của ta** ← kỳ vọng thắng

Eval trên: ViMath-gold (dịch) + VMLU-STEM.

**Nguồn:** [Qwen3-4B benchmark](https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/) ·
[OpenMathInstruct/MetaMath](https://arxiv.org/abs/2402.10176) ·
[WizardMath Evol-Instruct](https://arxiv.org/html/2308.09583v3) ·
[SPARQ](https://arxiv.org/pdf/2506.06499)
