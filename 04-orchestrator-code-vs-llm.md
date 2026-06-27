# 04 — Orchestrator: Code thuần vs LLM (Kimi)

[← 03 Kiến trúc](03-architecture-4-subagents.md) · Tiếp: [05 — Meta-optimizer →](05-meta-optimizer.md)

> Câu hỏi gốc: "Kimi rất mạnh agentic orchestration, sao lại dùng code thuần?"
> Trả lời: **"orchestrator" có 2 nghĩa** — tôi nói code thuần là nhắm vào *một* nghĩa thôi.

## Kimi K2.6 mạnh thật

Open-source (Modified MIT), MoE 1T total / 32B active, context 262K, ra mắt **20/04/2026**.
**Agentic index 69.9**, điều phối tới **300 sub-agent / 4.000 bước**, chạy tự chủ **12 tiếng**,
tie GPT-5.5 về coding, **rẻ ~$0.67/$3.50** (cached $0.15 ở DeepInfra). → Phản xạ "Kimi = orchestrator tốt" **không sai**.

## "Orchestrator" — hai tầng

| | **Tầng vi mô** (điều phối *từng item*) | **Tầng vĩ mô** (chiến lược / meta) |
|---|---|---|
| Việc | challenger→2 solver→verifier→keep/discard | "đang thiếu loại đề nào, sinh thêm gì, chỉnh độ khó", đề xuất mutation harness |
| Tần suất | **Hàng vạn lần** (mỗi mẫu 1 lần) | **Ít lần** (mỗi batch / 233 vòng meta-opt) |
| Bản chất | Luồng **cố định**, rule rõ | **Mơ hồ, cần lập kế hoạch & phán đoán** |
| Nên dùng | ✅ **Code thuần** | ✅ **Kimi (LLM agentic)** |

"Code thuần" = nhắm vào **tầng vi mô**. **Tầng vĩ mô đúng là đất diễn của Kimi.**

## Vì sao vòng lặp per-item phải là code (3 lý do cứng)

1. **Tái lập (reproducibility).** Dataset open-source phải tái lập — cùng input ra cùng output để người khác audit. LLM orchestrator **phi-deterministic** (đổi theo prompt, temperature, version) ⇒ mất tính tái lập của chính bộ data bạn muốn tạo dấu ấn.
2. **Chi phí ×số item.** Nghiên cứu đối chứng (COBOL→Python, chỉ đổi chiến lược điều phối) cho thấy điều phối deterministic **giảm token tới 3,5×**, accuracy tương đương, ổn định hơn ở worst-case. Trả tiền cho LLM suy nghĩ ở mỗi item — trong khi `if/else` làm được — là đốt tiền ×vạn lần.
3. **Lỗi điều phối nguy hiểm hơn lỗi text.** LLM cầm control flow mà "quên" ràng buộc giữa chừng ⇒ **route sai / bỏ bước / gọi nhầm subagent**, không chỉ câu chữ xấu. Trong pipeline nhiều bước không validation, lỗi này *cộng dồn*.

## Điểm mấu chốt

> **Đừng để Kimi *chạy* orchestrator mỗi item. Hãy để Kimi *viết / cải tiến* orchestrator — rồi code đó chạy.**

Đây chính là tinh thần **meta-optimization** (xem [05](05-meta-optimizer.md)): meta-optimizer tiến hóa cái *harness* (code + prompt + eval logic). Nếu vòng lặp per-item là code deterministic ⇒ meta-opt đo được **tín hiệu sạch** (cải thiện thật, không nhiễu bởi tính ngẫu nhiên của orchestrator). Nếu vòng lặp là LLM phi-deterministic ⇒ noise lẫn vào, khó biết mutation nào thực sự tốt.

## Kimi đóng góp đúng nhất ở 3 chỗ (đều là phán đoán/vĩ mô)

- **Meta-optimizer** — đề xuất sửa code+prompt cho harness (reasoning phức tạp, chạy ~233 lần → rẻ).
- **Data-scientist chiến lược** — phân tích gap phân phối, lên kế hoạch sinh thêm (mỗi batch 1 lần).
- **Verifier / Judge** — Kimi tool-use mạnh + rẻ, có thể **gọi code execution** để verify toán → rất hợp.

> 📌 Đính chính: trong paper Autodata, **Kimi-K2.6 được dùng làm reward model** (chấm response theo rubric), **không phải** làm orchestrator điều phối.

## Mẫu hình chuẩn = plan-then-execute (hybrid)

```
Kimi lập kế hoạch (tầng vĩ mô, ÍT lần)
        ↓
Executor bằng CODE chạy vòng lặp (tầng vi mô, VẠN lần)
        ↓
LLM chỉ chen vào ở bước cần phán đoán ngôn ngữ
   (challenger sinh đề, verifier chấm)
```

**Nguồn:** [Kimi K2.6 benchmarks (DeepInfra)](https://deepinfra.com/blog/kimi-k2-6-api-benchmarks-latency-throughput-cost) ·
[Kimi K2.6 explained (Miraflow)](https://miraflow.ai/blog/kimi-k2-6-explained-moonshot-ai-open-source-model-ties-gpt-5-5-coding) ·
[Deterministic vs LLM orchestration — đối chứng (arXiv 2605.09894)](https://arxiv.org/html/2605.09894) ·
[Orchestration patterns (Genta)](https://genta.dev/resources/ai-agent-orchestration-patterns-llm-vs-code-driven)
