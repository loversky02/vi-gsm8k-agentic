# 06 — Câu hỏi mở (cần chốt trước khi code)

[← 05 Meta-optimizer](05-meta-optimizer.md) · [Về README →](README.md)

> Danh sách quyết định đang treo. Chốt xong cái nào thì đánh dấu ✅ và ghi lựa chọn.

## 1. ✅ ĐÃ CHỐT — Domain: **TOÁN** (math word problems)

> Chốt 2026-06-26. Lý do: verify bằng code-execution (hợp RLVR), giữ giá trị tiếng Việt native,
> có benchmark VN (ViMath-Bench). Logic puzzle "knowledge-orthogonal" làm tiếng Việt mất ý nghĩa +
> transfer puzzle→math đang bị nghi ngờ (2026). **Logic = nhánh mở rộng giai đoạn 2.**
> Lưu ý: **SFT trước → GRPO sau** (research: SFT tăng tổng quát đa miền).

So sánh để tham khảo:

| | **Toán** (math word problems) | **Logic / tư duy** |
|---|---|---|
| Đáp án | Số / biểu thức | Dạng văn, nhiều lời giải đúng |
| Verify | **Dễ** — code-execution / so khớp số | **Khó** — phải LLM-judge + rubric |
| Rủi ro | Thấp hơn | Cao hơn (judge sai âm thầm) |
| Gợi ý | ✅ **Nên bắt đầu ở đây cho MVP** | Mở rộng sau khi pipeline ổn |

→ ✅ **Đã chốt: Toán** (xem khung trên).

## 2. 🟢 Cấu hình GPU — đã khuyến nghị → [07-training-config.md](07-training-config.md)

**Chốt:** Qwen ~4B, LoRA GRPO, **1× H200** cho MVP (scale 2–4× H200 nếu lên 7–14B).
Vẫn cần bạn xác nhận **số lượng H200** để biết trần model lớn nhất.

Câu hỏi gốc (giữ để tham khảo):

- Mấy GPU? Loại nào (H100 80GB / H200 141GB)?
- 1 con hay cụm đa GPU?
- Chạy liên tục được bao lâu?

→ Quyết định: train được model cỡ nào (4B? 7B? 32B? 70B?), self-host judge mạnh cỡ nào, meta-opt chạy bao nhiêu vòng.

## 3. ❓ Quy mô dataset mục tiêu

- MVP: ~1–3k mẫu. Bản full: 10k? 50k? 100k?
- Ảnh hưởng trực tiếp chi phí API (xem mục 4).

## 4. ❓ Ngân sách API

- Loop 4 agent + refinement đốt token nhanh.
- Ước tính: (số mẫu) × (số vòng refine) × (token/vòng) × (giá model).
- Giảm bằng: model rẻ ở weak solver, cache, giới hạn số vòng, batch API (thường -50%).

## 5. ✅ ĐÃ CHỐT — giữ cấu hình mặc định (Strong GPT-5.5 · Weak V4 Flash; KHÔNG nâng Weak→V4 Pro vì phá vai trò đo độ khó)

- Xem bảng ở [03-architecture-4-subagents.md](03-architecture-4-subagents.md).
- Mặc định "nhẹ nhàng": Gemini 3.1 Pro / GPT-5.5 / DeepSeek V4 Flash / Claude Opus 4.8.

## 6. ❓ Cách chứng minh "data tốt hơn" (chọn baseline)

- Baseline (a): data **dịch máy** (vd 5CD AI).
- Baseline (b): **self-instruct thường** (không agentic).
- Của ta: **agentic self-instruct** (+ meta-opt).
- Đánh giá trên: ViMath-Bench / VMLU / SEA-HELM (xem [02](02-vietnamese-data-landscape.md)).

## 7. ❓ Phạm vi meta-optimization cho MVP

- Có làm meta-opt ngay từ MVP, hay làm vòng trong cho chạy ổn trước rồi mới thêm meta-opt?
- Gợi ý: **vòng trong ổn trước → thêm meta-opt sau** (giảm rủi ro).

---

## Việc tiếp theo có thể làm
- [ ] Chốt mục 1 (toán/logic) + mục 2 (GPU) → tôi hiệu chỉnh lộ trình.
- [ ] Vẽ sơ đồ pipeline vòng trong (4 subagent + code orchestrator).
- [ ] Viết prompt mẫu cho challenger + verifier (tiếng Việt).
- [ ] Dựng skeleton code cho vòng trong.
