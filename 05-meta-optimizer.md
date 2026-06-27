# 05 — Meta-optimizer (Kimi tiến hóa harness)

[← 04 Orchestrator](04-orchestrator-code-vs-llm.md) · Tiếp: [06 — Câu hỏi mở →](06-open-questions.md)

> Đây là phần "ăn tiền" của Autodata — biến compute thành **data tốt hơn** một cách tự động.
> Cũng là phần khó nhất và paper mô tả ít nhất → cần nghiên cứu kỹ.

## Ý tưởng

- **Vòng trong** tối ưu *data* (sinh ra mẫu tốt).
- **Vòng ngoài (meta)** tối ưu *cỗ máy sinh data* — tức cái **harness** của agent.

Thay vì con người ngồi chỉnh prompt/logic, để **một agent (Kimi) tự đề xuất cải tiến harness**,
giữ lại cải tiến nào thực sự làm data tốt hơn.

## "Harness" gồm gì (đối tượng bị tiến hóa)

1. **Code scaffolding** — luồng điều phối, cách gọi 4 subagent, điều kiện keep/discard.
2. **Prompt** — prompt của challenger, solver, verifier.
3. **Eval logic** — tiêu chí chấm, rubric, ngưỡng độ khó.

→ Một "cá thể" (individual) trong quần thể tiến hóa = **một phiên bản đầy đủ của harness**.

## Cơ chế tiến hóa (evolution loop)

```
1. Có quần thể (population) các harness.
2. Chọn 1 harness cha → Kimi ĐỘT BIẾN nó (sửa code/prompt/eval) → tạo harness con (mutant).
3. Chạy harness con để sinh data → đo điểm trên VALIDATION set.
4. GATE: chỉ thêm con vào quần thể NẾU điểm validation > hẳn điểm của cha
   (strictly exceeds parent).
5. Lặp lại.
```

- Paper: **233 vòng**, **chấp nhận 126** (tỉ lệ ~54%).
- **Fitness = chính tiêu chí chất lượng của vòng trong** (data sinh ra đạt chuẩn tới đâu).
- Cổng "vượt hẳn cha" giúp quần thể chỉ đi lên, tránh trôi dạt (drift).

## Vai trò của Kimi ở đây

Kimi = **tác nhân đột biến (mutation operator)** thông minh: đọc harness hiện tại + tín hiệu lỗi,
rồi **đề xuất bản sửa có chủ đích** (không phải random mutation như GA cổ điển).
Đây đúng là *agentic reasoning* — chạy **ít lần**, mỗi lần đáng giá ⇒ trả tiền cho Kimi ở đây là hợp lý.

## ⚠️ Vì sao vòng trong PHẢI deterministic (liên hệ [04](04-orchestrator-code-vs-llm.md))

Meta-opt so sánh **con vs cha** bằng điểm validation. Nếu vòng trong (orchestrator per-item)
là LLM phi-deterministic, thì **chênh lệch điểm có thể chỉ là noise**, không phải do mutation tốt
⇒ meta-opt "học" nhầm. Giữ control flow là **code deterministic** → tín hiệu sạch → meta-opt mới đáng tin.

## Phần training để CHỨNG MINH (sau khi có data)

| Thành phần | Cấu hình paper |
|------------|----------------|
| Model train | Qwen-3.5-4B |
| Thuật toán | GRPO (~1 epoch) |
| Batch / LR | 32 / 1e-6 |
| Reward model | **Kimi-K2.6** (chấm theo rubric agent sinh) |
| So sánh | Agentic Self-Instruct **>** CoT Self-Instruct, thắng cả in-dist + OOD |

→ Với H100/H200, ta tái hiện được setup này (hoặc model nhỏ hơn cho MVP rồi scale lên).

## Câu trả lời cho các câu hỏi mở (đã research 2026-06-26)

### Q1 ✅ Validation set tiếng Việt
- **VMLU** (`anhdungitvn/vmlu_v1.5` trên HF) — 10.880 MCQ, 58 môn; **validation có đáp án** (test ẩn). Dùng **subset STEM/toán** làm gold.
- **Template HRM8K (Hàn)**: dịch GSM8K/MATH sang bản địa, **chỉ giữ bài đáp án SỐ** → tự dựng "ViMath-gold" ~200–500 bài tiếng Việt.
- ⚠️ Phải **held-out thật** (độc lập data sinh) + đáp án numeric (verify code).
- Nguồn: [HRM8K/Understand-Solve-Translate](https://arxiv.org/pdf/2501.02448)

### Q2 ✅ Fitness cho toán
3 trục (Quality-Diversity): **Difficulty · Correctness · Diversity**.
```
fitness = w1·verify_pass_rate   (code-exec đáp án số)
        + w2·difficulty         (strong_PASS ∧ weak_FAIL)
        + w3·diversity          (semantic spread, chống trùng)
        − penalty               (lỗi format / lộ đáp án / đề sai)
```
Đo trên held-out (Q1). ⚠️ **model collapse** nếu thiếu diversity guard. Nguồn: [Quality/Diversity/Complexity](https://arxiv.org/html/2412.02980v2)

### Q3 ✅ Framework tiến hóa
- **MVP → GEPA** (`pip install gepa` / `dspy.GEPA`): tiến hóa **prompt**, reflective + Pareto, hơn GRPO 20% với **35× ít rollout**, MATH 67→93%.
- **Nâng cao → `optimize_anything`** (GEPA team): tiến hóa **cả harness** (code+control-flow+prompt) — đúng tinh thần Autodata.
- Khác: ShinkaEvolve (cụm, sample-efficient), OpenEvolve (MAP-Elites).
- Nguồn: [GEPA](https://arxiv.org/pdf/2507.19457) · [optimize_anything](https://arxiv.org/html/2605.19633)

### Q4 ✅ Số vòng meta-opt cho MVP
Paper 233. GEPA mạnh với rất ít rollout → cải thiện dồn ở đầu rồi bão hòa.
→ **MVP: 20–30 vòng + early-stop theo plateau** (dừng khi vài vòng không vượt ε). Tốt hơn: đặt **budget rollout/tiền** thay vì số vòng cứng.

### Q5 ✅ Chống reward hacking
Verifier đơn lẻ **không đủ** (model lách: lộ đáp án sớm, format lạ, output rỗng). Guard kết hợp:
1. **Held-out khác training** (quan trọng nhất) — train cao mà held-out tụt = đang hack.
2. **Hybrid verifier**: code-exec + LLM judge + structural penalty.
3. **Semantic leak detection** (Sentence-BERT) chặn đề lộ đáp án.
4. **Diversity guard** chống collapse (đừng để over-exploit diversity).
5. **Monitor divergence** train vs held-reward + **human spot-check 5–10%**.
- Lợi thế toán: **đáp án numeric verify bằng code khó hack hơn LLM judge**. Nguồn: [LLMs Gaming Verifiers](https://arxiv.org/pdf/2604.15149)
