# 01 — Khả thi & Scope

[← 00 Paper](00-paper-autodata.md) · Tiếp: [02 — Bối cảnh data VN →](02-vietnamese-data-landscape.md)

## Kết luận ngắn

✅ **Khả thi**, và là một capstone tốt. Với hạ tầng **H100/H200**, **bottleneck compute biến mất** —
có thể bám sát paper gần 1:1. Câu hỏi không còn là *"có đủ máy không"* mà là
*"scope tới đâu để vừa ấn tượng vừa làm xong trong thời gian capstone"*.

## Tách bài toán làm 2 phần

| Phần | Mô tả | Độ nặng |
|------|-------|---------|
| **Sinh data bằng agent** (vòng trong) | 4 subagent sinh → giải → chấm → lọc | Nhẹ — chỉ gọi API, không cần GPU |
| **Meta-opt + train chứng minh** (vòng ngoài) | Tiến hóa harness + GRPO train model | Nặng — cần GPU (ta có) |

## Cái gì giờ khả thi (nhờ GPU mạnh)

- **Full GRPO training thật** — train Qwen 4B–7B (hoặc lớn hơn) như paper, không phải SFT demo.
- **Meta-optimization đầy đủ** — chạy hàng trăm vòng tiến hóa harness (paper chạy 233).
- **Self-host được** nếu muốn — nhưng ta chọn **API cho nhẹ** (xem [03](03-architecture-4-subagents.md)).

## Bottleneck thật (GPU KHÔNG giải quyết được)

1. **Re-implement từ paper** — không có code gốc. Đây là phần tốn công nhất.
2. **Độ tin của verify toán** — phải dùng **ground-truth / code-execution**, không tin mỗi LLM-judge.
   Đây là vấn đề *thiết kế*, không phải *tài nguyên*.
3. **Thiết kế thí nghiệm chứng minh** — so sánh in-distribution + out-of-distribution cho chặt.

## Lộ trình MVP (1 người, cỡ capstone)

1. **Thu hẹp domain** — chọn *math word problems* HOẶC *logic puzzles*, đừng ôm cả hai.
2. **Re-implement vòng trong** (4 subagent qua API) → sinh ~1–3k mẫu tiếng Việt, verify bằng code-execution.
3. **Light meta-optimization** — tối ưu prompt/harness qua ~20–30 vòng trên validation set nhỏ.
4. **Proof of quality** — train (SFT/GRPO) một model, so với 2 baseline:
   (a) data dịch máy, (b) self-instruct thường. Đánh giá trên benchmark VN có sẵn.
5. **Open-source** — dataset + code + model card + bài viết lên HuggingFace.

## Rủi ro lớn nhất (ghi để khỏi quên)

- ⚠️ **Re-implement từ con số 0** — chiếm phần lớn thời gian.
- ⚠️ **Verify toán bằng LLM dễ sai âm thầm** → bắt buộc đáp án kiểm chứng được bằng máy.
- ⚠️ **Chi phí API** — loop 4 agent + refinement đốt token nhanh; dùng model rẻ + cache + giới hạn vòng lặp.
- ⚠️ **Bẫy "ablation hời hợt"** — phần chứng minh data tốt hơn rất dễ làm qua loa; cần ít nhất 1 so sánh đáng tin.
