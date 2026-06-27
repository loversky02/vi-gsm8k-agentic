# 08 — Ước tính chi phí (thuê GPU FPT AI Factory)

[← 07 Training config](07-training-config.md) · [Về README →](../README.md)

> Dựa trên bảng giá FPT AI Factory user chụp ngày 2026-06-26. Quy đổi ~26.000 VND/$ (kiểm lại tỉ giá khi tính thật).
> Mọi con số là **ước lượng dải rộng** — phụ thuộc số mẫu, số vòng refine, số run thử nghiệm.

## Hai nguồn chi phí TÁCH BIỆT

1. **GPU thuê (FPT)** — chỉ cho **training** (SFT + GRPO). Tính theo giờ.
2. **API sinh data** — vòng trong 4 subagent (Gemini/GPT/DeepSeek). Tính theo token. **Không** qua FPT.

## Bảng giá FPT (từ ảnh, /giờ)

| Cấu hình | VND/h | ≈ USD/h | Region |
|---|---|---|---|
| **1× H100 80GB** | 67.924 | ~$2.6 | SEA |
| 2× H100 | 135.849 | ~$5.2 | SEA |
| 4× H100 | 271.698 | ~$10.4 | SEA |
| 8× H100 | 543.397 | ~$20.9 | SEA |
| **1× H200 141GB** | 176.497 | ~$6.8 | Japan |
| 2× H200 | 352.994 | ~$13.6 | Japan |
| 4× H200 | 705.988 | ~$27.2 | Japan |
| 8× H200 | 1.411.976 | ~$54.3 | Japan |
| 1× B300 288GB | 184.927 | ~$7.1 | SEA |
| 8× B300 | 1.479.419 | ~$56.9 | SEA |

## 3 insight tiết kiệm

1. 🎯 **MVP 4B LoRA → 1× H100 đủ**, rẻ hơn H200 **~2,6×**. H200 chỉ cần khi 7B+/full-param/context dài.
2. 🎯 **Domain Toán (đã chốt) → reward = code-execution MIỄN PHÍ.** Không tốn Kimi API cho verify đáp án số.
3. 💡 **B300 (~$7.1) ≈ H200 (~$6.8)** nhưng 288GB + Blackwell mạnh hơn → đáng cân nhắc khi train lớn (cần check framework hỗ trợ Blackwell).

## 2× H100 vs 1× H200 (bước scale)

| | **2× H100 80GB** | **1× H200 141GB** |
|---|---|---|
| Giá/h | **135.849 VND (~$5.2)** | 176.497 VND (~$6.8) |
| VRAM tổng | **160GB** (2×80, rời) | 141GB (liền 1 card) |
| Region | **SEA** (gần VN) | Japan |
| Hợp nhất cho | **GRPO tách rollout/train** (1 card sinh, 1 card train) | Model đơn cần **>80GB liền mạch** / 7B full-param |

→ Cho GRPO của ta, **2× H100 thường thắng**: rẻ hơn ~23%, tổng VRAM nhiều hơn, đúng kiểu "1 card rollout + 1 card train". Chọn H200 chỉ khi cần một model chiếm >80GB trên *một* card.

> 💡 Mẹo: 2× H100 đắt gấp đôi/giờ NHƯNG nếu tách rollout/train làm GRPO nhanh ~2× → **tổng tiền mỗi run ≈ ngang 1× H100**. *"Đắt theo giờ, không hẳn đắt theo run."*

## Lộ trình GPU theo giai đoạn

| Giai đoạn | GPU | Vì sao |
|---|---|---|
| MVP (4B LoRA, ít run) | **1× H100** | Đủ + rẻ nhất + setup đơn giản |
| Nhiều GRPO run / ablation | **2× H100** | Tách rollout/train → nhanh ~2× |
| 7B full-param / model >80GB liền | 1× H200 / 4×+ | Cần VRAM liền mạch |

## Scaling số GPU: đổi tiền lấy tốc độ (KHÔNG tiết kiệm cả hai)

Giá thuê **tuyến tính** theo số GPU, nhưng tốc độ **không** (hiệu suất giảm dần do overhead giao tiếp — Amdahl).
Minh hoạ 1 run GRPO 4B (giả định 20h trên 1×H100 — *cần benchmark thật để chốt*):

| GPU | Speedup (ước) | Thời gian | Tổng tiền | So với 1× |
|---|---|---|---|---|
| 1× H100 | 1,0× | 20h | ~1,36tr | mốc |
| 2× H100 | ~1,8–2,0× | 10–11h | ~1,36–1,51tr | **≈ ngang** (GRPO tách rollout/train) |
| 4× H100 | ~3,0× | 6,7h | ~1,82tr | +34% tiền, nhanh 3× |
| 8× H100 | ~4,5× | 4,4h | ~2,39tr | +76% tiền, nhanh 4,5× |

