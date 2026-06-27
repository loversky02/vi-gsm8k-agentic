"""SFT Qwen3-4B LoRA trên jsonl {question, chain_of_thought, final_answer}.
CHẠY TRÊN H100 (cần GPU). Ví dụ:
  python train_sft.py --data out/gsm8k_clean.jsonl --out ckpt/ours
  python train_sft.py --data out/baseline_vi.jsonl --out ckpt/baseline
"""
import argparse
import json

from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--epochs", type=float, default=3)
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(a.model)
    rows = [json.loads(l) for l in open(a.data, encoding="utf-8") if l.strip()]

    def fmt(r):
        msgs = [{"role": "user", "content": r["question"]},
                {"role": "assistant", "content": r["chain_of_thought"]}]
        return {"text": tok.apply_chat_template(msgs, tokenize=False)}

    ds = Dataset.from_list([fmt(r) for r in rows])

    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype="bfloat16", device_map="auto")
    peft = LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    cfg = SFTConfig(
        output_dir=a.out, num_train_epochs=a.epochs,
        per_device_train_batch_size=4, gradient_accumulation_steps=4,
        learning_rate=2e-4, bf16=True, logging_steps=10,
        save_strategy="epoch", max_length=2048, warmup_ratio=0.03,
    )
    trainer = SFTTrainer(model=model, train_dataset=ds, peft_config=peft, args=cfg)
    trainer.train()
    trainer.save_model(a.out)
    print(f"✓ SFT xong ({len(rows)} mẫu) -> {a.out}")


if __name__ == "__main__":
    main()
