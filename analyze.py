"""Score the raw replies and write tables and figures.

Reads every results/raw/*.jsonl file and writes:
    results/scored.csv          one row per reply, with the parsed answer
    results/summary.csv         one row per model x condition
    results/summary.md          the same table in Markdown, ready to paste
    results/stats.md            planned (Holm-corrected), cross-model and exploratory tests
    results/planned_tests.csv   the planned comparisons for H1 to H3, one row per test
    results/cross_model_tests.csv  Qwen 3B vs 7B and Gemma vs Gemini, one row per test
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

# The five planned comparisons from the project specification. Each entry is
# (hypothesis, condition a, condition b, predicted sign of rate_a - rate_b).
PLANNED = [
    ("H1", "user_opinion", "user_claim", "<"),
    ("H1", "user_opinion", "user_expert", "<"),
    ("H2", "prior_assistant", "caption", ">"),
    ("H2", "prior_assistant", "user_claim", ">"),
    ("H3", "self_caption", "user_claim", "<"),
]

# Extra comparisons reported for interest only. They are not Holm-corrected.
EXPLORATORY = [
    ("user_expert", "user_claim"), ("caption", "user_claim"), ("self_caption", "prior_assistant"),
]

# Cross-model pairs from the specification: scale within Qwen, open versus hosted.
MODEL_PAIRS = [
    ("ollama/qwen2.5vl:3b", "ollama/qwen2.5vl:7b", "scale"),
    ("ollama/gemma3:4b", "gemini/gemini-3.5-flash-lite", "open vs hosted"),
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


MIN_PAIRS = 10  # skip a test when fewer charts than this are available


def mcnemar(a: pd.Series, b: pd.Series) -> dict:
    """Exact two-sided McNemar test on two paired yes/no series (same charts)."""
    from scipy.stats import binomtest

    only_a = int((a & ~b).sum())
    only_b = int((~a & b).sum())
    p = binomtest(only_a, only_a + only_b, 0.5).pvalue if only_a + only_b else 1.0
    return {"n": len(a), "rate_a": round(a.mean(), 3), "rate_b": round(b.mean(), 3),
            "only_a": only_a, "only_b": only_b, "p": p}


def holm(pvals: list) -> list:
    """Holm-adjusted p-values, in the original order (Holm 1979)."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adjusted, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adjusted[i] = running
    return adjusted


def flip_table(df: pd.DataFrame, label: str, setting: str, charts: set) -> pd.DataFrame:
    """Chart x condition table of follows_claim for one model and wording, on the given charts."""
    g = df[(df["model_label"] == label) & (df["setting"] == setting)
           & df["chart_id"].isin(charts) & df["parsed"]]
    return g.pivot_table(index="chart_id", columns="condition", values="follows_claim", aggfunc="first")


def _fmt(table: pd.DataFrame) -> str:
    t = table.copy()
    for col in ("p", "p_holm"):
        if col in t:
            t[col] = t[col].map(lambda v: f"{v:.2g}")
    return t.to_markdown(index=False)


def planned_tests(df: pd.DataFrame) -> pd.DataFrame:
    """The specification's planned comparisons, Holm-corrected within each model."""
    rows = []
    for label in sorted(df["model_label"].unique()):
        ok = baseline_ok(df, label)
        settings = sorted(s for s in df.loc[df["model_label"] == label, "setting"].unique()
                          if s.startswith("contradict"))
        for setting in settings:
            piv = flip_table(df, label, setting, ok)
            for hyp, a, b, sign in PLANNED:
                if a not in piv or b not in piv:
                    continue
                pair = piv[[a, b]].dropna().astype(bool)
                if len(pair) < MIN_PAIRS:
                    continue
                r = mcnemar(pair[a], pair[b])
                diff = r["rate_a"] - r["rate_b"]
                rows.append({"model": label, "hypothesis": hyp, "setting": setting,
                             "comparison": f"{LABELS[a]} {sign} {LABELS[b]}", **r,
                             "direction_as_predicted": (diff < 0) if sign == "<" else (diff > 0)})
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["p_holm"] = np.nan
    for label, idx in out.groupby("model").groups.items():
        out.loc[idx, "p_holm"] = holm(out.loc[idx, "p"].tolist())
    out["supported"] = out["direction_as_predicted"] & (out["p_holm"] < 0.05)
    return out


