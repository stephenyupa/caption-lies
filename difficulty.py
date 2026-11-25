"""Chart ground-truth checks and an exploratory analysis of visual difficulty.

Two questions a reader may ask about synthetic charts:

1. Is each chart's label (rising or falling) really what the chart shows?
   chart_checks() tests every chart three ways: the sign of the change from first
   to last point, the sign of the least-squares slope, and whether the maximum
   comes after the minimum (rising) or before it (falling). It also reports how
   noisy each trend is: the variance a straight line leaves unexplained, and the
   share of consecutive steps that move in the trend's direction.

2. Do models defer more when the chart is harder to read?
   difficulty_models() fits, for each model, a logistic regression of following
   the false claim on chart noise and on the size of the change, controlling for
   chart type, condition and wording, with standard errors clustered by chart.
   It uses claim conditions in the contradicting wordings, on charts the model
   read correctly with no claim. Because false claims of growth almost never
   work, it uses rising charts only. Conditions in which the model never followed
   the claim are left out (they carry no information and break the fit), and
   models with fewer than MIN_FLIPS flips are skipped. This analysis was not
   planned in the specification, so treat it as exploratory.

Run through analyze.py, which writes:
    results/chart_checks.csv       one row per chart
    results/difficulty_models.csv  one row per model x predictor
    results/difficulty.md          both, summarized in Markdown
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

MIN_FLIPS = 10
from caption_lies.conditions import CORE_CLAIM_CONDITIONS


def load_charts(data_dir: Path) -> dict:
    with open(Path(data_dir) / "charts.jsonl") as f:
        return {m["chart_id"]: m for m in map(json.loads, f) if m}


def chart_checks(meta: dict) -> pd.DataFrame:
    """Direction checks and noise measures for every chart."""
    rows = []
    for cid, m in meta.items():
        v = np.asarray(m["values"], dtype=float)
        x = np.arange(len(v))
        sign = 1 if m["direction"] == "increase" else -1
        slope, intercept = np.polyfit(x, v, 1)
        fit = slope * x + intercept
        r2 = 1 - ((v - fit) ** 2).sum() / ((v - v.mean()) ** 2).sum()
        rows.append({
            "chart_id": cid, "kind": m["kind"], "metric": m["metric"], "direction": m["direction"],
            "pct_change": abs(m["pct_change"]), "points": len(v),
            "endpoints_agree": bool(np.sign(v[-1] - v[0]) == sign),
            "slope_agrees": bool(np.sign(slope) == sign),
            "extremes_agree": bool((np.argmax(v) > np.argmin(v)) == (sign > 0)),
            "r2": r2,
            "noise_pct": (1 - r2) * 100,  # share of variance a straight line leaves unexplained
            "steps_with_trend": float((np.sign(np.diff(v)) == sign).mean()),
        })
    return pd.DataFrame(rows).sort_values("chart_id").reset_index(drop=True)


def difficulty_models(df: pd.DataFrame, checks: pd.DataFrame, baseline_ok) -> pd.DataFrame:
    """Odds ratios for chart noise and size of change, one model at a time."""
    import statsmodels.formula.api as smf

    d = df.merge(checks[["chart_id", "kind", "pct_change", "noise_pct"]], on="chart_id")
    rows = []
    for label in sorted(d["model_label"].unique()):
        x = d[(d["model_label"] == label) & d["setting"].str.startswith("contradict") & d["parsed"]
              & d["condition"].isin(CORE_CLAIM_CONDITIONS) & (d["truth"] == "increase")
              & d["chart_id"].isin(baseline_ok(df, label))].copy()
        x["fc"] = x["follows_claim"].astype(int)
        used = x.groupby("condition")["fc"].sum()
        x = x[x["condition"].isin(used[used > 0].index)]
        if x["fc"].sum() < MIN_FLIPS:
            continue
        x["pct10"] = x["pct_change"] / 10
        terms = ["pct10", "noise_pct"]
        for col in ("kind", "condition", "setting"):
            if x[col].nunique() > 1:
                terms.append(f"C({col})")
        fit = smf.logit("fc ~ " + " + ".join(terms), data=x).fit(
            disp=0, maxiter=200, cov_type="cluster", cov_kwds={"groups": pd.factorize(x["chart_id"])[0]})
        thirds = pd.qcut(x["noise_pct"], 3, labels=["cleanest", "middle", "noisiest"])
        by_third = x.groupby(thirds, observed=True)["fc"].mean()
        ci = fit.conf_int()
        for term, name in (("noise_pct", "noise (per percentage point)"), ("pct10", "size of change (per 10 points)")):
            rows.append({
                "model": label, "predictor": name, "answers": len(x), "charts": x["chart_id"].nunique(),
                "conditions": ", ".join(sorted(x["condition"].unique())),
                "odds_ratio": round(float(np.exp(fit.params[term])), 3),
                "ci_low": round(float(np.exp(ci.loc[term, 0])), 3),
                "ci_high": round(float(np.exp(ci.loc[term, 1])), 3),
                "p": float(fit.pvalues[term]),
                "flip_cleanest_third": round(float(by_third.get("cleanest", np.nan)), 3),
                "flip_noisiest_third": round(float(by_third.get("noisiest", np.nan)), 3),
            })
    return pd.DataFrame(rows)


def difficulty_report(checks: pd.DataFrame, models: pd.DataFrame) -> str:
    n = len(checks)
    all_three = int((checks["endpoints_agree"] & checks["slope_agrees"] & checks["extremes_agree"]).sum())
    lines = [
        "# Chart ground-truth checks", "",
        f"{all_three} of {n} charts pass all three direction checks "
        "(endpoints, least-squares slope, order of minimum and maximum).", "",
        "| measure | min | median | max |", "|:--|--:|--:|--:|",
        f"| size of change (%) | {checks['pct_change'].min():.1f} | {checks['pct_change'].median():.1f} | {checks['pct_change'].max():.1f} |",
        f"| variance explained by a straight line (%) | {checks['r2'].min() * 100:.1f} | {checks['r2'].median() * 100:.1f} | {checks['r2'].max() * 100:.1f} |",
        f"| steps moving with the trend (%) | {checks['steps_with_trend'].min() * 100:.0f} | {checks['steps_with_trend'].median() * 100:.0f} | {checks['steps_with_trend'].max() * 100:.0f} |",
        "", "# Visual difficulty (exploratory)", "",
        "Logistic regression of following the false claim, rising charts only, standard errors clustered",
        "by chart. An odds ratio above 1 means deference rises with the predictor.", "",
    ]
    if models.empty:
        lines.append("No model had enough flips to fit.")
    else:
        t = models.copy()
        t["p"] = t["p"].map(lambda v: f"{v:.2g}")
        lines.append(t.drop(columns=["conditions"]).to_markdown(index=False))
    return "\n".join(lines) + "\n"
