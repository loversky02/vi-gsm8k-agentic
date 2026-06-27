# 02 — Bối cảnh dữ liệu tiếng Việt & Định vị

[← 01 Khả thi](01-feasibility-scope.md) · Tiếp: [03 — Kiến trúc 4 subagent →](03-architecture-4-subagents.md)

## Sự thật phũ phàng

Câu "data chất lượng cao tiếng Việt còn hiếm" **không còn hoàn toàn đúng**. Đã có khá nhiều:

| Nguồn | Loại | Ghi chú |
|-------|------|---------|
| [ViMath-Bench / SiRC](https://aclanthology.org/2024.conll-1.20/) (CoNLL 2024) | Toán VN + phương pháp "Simple Reasoning with Code" | Bench toán VN lớn nhất; có code + dataset |
| [5CD AI Team](https://github.com/vndee/awsome-vietnamese-nlp) | Math Instruct + CoT (bản **dịch**) | Dịch từ tiếng Anh |
| [Stanford SAIL](https://ai.stanford.edu/blog/crossing-linguistic-horizon/) | 2 bộ reasoning VN (toán + synthetic) | Open-source |
| VinaLLaMA | Foundation model VN | Có data instruction VN |

## Gap thật sự nằm ở đâu

👉 **Phần lớn data hiện có là DỊCH MÁY từ tiếng Anh**, không phải sinh *native* tiếng Việt
có kiểm định chất lượng.

→ **Điểm bán hàng của ta:** dữ liệu tiếng Việt **native**, **sinh + kiểm định bằng agentic verification**,
**không phải bản dịch**. Đây mới là cái tạo dấu ấn trên HuggingFace — chứ không phải "lại một bản dịch nữa".

## Benchmark để đánh giá (dùng khi chứng minh chất lượng)

| Benchmark | Dùng cho |
|-----------|----------|
| **VLUE** | Vietnamese Language Understanding Evaluation (NLU) |
| **VMLU** | Vietnamese MMLU — kiến thức/đa lĩnh vực |
| **SEA-HELM** | [leaderboard](https://leaderboard.sea-lion.ai/) — chuẩn vùng Đông Nam Á (AI Singapore × Stanford CRFM) |
| **ViMath-Bench** | Toán tiếng Việt (từ SiRC) |
| **VMMU** | Multimodal VN (nếu mở rộng sang ảnh) |

> Lưu ý: benchmark tiếng Anh (MMLU, GPQA…) **không** phản ánh đúng năng lực tiếng Việt
> (thanh điệu, ngữ cảnh văn hóa). Phải dùng benchmark VN.

## Hệ quả cho thiết kế

- Ưu tiên **sinh đề native** (challenger nói tiếng Việt tự nhiên), không dịch.
- Giữ lại **metadata** (độ khó, lĩnh vực, lời giải từng bước) để dataset có giá trị cao hơn bản dịch trơn.
- Khi công bố, **so trực tiếp với data dịch** để làm nổi bật giá trị native + verified.