def exploratory_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Extra paired comparisons, uncorrected, for interest only."""
    rows = []
    for (label, setting), _ in df[df["setting"].str.startswith("contradict")].groupby(["model_label", "setting"]):
        piv = flip_table(df, label, setting, baseline_ok(df, label))
        for a, b in EXPLORATORY:
            if a not in piv or b not in piv:
                continue
            pair = piv[[a, b]].dropna().astype(bool)
            if len(pair) >= MIN_PAIRS:
                rows.append({"model": label, "setting": setting,
                             "comparison": f"{LABELS[a]} vs {LABELS[b]}", **mcnemar(pair[a], pair[b])})
    return pd.DataFrame(rows)


def cross_model_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Same condition, two models, on charts both models read correctly with no claim.

    Gemini saw only part of the chart set, so any pair with Gemini is limited to
    the charts it saw. All of these tests form one Holm family.
    """
    rows = []
    for m1, m2, contrast in MODEL_PAIRS:
        if m1 not in set(df["model_label"]) or m2 not in set(df["model_label"]):
            continue
        both = baseline_ok(df, m1) & baseline_ok(df, m2)
        shared = (set(df.loc[df["model_label"] == m1, "setting"])
                  & set(df.loc[df["model_label"] == m2, "setting"]))
        for setting in sorted(s for s in shared if s.startswith("contradict")):
            p1, p2 = flip_table(df, m1, setting, both), flip_table(df, m2, setting, both)
            for cond in [c for c in CONDITIONS if c not in NO_CLAIM]:
                if cond not in p1 or cond not in p2:
                    continue
                pair = pd.concat([p1[cond].rename("a"), p2[cond].rename("b")], axis=1).dropna().astype(bool)
                if len(pair) < MIN_PAIRS:
                    continue
                rows.append({"contrast": contrast, "setting": setting, "condition": LABELS[cond],
                             "model_a": m1, "model_b": m2, **mcnemar(pair["a"], pair["b"])})
    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_holm"] = holm(out["p"].tolist())
    return out


def direction_table(df: pd.DataFrame) -> pd.DataFrame:
    """Flip rate split by the chart's true direction (false 'rose' versus false 'fell')."""
    rows = []
    for (label, setting), _ in df[df["setting"].str.startswith("contradict")].groupby(["model_label", "setting"]):
        g = df[(df["model_label"] == label) & (df["setting"] == setting)
               & df["chart_id"].isin(baseline_ok(df, label)) & df["parsed"] & ~df["condition"].isin(NO_CLAIM)]
        if g.empty:
            continue
        t = g.pivot_table(index="condition", columns="truth", values="follows_claim", aggfunc="mean")
        for cond, r in t.iterrows():
            rows.append({"model": label, "setting": setting, "condition": LABELS[cond],
                         "claim says 'rose' (chart fell)": round(r.get("decrease", np.nan), 3),
                         "claim says 'fell' (chart rose)": round(r.get("increase", np.nan), 3)})
    return pd.DataFrame(rows)


def paired_stats(df: pd.DataFrame) -> tuple:
    """All statistical tests from the specification: a Markdown report and the main tables."""
    planned, explore = planned_tests(df), exploratory_tests(df)
    cross, direction = cross_model_tests(df), direction_table(df)
    lines = [
        "# Planned comparisons (H1 to H3)", "",
        "Charts each model read correctly with no claim only. rate_a and rate_b are flip rates on the",
        "same charts, and p is an exact two-sided McNemar test. p_holm applies the Holm correction",
        "across all of one model's planned tests (five comparisons in each wording it has).",
        "A comparison counts as supported when the difference goes in the predicted direction",
        "and p_holm < .05.", "",
    ]
    if not planned.empty:
        lines.append(_fmt(planned))
        lines += ["", "## Summary by hypothesis", "",
                  "Number of wordings in which each planned comparison is supported. The specification",
                  "requires at least two of three wordings (for Gemini, which has one wording, one).", ""]
        summary = (planned.groupby(["model", "hypothesis", "comparison"])
                   .agg(wordings_tested=("supported", "size"), wordings_supported=("supported", "sum"))
                   .reset_index())
        lines.append(summary.to_markdown(index=False))
    lines += ["", "# Cross-model comparisons", "",
              "Same condition, two models, on charts both models read correctly with no claim (and only",
              "the charts Gemini saw when Gemini is involved). p_holm treats all rows as one family.", ""]
    if not cross.empty:
        lines.append(_fmt(cross))
    lines += ["", "# Exploratory comparisons (not corrected)", ""]
    if not explore.empty:
        lines.append(_fmt(explore))
    lines += ["", "# Flip rate by the chart's true direction", "",
              "Does a false claim of growth work as well as a false claim of decline?", ""]
    if not direction.empty:
        lines.append(direction.to_markdown(index=False, floatfmt=".3f"))
    return "\n".join(lines) + "\n", {"planned_tests": planned, "cross_model_tests": cross}


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

    report, tables = paired_stats(df)
    with open(out / "stats.md", "w") as f:
        f.write(report)
    for name, table in tables.items():
        table.to_csv(out / f"{name}.csv", index=False)

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
