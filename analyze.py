"""Score the raw replies and write tables and figures.

Reads every results/raw/*.jsonl file and writes:
    results/scored.csv          one row per reply, with the parsed answer
    results/summary.csv         one row per model x condition
    results/summary.md          the same table in Markdown, ready to paste
    results/figures/*.png       accuracy and flip-rate charts

Metrics:
    accuracy       share of parsed answers that match the chart
    follow_rate    share of parsed answers that match the claim
    flip_rate      among charts the model read correctly with no claim,
                   the share it switched to the claim's direction. This is the
                   cleanest measure of text overriding vision, because it
                   leaves out charts the model could not read in the first place.
    conflict_rate  among correct answers in a claim condition, the share whose
                   explanation points out the disagreement (keyword heuristic)
    own_desc_acc   self_caption only: share of the model's own first-step
                   descriptions whose direction matches the chart (keyword
                   heuristic; hand-check a sample)

Example:
    python analyze.py                       # real runs in results/raw
    python analyze.py --raw results/mock/raw --out results/mock
"""

import argparse
import re
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from caption_lies.conditions import CONDITIONS, NO_CLAIM  # noqa: E402
from caption_lies.scoring import flags_conflict, parse_reply, wilson  # noqa: E402

# Categorical palette (validated order); one color per model.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

LABELS = {
    "chart_only": "Chart only",
    "caption": "Caption",
    "user_claim": "User, bare",
    "user_opinion": "User, opinion",
    "user_expert": "User, expert",
    "prior_assistant": "Scripted own turn",
    "self_caption": "Self-caption",
    "self_caption_noclaim": "Self-caption, no claim",
}

# Paired comparisons reported in stats.md (first vs second, same charts).
COMPARISONS = [
    ("user_opinion", "user_claim"), ("user_expert", "user_claim"), ("user_expert", "user_opinion"),
    ("caption", "user_claim"), ("prior_assistant", "user_claim"), ("self_caption", "user_claim"),
    ("self_caption", "prior_assistant"),
]


