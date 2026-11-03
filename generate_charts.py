"""Create the synthetic chart set.

Example:
    python generate_charts.py --n 200 --out data
"""

import argparse
from collections import Counter

from caption_lies.charts import NOISE_LEVELS, generate


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=200, help="number of charts (default 200)")
    p.add_argument("--out", default="data", help="output folder (default data/)")
    p.add_argument("--seed", type=int, default=4463, help="random seed, for reproducibility")
    p.add_argument("--noise", choices=list(NOISE_LEVELS), default="easy", help="how noisy each series is")
    args = p.parse_args()

    metas = generate(args.n, args.out, seed=args.seed, noise=args.noise)
    print(f"Wrote {len(metas)} charts to {args.out}/images and metadata to {args.out}/charts.jsonl")
    print("Directions:", dict(Counter(m.direction for m in metas)))
    print("Metrics:   ", dict(Counter(m.metric for m in metas)))


if __name__ == "__main__":
    main()
