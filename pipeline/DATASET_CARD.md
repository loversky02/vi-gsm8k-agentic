---
license: mit
language:
- vi
task_categories:
- text-generation
tags:
- math
- instruction-tuning
- vietnamese
- synthetic
- chain-of-thought
- agentic-self-instruct
size_categories:
- 1K<n<10K
---

# Vietnamese Grade-School Math (Agentic Self-Instruct)

Native **Vietnamese** grade-school math word problems with **code-verified numeric answers** and
step-by-step chain-of-thought solutions. Generated with a 4-subagent *Agentic Self-Instruct* pipeline
(inspired by Meta's **Autodata**, arXiv:2606.25996) — **not machine-translated**.

## Why this dataset

Most Vietnamese math instruction data is machine-translated from English. This set is generated
*natively* in Vietnamese and quality-controlled by an agentic verification loop, every answer checked
by code execution.

## How it was built

A deterministic code orchestrator coordinates four LLM subagents per item:

| Subagent | Role |
|---|---|
| **Challenger** | Generate a new Vietnamese problem (seed → bootstrap → difficulty-evolve → Vietnamese persona) + expected numeric answer |
| **Strong solver** | Must solve correctly → its CoT becomes the label |
| **Weak solver** | Must struggle → used to measure difficulty |
| **Verifier** | Code-execution answer match (primary) + LLM judge on the reasoning (secondary) |

**GATE (kept only if):** `strong PASS ∧ weak FAIL ∧ verify PASS ∧ not duplicate`.

Seeds: GSM8K (MIT) — used only as difficulty inspiration; all released items are new derivative
Vietnamese problems.

## Schema

```json
{
  "id": "vi-gsm-000123",
  "question": "<Vietnamese problem>",
  "chain_of_thought": "<step-by-step solution, Vietnamese>",
  "final_answer": "42",
  "verify": {"method": "code-exec", "passed": true, "judge": "..."},
  "difficulty": {"strong_pass": true, "weak_fail": true},
  "topic": "...",
  "source_seed": "gsm8k:...",
  "lang": "vi"
}
```

## Cleaning

1.500 raw → **1.465** after a 3-step clean:
1. **Rule filter** — drop non-positive answers (logic errors).
2. **Leak filter** — drop items where the answer is pre-stated in the question.
3. **True-duplicate dedup** — drop only pairs that share *both* template (multilingual-MiniLM cosine ≥ 0.92) *and* the same final answer. "Same template, different numbers" pairs are **kept** as valid variants.

## Results — does it beat translated data?

Fine-tuned **Qwen3-4B-Instruct-2507** (LoRA SFT, 3 epochs) on this dataset vs a same-size
machine-translated GSM8K baseline, evaluated on **200 held-out Vietnamese GSM8K-test** problems
(answers verified by code):

| Model | Train data | Accuracy |
|---|---|---|
| Base | — (zero-shot) | 73.5% |
| Baseline | machine-translated GSM8K | 76.5% |
| **This dataset (agentic)** | agentic self-instruct | **81.0%** |

→ Training on this agentic dataset beats translated data by **+4.5 points** (and base by +7.5).
*Single-seed result; multi-seed + larger eval recommended for tighter statistical significance.*

## License

MIT. Derived from GSM8K (MIT). Generated content; verify before high-stakes use.

## Citation

If you use this dataset, please cite the Autodata paper (arXiv:2606.25996) and this repository.
