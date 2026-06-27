"""Entry point. Chạy thử (MOCK):  AUTODATA_MOCK=1 python3 run.py --n 5
Chạy thật:  điền .env rồi  python3 run.py --n 50 --out out/dataset.jsonl
"""
import argparse
import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from schema import Seed
from orchestrator import generate, _norm_q


def load_seeds(path):
    seeds = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                seeds.append(Seed(d["question"], str(d["answer"])))
    return seeds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5, help="số mẫu cần giữ")
    ap.add_argument("--seeds", default="seeds/sample.jsonl")
    ap.add_argument("--out", default="out/dataset.jsonl")
    ap.add_argument("--no-judge", action="store_true", help="tắt LLM judge phụ (chỉ verify bằng code)")
    ap.add_argument("--workers", type=int, default=1, help="số luồng song song (vd 12 để scale)")
    ap.add_argument("--resume", action="store_true", help="đọc out cũ, bù cho đủ n (append + dedup)")
    a = ap.parse_args()

    seeds = load_seeds(a.seeds)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)

    initial_seen, n_to_gen, append, offset = None, a.n, False, 0
    if a.resume and os.path.exists(a.out):
        existing = [json.loads(line) for line in open(a.out, encoding="utf-8") if line.strip()]
        initial_seen = set(_norm_q(e["question"]) for e in existing)
        offset = len(existing)
        n_to_gen = max(0, a.n - len(existing))
        append = True
        print(f"Resume: đã có {len(existing)} mẫu, cần sinh thêm {n_to_gen}")

    kept, stats = generate(seeds, n_to_gen, use_judge=not a.no_judge, workers=a.workers,
                           out_path=a.out, initial_seen=initial_seen, append=append, idx_offset=offset)

    total = offset + len(kept)
    print(f"Giữ thêm {len(kept)} (tổng {total}/{a.n})  ->  {a.out}")
    print("Thống kê GATE:", stats)
    if kept:
        print("\nVí dụ 1 mẫu:")
        print(json.dumps(kept[0].to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
