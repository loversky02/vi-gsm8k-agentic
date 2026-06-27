# 07 — Cấu hình Training & GPU (đã khuyến nghị)

[← 06 Câu hỏi mở](06-open-questions.md) · [Về README →](../README.md)

> Chốt ngày 2026-06-26. Số liệu tổng hợp từ research, mang tính ước lượng — phụ thuộc framework & cách train.

## Nguyên tắc: RL tốn VRAM hơn SFT nhiều

GRPO (RL) cần thêm bộ nhớ cho **rollout generation + policy gradient + reward** → nặng hơn SFT.
Tham chiếu thô: full fine-tune ~**16GB/1B** (FP16, gồm gradient + optimizer state); inference chỉ ~2GB/1B.

## Bảng scaling (GRPO)

| Cỡ model | Cách train | GPU cần (ước lượng) |
|----------|-----------|---------------------|
| 1–3B | LoRA GRPO | **1× 80GB** (hoặc ~11GB cho ≤3B trên GPU consumer) |
| 3B | Full-param GRPO | ~**4× H200 (141GB)** (paper Rank-GRPO) |
| 7–14B | LoRA RL | **2–4× 80GB** |
| 32B+ | Full-param RL | 4–8 GPU, **>600GB** tổng |

## H100 vs H200 → **chọn H200**

| | H100 | H200 |
|---|------|------|
| VRAM | 80GB | **141GB** |
| Bandwidth | 3.35 TB/s | **4.8 TB/s (+43%)** |
| Hệ quả | — | Chứa rollout+KV cache thoải mái; **rollout nhanh hơn** (khâu ngốn thời gian nhất của GRPO) |

→ GRPO nghẽn ở sinh rollout, nên **bandwidth + VRAM của H200 ăn đứt** cho việc này.

## Cấu hình chốt (sweet spot capstone)

```
Model train   = Qwen ~4B   (bám paper Autodata)
Phương pháp   = LoRA GRPO
GPU (MVP)     = 1× H100      → đủ cho 4B LoRA, rẻ hơn H200 ~2,6× (xem 08)
GPU (scale)   = 2× H100      → tách rollout/train, GRPO nhanh ~2×, rẻ hơn 1×H200 (xem 08)
GPU (lớn hơn) = 1× H200 (>80GB liền) | 4×+ (14B+ / full-param)
Rollout       = vLLM (PagedAttention)
Reward model  = Kimi-K2.6 qua API + code-execution (KHÔNG tốn GPU)
Pipeline      = SFT → GRPO   (SFT trước giúp tổng quát đa miền)
Framework gợi ý = TRL hoặc verl (verl scale RL tốt)
```

## Vì sao "SFT → GRPO" chứ không GRPO thẳng

Ablation trong research: **SFT trước RLVR tăng mạnh khả năng tổng quát đa miền** + bền với biến đổi
template/ngôn ngữ. Với tiếng Việt (ít data, nhiều biến thể) → bước SFT càng đáng giá.

## Còn chờ xác nhận

- [ ] **Số lượng H200** thực có (1 / 2 / 4 / cụm) → quyết định **trần model lớn nhất** train được.
  *(MVP 4B không bị chặn — chạy được trên 1 con.)*

**Nguồn:** [LLM VRAM Requirements 2026 (VRLA)](https://vrlatech.com/llm-vram-requirements-2026/) ·
[VRAM cho 7B/33B/70B (DatabaseMart)](https://www.databasemart.com/blog/how-much-vram-do-you-need-for-7-70b-llm) ·
[Rank-GRPO (arXiv)](https://arxiv.org/pdf/2510.20150) ·
[GPU memory for LLMs (Spheron)](https://www.spheron.network/blog/gpu-memory-requirements-llm/)