→ **Thời gian giảm, tổng tiền tăng dần.** Mua tốc độ bằng tiền, không tiết kiệm cả hai.
Model 4B quá nhỏ → 8 GPU hiệu suất ~56% = **lãng phí**. Sweet spot = **1–2 GPU**.
(H100 SXM có NVLink → scaling tốt hơn loại PCIe.)

### So sánh nhanh các option cho **1 run 4B** (ước lượng tương đối, base ~8h/1×H100)

| Option | Thời gian | Tiền 1 run | Nhận xét |
|---|---|---|---|
| 1× H100 | ~8h | ~543k | Rẻ nhất — MVP |
| **2× H100** | ~4,4h | ~598k | 🏆 Sweet spot |
| 4× H100 | ~2,6h | ~706k | Nhanh, vẫn rẻ |
| 8× H100 | ~1,8h | ~978k | Nhanh nhất, hiệu suất ~56% |
| 1× H200 | ~5,7h | ~1.006k | ❌ Đắt hơn mà chậm hơn 2×H100 |
| 2× H200 | ~3,2h | ~1.130k | ❌ Đắt gần 2× so 2×H100 |
| 4× H200 | ~1,8h | ~1.271k | ❌ = tốc độ 8×H100 nhưng đắt hơn |

> 🔑 **4× H100 nhanh hơn VÀ rẻ hơn 2× H200** — với 4B chỉ mua compute, H100 rẻ hơn/đồng. **H200 chỉ đáng khi model cần >80GB VRAM trên 1 card** (13B+ full-param / inference model lớn). Cho 4B MVP: **dùng H100, bỏ qua H200.**

> ⚠️ "Thời gian chờ" tổng gồm 3 phần — thêm GPU **chỉ** rút ngắn phần train:
> - **Sinh data (API)** → tăng tốc bằng *concurrency API*, không phải GPU (rẻ).
> - **Train (GPU)** → số GPU, không tuyến tính (bảng trên).
> - **Meta-opt** → song song hoá các vòng đánh giá.

> 💡 Giảm thời gian RẺ hơn thêm GPU: **LoRA**, **GRPO no-KL** (bỏ ref model), tăng batch rollout, giảm dataset MVP — miễn phí mà cắt nhiều giờ.

## Ước tính tổng

| Kịch bản | GPU thuê | API sinh data | **Tổng** |
|---|---|---|---|
| **MVP** (4B LoRA, ~3–5k mẫu, 1×H100 ~20–50h) | 1,4–3,4tr (~$52–131) | 0,8–3,9tr (~$30–150) | **~2–7tr VND (~$80–280)** |
| **Full** (paper-scale + ablation, ~7B, ~100–250h) | 10–35tr (~$390–1360) | 8–39tr (~$300–1500) | **~18–74tr VND (~$700–2800)** |

## 🎁 Free credit — MVP gần như $0

FPT AI Factory tặng **$100 credit cho tài khoản mới**. Giá USD: 1×H100 (SEA) **$2.54/h**, 2×H100 **$5.08/h**, 1×H200 (Japan) $6.60/h, 2×H200 $13.20/h.

→ MVP ~10h trên **2×H100 = ~$51** → **nằm gọn trong $100, dư ~$49** cho ablation/meta-opt nhẹ. Phần GPU train MVP coi như **miễn phí**. Chỉ còn **API sinh data ~$15–25** trả ngoài (model bên thứ 3).

⚠️ Dùng **1 tài khoản hợp lệ** (đúng mục đích free-trial). Multi-account farming vi phạm ToS → rủi ro khóa tài khoản + mất data; không cần thiết vì $100 đã đủ. Check **hạn dùng credit** + GPU/region áp dụng.

## Công thức tự tính

```
Chi phí GPU  = (số giờ train) × (giá/h theo cấu hình)
Chi phí API  = (số mẫu sinh, gồm bị loại) × (token/mẫu) × (giá blended/token)

Mốc nhanh: 10h H100 ≈ 679k VND (~$26)
GRPO ngốn thời gian chủ yếu ở khâu sinh rollout.
```

## ⚠️ Lưu ý vận hành

- **Total Balance đang $0** → nạp tiền trước khi chạy.
- **Storage = local NVMe** → tắt VM có thể **mất data**. Lưu checkpoint + dataset ra Data Hub / HuggingFace ngay sau mỗi run.
- Tính tiền theo **giờ VM bật** → tắt khi không train; đừng để VM chạy không.
- Region: H200 ở **Japan**, H100/B300 ở **SEA** → cân nhắc latency nếu kéo data qua lại.
