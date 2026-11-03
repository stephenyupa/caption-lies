"""Generate synthetic financial charts with a known ground-truth trend.

Every chart shows one invented company and one metric. Half of the charts rise
and half fall, so a model cannot score well by always guessing one direction.
The image itself never states the trend in words; the title is neutral.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# Invented company names. None of these are meant to match a real firm.
COMPANIES = [
    "Norvale Systems", "Brightmere Foods", "Calderon Logistics", "Ostwick Energy",
    "Pellham Biotech", "Quarry Lane Retail", "Tessaline Media", "Wexford Robotics",
    "Halvorsen Marine", "Ambrose Textiles", "Kestrel Analytics", "Lumora Health",
    "Ridgefield Metals", "Sablewood Homes", "Corvane Telecom", "Duskhaven Gaming",
    "Ferncliff Pharma", "Gladstone Aerospace", "Ironbark Mining", "Juniper Coast Bank",
    "Marlowe Apparel", "Northgate Water", "Orchid Lane Cosmetics", "Pinecrest Software",
    "Redwater Chemicals", "Silverbrook Insurance", "Thornfield Motors", "Umberly Paper",
    "Valecrest Hotels", "Willowmere Farms", "Yarrow Semiconductors", "Zephyr Airlines",
]

# Each metric: how it is drawn, its unit, its time axis, and a plausible range.
METRICS = {
    "stock price": {
        "kind": "line", "unit": "$", "suffix": "", "periods": "months",
        "low": 20.0, "high": 180.0, "decimals": 2,
    },
    "quarterly revenue": {
        "kind": "bar", "unit": "$", "suffix": "M", "periods": "quarters",
        "low": 50.0, "high": 900.0, "decimals": 0,
    },
    "operating margin": {
        "kind": "line", "unit": "", "suffix": "%", "periods": "quarters",
        "low": 4.0, "high": 30.0, "decimals": 1,
    },
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
QUARTERS = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]

# Noise levels as a share of the total start-to-end change.
NOISE_LEVELS = {"easy": 0.08, "hard": 0.30}

LINE_COLOR = "#2a78d6"
BAR_COLOR = "#2a78d6"


@dataclass
class ChartMeta:
    chart_id: str
    image: str
    company: str
    metric: str
    kind: str
    direction: str  # "increase" or "decrease"
    start_label: str
    end_label: str
    start_value: float
    end_value: float
    pct_change: float
    noise: str
    values: list


def _series(rng: np.random.Generator, n: int, direction: str, spec: dict, noise: str) -> np.ndarray:
    """A trend from start to end plus noise, re-drawn until the trend is unambiguous."""
    low, high = spec["low"], spec["high"]
    for _ in range(1000):
        start = rng.uniform(low + 0.25 * (high - low), high - 0.25 * (high - low))
        change = rng.uniform(0.15, 0.60)  # 15% to 60% total move
        end = start * (1 + change) if direction == "increase" else start * (1 - change)
        trend = np.linspace(start, end, n)
        noise_sd = NOISE_LEVELS[noise] * abs(end - start)
        vals = trend + rng.normal(0, noise_sd, n)
        vals[0], vals[-1] = start, end
        vals = np.clip(vals, low * 0.3, None)
        slope = np.polyfit(np.arange(n), vals, 1)[0]
        # The end point and the overall fitted slope must both agree with the
        # label, so "up" or "down" is not a judgment call.
        ok_slope = slope > 0 if direction == "increase" else slope < 0
        ok_end = (vals[-1] > vals[0]) if direction == "increase" else (vals[-1] < vals[0])
        if ok_slope and ok_end:
            return np.round(vals, spec["decimals"])
    raise RuntimeError("Could not draw an unambiguous series")


def _draw(meta: ChartMeta, labels: list[str], spec: dict, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    x = np.arange(len(labels))
    vals = np.array(meta.values)
    if spec["kind"] == "bar":
        ax.bar(x, vals, color=BAR_COLOR, width=0.6)
    else:
        ax.plot(x, vals, color=LINE_COLOR, linewidth=2.2, marker="o", markersize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ylabel = meta.metric.capitalize()
    if spec["unit"] or spec["suffix"]:
        ylabel += f" ({spec['unit']}{spec['suffix']})".replace("($M)", "($ millions)")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(f"{meta.company}: {meta.metric}", fontsize=13, loc="left")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if spec["kind"] == "bar":
        ax.set_ylim(0, vals.max() * 1.15)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def generate(n: int, out_dir: Path, seed: int = 4463, noise: str = "easy") -> list[ChartMeta]:
    """Create n charts (balanced up/down, cycling metrics) and a metadata file."""
    out_dir = Path(out_dir)
    img_dir = out_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)

    directions = ["increase", "decrease"] * (n // 2) + (["increase"] if n % 2 else [])
    pyrng.shuffle(directions)
    metric_names = list(METRICS)

    metas = []
    for i in range(n):
        metric = metric_names[i % len(metric_names)]
        spec = METRICS[metric]
        labels = MONTHS if spec["periods"] == "months" else QUARTERS
        company = pyrng.choice(COMPANIES)
        vals = _series(rng, len(labels), directions[i], spec, noise)
        chart_id = f"c{i:04d}"
        image = f"images/{chart_id}.png"
        meta = ChartMeta(
            chart_id=chart_id,
            image=image,
            company=company,
            metric=metric,
            kind=spec["kind"],
            direction=directions[i],
            start_label=labels[0],
            end_label=labels[-1],
            start_value=float(vals[0]),
            end_value=float(vals[-1]),
            pct_change=round(float((vals[-1] - vals[0]) / vals[0] * 100), 1),
            noise=noise,
            values=[float(v) for v in vals],
        )
        _draw(meta, labels, spec, out_dir / image)
        metas.append(meta)

    with open(out_dir / "charts.jsonl", "w") as f:
        for m in metas:
            f.write(json.dumps(asdict(m)) + "\n")
    return metas


def load_charts(data_dir: Path) -> list[dict]:
    with open(Path(data_dir) / "charts.jsonl") as f:
        return [json.loads(line) for line in f if line.strip()]
