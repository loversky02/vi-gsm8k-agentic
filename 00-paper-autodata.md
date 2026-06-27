# 00 — Paper Autodata (tóm tắt)

[← README](README.md) · Tiếp: [01 — Khả thi & scope →](01-feasibility-scope.md)

## Thông tin

- **Tên:** *Autodata: An agentic data scientist to create high quality synthetic data*
- **Nơi:** Meta FAIR (nhóm RAM — Reasoning, Alignment, and use of Memory)
- **Tác giả:** Ilia Kulikov, Chenxi Whitehouse, … **Jason Weston** (senior author) — 15 người
- **arXiv:** [2606.25996](https://arxiv.org/abs/2606.25996) — v1 24/06/2026, v2 25/06/2026
- ⚠️ **Không release code/dataset** → muốn làm lại phải **re-implement từ mô tả**.

## Ý tưởng một câu

Cho một **agent đóng vai data scientist** tự tạo dữ liệu train/eval chất lượng cao, rồi
**meta-optimize** (huấn luyện/tiến hóa) chính agent đó để nó tạo data ngày càng mạnh —
tức là **biến compute thành chất lượng dữ liệu**.

## Hai vòng lặp

### Vòng trong (inner loop) — "Agentic Self-Instruct"

Một **orchestrator** điều phối **4 subagent**:

| Subagent | Vai trò |
|----------|---------|
| **Challenger & Verifier** | Sinh đề (task) + đóng vai trọng tài chấm |
| **Strong solver** | Model mạnh — *phải giải đúng* (lời giải này thành nhãn/ground-truth) |
| **Weak solver** | Model yếu — *phải vật lộn* (dùng để đo độ khó) |
| (Verifier) | Chấm output theo tiêu chí/rubric |

Vòng lặp chạy đến khi mẫu data đạt **tiêu chí thành công + độ khó** đã định
(đề nào weak solver cũng giải được ⇒ quá dễ ⇒ loại).

### Vòng ngoài (outer loop) — Meta-optimization

Dùng **thuật toán tiến hóa (evolution)** để **đột biến chính cái "harness"** của agent —
gồm *code scaffolding + prompt + logic chấm*. Một "mutant harness" chỉ được giữ lại nếu
**điểm validation vượt hẳn (strictly exceeds) cha của nó**.

- Chạy **233 vòng**, **chấp nhận 126** mutant.
- Fitness = chính tiêu chí chất lượng của vòng trong.
- Chi tiết: xem [05-meta-optimizer.md](05-meta-optimizer.md).

## Bằng chứng "data tốt hơn" (phần training)

- Train **Qwen-3.5-4B** bằng **GRPO** (~1 epoch, batch 32, lr 1e-6).
- **Reward model = Kimi-K2.6**, chấm response theo rubric do agent sinh ra.
- So sánh: model train trên **Agentic Self-Instruct** > train trên **CoT Self-Instruct**,
  thắng trên **cả in-distribution lẫn out-of-distribution**.

## Domain họ thử nghiệm

- Computer science research tasks
- Legal reasoning
- Reasoning with mathematical objects (→ gần với hướng của ta nhất)

## Điểm cần nhớ cho dự án của ta

1. Phần **"agent tự đánh giá & sửa data"** = vòng trong, **chỉ là prompting + control flow**, không cần GPU.
2. Phần **meta-opt + GRPO** = vòng ngoài, là chỗ cần compute (ta có H100/H200 nên ổn).
3. **Kimi xuất hiện ở vai reward model**, không phải orchestrator — nhớ điều này (xem [04](04-orchestrator-code-vs-llm.md)).