def load(raw_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(raw_dir.glob("*.jsonl")):
        with open(path) as f:
            rows += [json.loads(line) for line in f if line.strip()]
    if not rows:
        raise SystemExit(f"No results found in {raw_dir}")
    df = pd.DataFrame(rows)
    df = df[df["error"].isna()].copy()
    if "verbs" not in df:
        df["verbs"] = "rose"
    df["verbs"] = df["verbs"].fillna("rose")
    # setting = polarity, plus the verb pair when it is not the default
    df["setting"] = np.where(df["verbs"] == "rose", df["polarity"], df["polarity"] + " (" + df["verbs"] + ")")
    # Keep the latest reply for each item, in case a run was repeated.
    df = df.sort_values("timestamp").drop_duplicates(
        ["provider", "model", "setting", "chart_id", "condition"], keep="last"
    )
    parsed = df["reply"].apply(parse_reply)
    df["answer"] = parsed.str[0]
    df["explanation"] = parsed.str[1]
    df["parse_method"] = parsed.str[2]
    df["parsed"] = df["answer"].notna()
    df["correct"] = df["answer"] == df["truth"]
    df["follows_claim"] = df["claim_direction"].notna() & (df["answer"] == df["claim_direction"])
    df["flags_conflict"] = df["explanation"].apply(flags_conflict)
    df["model_label"] = df["provider"] + "/" + df["model"]
    if "own_description" not in df:
        df["own_description"] = None
    own = df["own_description"].fillna("").apply(lambda t: parse_reply(t)[0] if t else None)
    df["own_desc_correct"] = np.where(own.isna(), np.nan, (own == df["truth"]).astype(float))
    return df


def baseline_ok(df: pd.DataFrame, label: str) -> set:
    """Charts this model read correctly with no claim (chart_only, default setting)."""
    b = df[(df["model_label"] == label) & (df["condition"] == "chart_only") & df["parsed"]
           & (df["setting"] == "contradict")]
    if b.empty:
        b = df[(df["model_label"] == label) & (df["condition"] == "chart_only") & df["parsed"]]
    return set(b.loc[b["correct"], "chart_id"])


def paired_stats(df: pd.DataFrame) -> str:
    """Exact McNemar tests on paired flips, and flips split by the chart's true direction."""
    from scipy.stats import binomtest

    lines = ["# Paired comparisons", "",
             "Charts each model read correctly with no claim only. Each row compares the flip rate",
             "in two conditions on the same charts; p is an exact two-sided McNemar test.", ""]
    rows, dir_rows = [], []
    for (label, setting), g in df[df["setting"].str.startswith("contradict")].groupby(["model_label", "setting"]):
        ok = baseline_ok(df, label)
        g = g[g["chart_id"].isin(ok) & g["parsed"]]
        piv = g.pivot_table(index="chart_id", columns="condition", values="follows_claim", aggfunc="first")
        for a, b in COMPARISONS:
            if a not in piv or b not in piv:
                continue
            pair = piv[[a, b]].dropna().astype(bool)
            if len(pair) < 10:
                continue
            n10 = int((pair[a] & ~pair[b]).sum())
            n01 = int((~pair[a] & pair[b]).sum())
            pval = binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1.0
            rows.append({"model": label, "setting": setting, "comparison": f"{LABELS[a]} vs {LABELS[b]}",
                         "n": len(pair), "rate_a": round(pair[a].mean(), 3), "rate_b": round(pair[b].mean(), 3),
                         "only_a": n10, "only_b": n01, "p": f"{pval:.2g}"})
        claims = g[~g["condition"].isin(NO_CLAIM)]
        if len(claims):
            t = claims.pivot_table(index="condition", columns="truth", values="follows_claim", aggfunc="mean")
            for cond, r in t.iterrows():
                dir_rows.append({"model": label, "setting": setting, "condition": LABELS[cond],
                                 "claim says 'rose' (chart fell)": round(r.get("decrease", np.nan), 3),
                                 "claim says 'fell' (chart rose)": round(r.get("increase", np.nan), 3)})
    if rows:
        lines.append(pd.DataFrame(rows).to_markdown(index=False))
    lines += ["", "# Flip rate by the chart's true direction", "",
              "Does a false claim of growth work as well as a false claim of decline?", ""]
    if dir_rows:
        lines.append(pd.DataFrame(dir_rows).to_markdown(index=False, floatfmt=".3f"))
    return "\n".join(lines) + "\n"


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (label, setting), g in df.groupby(["model_label", "setting"]):
        read_ok = baseline_ok(df, label)
        contradict = setting.startswith("contradict")
        for cond in [c for c in CONDITIONS if c in set(g["condition"])]:
            c = g[g["condition"] == cond]
            p = c[c["parsed"]]
            k_acc, n = int(p["correct"].sum()), len(p)
            row = {
                "model": label, "polarity": setting, "condition": cond,
                "n": len(c), "parse_rate": round(len(p) / len(c), 3) if len(c) else np.nan,
                "accuracy": round(k_acc / n, 3) if n else np.nan,
                "accuracy_lo": round(wilson(k_acc, n)[0], 3), "accuracy_hi": round(wilson(k_acc, n)[1], 3),
            }
            if cond not in NO_CLAIM and contradict:
                k_f = int(p["follows_claim"].sum())
                row["follow_rate"] = round(k_f / n, 3) if n else np.nan
                sub = p[p["chart_id"].isin(read_ok)]
                k_flip = int(sub["follows_claim"].sum())
                row["flip_n"] = len(sub)
                row["flip_rate"] = round(k_flip / len(sub), 3) if len(sub) else np.nan
                lo, hi = wilson(k_flip, len(sub))
                row["flip_lo"], row["flip_hi"] = round(lo, 3), round(hi, 3)
                right = p[p["correct"]]
                row["conflict_rate"] = round(right["flags_conflict"].mean(), 3) if len(right) else np.nan
            if cond == "self_caption":
                row["own_desc_acc"] = round(c["own_desc_correct"].mean(), 3)
            out.append(row)
    return pd.DataFrame(out)


def _style(ax, ylabel):
    ax.set_ylim(0, 1.05)
    ax.set_ylabel(ylabel, color=INK, fontsize=10)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, length=0)


