"""Push dataset jsonl lên HuggingFace Hub + dataset card. Cần HF_TOKEN trong .env + --repo.

Ví dụ:  python3 push_hf.py --data out/gsm8k_1500.jsonl --repo yourname/vi-gsm-agentic
"""
import argparse
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/gsm8k_200.jsonl")
    ap.add_argument("--repo", required=True, help="vd: yourname/vi-gsm-agentic")
    ap.add_argument("--private", action="store_true")
    ap.add_argument("--card", default="DATASET_CARD.md")
    a = ap.parse_args()

    token = os.getenv("HF_TOKEN")
    if token:
        token = token.encode("ascii", "ignore").decode().strip()  # phòng ký tự ẩn khi paste
    if not token:
        print("Thiếu HF_TOKEN trong .env (lấy tại huggingface.co/settings/tokens, quyền write)")
        return

    from datasets import load_dataset
    ds = load_dataset("json", data_files=a.data, split="train")
    ds.push_to_hub(a.repo, private=a.private, token=token)

    if os.path.exists(a.card):
        from huggingface_hub import HfApi
        HfApi(token=token).upload_file(
            path_or_fileobj=a.card, path_in_repo="README.md",
            repo_id=a.repo, repo_type="dataset",
        )
    print(f"Đã push {len(ds)} mẫu -> https://huggingface.co/datasets/{a.repo}")


if __name__ == "__main__":
    main()
