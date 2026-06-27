# Build-in-Public — vi-gsm8k-agentic

Ready-to-post copy for launch. Numbers below are the **multi-seed (3 seeds) result**, in-distribution
(GSM8K-test) + out-of-distribution (SVAMP-derived). Model is live on HF.

---

## 🧵 X / Twitter thread

**1/ (hook)**
> I built a Vietnamese grade-school math dataset where **4 AI agents generate, solve, and grade each other's work** — zero human labeling.
>
> It trains models that beat machine-translated data **+4.3% in-distribution and +6.6% out-of-distribution**.
>
> Fully open-source. Here's how 🧵

**2/ (the problem)**
> High-quality Vietnamese math data is scarce. Almost all of it is machine-translated from English — awkward phrasing, translation errors, answers that don't match the question.
>
> I wanted *native* Vietnamese problems, each verified correct.

**3/ (the idea)**
> The approach: **agentic self-instruct**, inspired by Meta's Autodata paper (arXiv:2606.25996).
>
> Instead of one LLM dumping data, a deterministic **code orchestrator** runs 4 specialized agents per sample — each one checks the others.

**4/ (the agents)**
> The 4 agents:
> 🎯 Challenger — writes a new VN problem + its answer
> 💪 Strong solver — must solve it (its steps become the label)
> 🥱 Weak solver — must FAIL (proves the problem is hard enough)
> ⚖️ Verifier — code-checks the answer + judges the reasoning

**5/ (the GATE)**
> A sample is kept ONLY if:
> ✅ Strong solves it correctly
> ✅ Weak fails it (so it's non-trivial)
> ✅ Code verifies the numeric answer
> ✅ It's not a duplicate
>
> Everything else is thrown away. Quality over quantity.

**6/ (build-in-public = share the mess)**
> The honest parts:
> • Google blocked my gateway's Gemini access (403) → direct API
> • Gemini ran out of credit mid-run → swapped to DeepSeek
> • GPT hit rate limits → checkpoint + resume
> • A bug parsed "3,75" as "375" — Vietnamese uses comma decimals! → fixed

**7/ (does it work?)**
> Fine-tuned Qwen3-4B (LoRA, 3 seeds) on it vs a same-size machine-translated baseline. Tested in-distribution (GSM8K-test) AND out-of-distribution (SVAMP-derived), answers code-verified:
>
> ⠀⠀⠀⠀⠀⠀In-dist⠀/⠀OOD
> Base⠀⠀⠀⠀75.0 / 88.0
> Translated⠀76.5 / 83.6
> Agentic⠀⠀⠀80.8 / 90.2 ✅

**8/ (the killer finding)**
> Look at OOD closely:
> • Agentic (90.2) > **base model** (88.0) → it *improves* generalization
> • Translated (83.6) < base (88.0) → it *hurts* it
>
> Machine-translated data teaches the model to memorize GSM8K-style phrasing and breaks on anything else. Agentic data doesn't.

**9/ (CTA + links)**
> Everything's open:
> 📊 Dataset: huggingface.co/datasets/vuongtsc/vi-gsm8k-agentic
> 🤖 Model: huggingface.co/vuongtsc/qwen3-4b-vi-gsm8k-agentic
> 💻 Code: github.com/loversky02/vi-gsm8k-agentic
>
> If you work on low-resource-language data, I'd love to hear how you do quality control 👇

---

## 💼 LinkedIn / blog version (long form)

**Title:** Teaching AI to write its own (better) training data — in Vietnamese

Most Vietnamese math datasets for fine-tuning LLMs are machine-translated from English. That
means awkward phrasing, subtle translation errors, and answers that don't always match the
question. I wanted something better: *native* Vietnamese problems, every one verified correct.

So I built an **agentic self-instruct pipeline** (inspired by Meta's Autodata paper), where a
deterministic code orchestrator coordinates four specialized LLM agents for every single sample:

- **Challenger** writes a brand-new Vietnamese word problem and its expected answer.
- **Strong solver** must solve it correctly — its step-by-step solution becomes the training label.
- **Weak solver** must *fail* — if an easy model gets it right, the problem is too trivial to keep.
- **Verifier** checks the numeric answer by code execution and judges the reasoning.

A sample survives only if **strong passes, weak fails, the answer verifies, and it's not a
duplicate.** Everything else is discarded. The orchestrator is plain code — deterministic and
debuggable — while the LLMs handle only what they're good at.

**Does it actually produce better data?** I fine-tuned Qwen3-4B (LoRA, 3 seeds) on this dataset and
on a same-size machine-translated baseline, then evaluated on held-out Vietnamese GSM8K-test
(in-distribution) and a SVAMP-derived out-of-distribution set:

| Model | Train data | In-dist | OOD |
|---|---|---|---|
| Base | — (zero-shot) | 75.0% | 88.0% |
| Baseline | machine-translated | 76.5% ±1.1 | 83.6% ±2.2 |
| **Ours** | **agentic self-instruct** | **80.8% ±1.2** | **90.2% ±0.4** |

The agentic data beat translated data by **+4.3 points in-distribution and +6.6 out-of-distribution**.
The most striking part is the OOD column: the agentic model *beats the base model* (90.2 vs 88.0),
while training on translated data actually drops *below* the base model (83.6). In other words,
machine-translated data quietly teaches the model to memorize GSM8K-style phrasing and damages its
ability to generalize — the agentic data preserves it. *How* you generate synthetic data matters as
much as how much.

Building in public also means sharing the friction: my gateway's Gemini access got blocked, credits
ran dry mid-run, GPT rate-limited me, and a sneaky bug parsed "3,75" as "375" because Vietnamese
writes decimals with a comma. All fixed, all part of the process.

Dataset, code, and the fine-tuned model are all open-source. Links in the comments. If you work on
low-resource-language data, I'd genuinely love to compare notes on quality control.

---

## ✅ Status checklist

- [x] **Multi-seed result** (3 seeds): in-dist 80.8% ±1.2 vs baseline 76.5% ±1.1; OOD 90.2% ±0.4 vs 83.6% ±2.2
- [x] **OOD finding** added (agentic > base on OOD; translated < base)
- [x] **Model URL** live: `vuongtsc/qwen3-4b-vi-gsm8k-agentic`
- [x] **README.md & DATASET_CARD.md** updated with multi-seed + OOD table
- [ ] **Scale dataset 1.5k → ~15k** — paused at 2,047 samples (waiting on a cheaper DeepSeek account). When done: bump the "1.5k" framing and `size_categories` (`1K<n<10K` → `10K<n<100K`), and note the challenger switched Gemini → deepseek-chat for the scaled portion.
- [ ] Attach a screenshot of the results table or a topic-distribution chart before posting — visual posts get far more engagement.

> Raw eval numbers per seed: `pipeline/out/eval_results_2b.txt`.