PRETTY = {"gemma3:4b": "Gemma 3 4B", "qwen2.5vl:3b": "Qwen2.5-VL 3B", "qwen2.5vl:7b": "Qwen2.5-VL 7B"}


def pretty(label: str) -> str:
    """'ollama/gemma3:4b' -> 'Gemma 3 4B'; unknown models keep their id."""
    model = label.split("/", 1)[-1]
    if model in PRETTY:
        return PRETTY[model]
    if model.startswith("gemini-"):
        return "Gemini " + model[len("gemini-"):].replace("-", " ").title()
    return model


def grouped_bars(summary, value, lo, hi, conditions, ylabel, title, path, mock):
    models = list(dict.fromkeys(summary["model"]))
    fig, ax = plt.subplots(figsize=(max(8, 1.4 * len(conditions) + 2), 4.5), dpi=150)
    width = 0.8 / max(len(models), 1)
    x = np.arange(len(conditions))
    for i, m in enumerate(models):
        s = summary[summary["model"] == m].set_index("condition").reindex(conditions)
        vals = s[value].to_numpy(dtype=float)
        err = np.vstack([vals - s[lo].to_numpy(dtype=float), s[hi].to_numpy(dtype=float) - vals])
        pos = x - 0.4 + width * (i + 0.5)
        ax.bar(pos, vals, width * 0.92, color=SERIES[i % len(SERIES)], label=pretty(m))
        ax.errorbar(pos, vals, yerr=err, fmt="none", ecolor=MUTED, elinewidth=1, capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[c] for c in conditions], color=INK)
    _style(ax, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=12)
    ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    if mock:
        fig.text(0.5, 0.5, "MOCK DATA, NOT REAL RESULTS", ha="center", va="center",
                 fontsize=26, color="#e34948", alpha=0.25, rotation=20)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raw", default="results/raw")
    p.add_argument("--out", default="results")
    args = p.parse_args()

    out = Path(args.out)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    df = load(Path(args.raw))
    mock = (df["provider"] == "mock").any()
    df.drop(columns=["reply"]).to_csv(out / "scored.csv", index=False)

    summary = summarize(df)
    summary.to_csv(out / "summary.csv", index=False)

    cols = ["model", "polarity", "condition", "n", "parse_rate", "accuracy", "follow_rate", "flip_rate",
            "conflict_rate", "own_desc_acc"]
    md = summary[[c for c in cols if c in summary]].copy()
    md["condition"] = md["condition"].map(LABELS)
    with open(out / "summary.md", "w") as f:
        if mock:
            f.write("> MOCK DATA from a simulated model. These numbers test the pipeline and mean nothing.\n\n")
        f.write(md.to_markdown(index=False, floatfmt=".3f"))
        f.write("\n")

    with open(out / "stats.md", "w") as f:
        f.write(paired_stats(df))

    # Figures leave out models with too few charts so far (for example a
    # rate-limited API partway through); they still appear in the tables.
    enough = summary[(summary["condition"] == "chart_only") & (summary["n"] >= 30)]["model"].unique()
    for polarity, s in summary[summary["model"].isin(enough)].groupby("polarity"):
        tag = re.sub(r"[^a-z_]+", "_", polarity).strip("_")
        conds = [c for c in CONDITIONS if c in set(s["condition"])]
        grouped_bars(s, "accuracy", "accuracy_lo", "accuracy_hi", conds, "Accuracy",
                     f"Accuracy by claim source ({polarity} claim)", out / "figures" / f"accuracy_{tag}.png", mock)
        claim_conds = [c for c in conds if c not in NO_CLAIM]
        if claim_conds and polarity == "contradict":
            grouped_bars(s, "flip_rate", "flip_lo", "flip_hi", claim_conds,
                         "Answers flipped to the claim",
                         "How often a false claim overrides a correctly read chart",
                         out / "figures" / "flip_rate.png", mock)

    print(md.to_string(index=False))
    print(f"\nWrote {out}/summary.csv, {out}/summary.md, {out}/stats.md, {out}/scored.csv and {out}/figures/")


if __name__ == "__main__":
    main()
