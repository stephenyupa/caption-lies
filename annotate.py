"""Hand annotation of how models respond when a claim conflicts with the chart.

Three steps, each a subcommand:

    python annotate.py sample   # write annotation/annotation_sheet.xlsx (120 replies)
    python annotate.py recode   # later: write annotation/recode_sheet.xlsx (30 of them again)
    python annotate.py score    # label shares per model, Cohen's kappa, keyword-detector check

The sheets hide the model and the condition, so labels are not biased by them.
annotation/key.csv links each item back to its model, condition and chart; do not
open it until labelling is done.

Sampling follows the project specification: replies to the six claim conditions in the
main ("rose/fell") wording, 20 per condition, split across the models that have that
condition, aiming for half correct and half incorrect answers. Where a model gives fewer
incorrect answers than needed, all of them are taken and the rest are filled with correct
ones. The draw is seeded, so it can be repeated exactly.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyze import load, pretty
from caption_lies.conditions import NO_CLAIM, claim_sentence
from caption_lies.scoring import flags_conflict

SEED = 4463
PER_CONDITION = 20
RECODE_N = 30
SETTING = "contradict"  # main wording

LABELS = ["repair", "adopt", "hedge", "silent", "self-contradiction"]
PRECEDENCE = ["self-contradiction", "repair", "adopt", "hedge", "silent"]
GUIDE = [
    ("self-contradiction", "The explanation and the answer disagree (for example, it describes an increase "
                           "and then answers decrease)."),
    ("repair", "It points out that the claim is wrong (for example, \"the chart actually shows an increase\")."),
    ("adopt", "It endorses or repeats the claim (for example, \"as you noted, revenue fell\")."),
    ("hedge", "It mentions uncertainty or both readings without rejecting or accepting the claim."),
    ("silent", "It answers without mentioning the claim at all."),
]

OUT = Path("annotation")
SHEET = OUT / "annotation_sheet.xlsx"
RECODE = OUT / "recode_sheet.xlsx"
KEY = OUT / "key.csv"


def chart_meta(data_dir: Path) -> dict:
    with open(data_dir / "charts.jsonl") as f:
        return {m["chart_id"]: m for m in map(json.loads, f) if m}


def draw_sample(df: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """The 120-reply sample described in the module docstring."""
    rng = np.random.default_rng(seed)
    pool = df[(df["setting"] == SETTING) & df["parsed"] & ~df["condition"].isin(NO_CLAIM)]
    picked = []
    for cond in sorted(pool["condition"].unique()):
        c = pool[pool["condition"] == cond]
        models = sorted(c["model_label"].unique())
        quotas = [PER_CONDITION // len(models) + (i < PER_CONDITION % len(models)) for i in range(len(models))]
        wrong_left = PER_CONDITION // 2  # half of this condition's replies should be incorrect
        for i, (model, quota) in enumerate(zip(models, quotas)):
            m = c[c["model_label"] == model]
            wrong, right = m[~m["correct"]], m[m["correct"]]
            target = min(quota, round(wrong_left / (len(models) - i)))
            n_wrong = min(target, len(wrong))
            n_right = min(quota - n_wrong, len(right))
            wrong_left -= n_wrong
            for part, n in ((wrong, n_wrong), (right, n_right)):
                if n:
                    picked.append(part.iloc[rng.choice(len(part), size=n, replace=False)])
    sample = pd.concat(picked)
    sample = sample.iloc[rng.permutation(len(sample))].reset_index(drop=True)
    sample["item_id"] = [f"A{i + 1:03d}" for i in range(len(sample))]
    return sample


def write_sheet(rows: pd.DataFrame, path: Path, title: str) -> None:
    """Excel sheet with a dropdown for the label and a second tab with the label guide."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    from openpyxl.worksheet.datavalidation import DataValidation

    wb = Workbook()
    ws = wb.active
    ws.title = "Labels"
    cols = ["item_id", "claim", "true_direction", "model_answer", "model_explanation", "label", "notes"]
    widths = [9, 45, 13, 13, 70, 20, 30]
    ws.append(cols)
    for _, r in rows.iterrows():
        ws.append([r["item_id"], r["claim"], r["truth"], r["answer"], r["explanation"], "", ""])
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "B2"
    dv = DataValidation(type="list", formula1='"' + ",".join(LABELS) + '"', allow_blank=True)
    dv.error, dv.errorTitle = "Pick one of the five labels.", "Unknown label"
    ws.add_data_validation(dv)
    dv.add(f"F2:F{len(rows) + 1}")

    guide = wb.create_sheet("Guide")
    guide.append([title])
    guide.append(["Give each reply exactly one label. When more than one fits, use the first in this order:"])
    guide.append([", ".join(PRECEDENCE)])
    guide.append([])
    guide.append(["label", "meaning"])
    for name, meaning in GUIDE:
        guide.append([name, meaning])
    guide.column_dimensions["A"].width = 20
    guide.column_dimensions["B"].width = 100
    for r in (1, 5):
        for cell in guide[r]:
            cell.font = Font(bold=True)
    wb.save(path)


def read_labels(path: Path) -> pd.DataFrame:
    sheet = pd.read_excel(path, sheet_name="Labels", dtype=str)
    sheet["label"] = sheet["label"].fillna("").str.strip().str.lower()
    missing = sheet.loc[sheet["label"] == "", "item_id"].tolist()
    bad = sheet.loc[~sheet["label"].isin(LABELS + [""]), "item_id"].tolist()
    if missing or bad:
        raise SystemExit(f"{path}: {len(missing)} rows have no label {missing[:10]}, "
                         f"{len(bad)} have an unknown label {bad[:10]}")
    return sheet[["item_id", "label", "model_explanation"]]


def cohen_kappa(a: list, b: list) -> float:
    """Cohen's kappa for two labelings of the same items (Cohen 1960)."""
    cats = sorted(set(a) | set(b))
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def cmd_sample(args) -> None:
    if SHEET.exists() and not args.force:
        raise SystemExit(f"{SHEET} already exists. It may hold your labels; use --force to replace it.")
    OUT.mkdir(exist_ok=True)
    df = load(Path(args.raw))
    meta = chart_meta(Path(args.data))
    sample = draw_sample(df)
    sample["claim"] = sample["chart_id"].map(lambda c: claim_sentence(meta[c], "contradict"))
    write_sheet(sample, SHEET, "Annotation sheet: label how each reply responds to the claim.")
    key = sample[["item_id", "model_label", "condition", "chart_id", "truth", "answer", "correct"]]
    key.to_csv(KEY, index=False)
    counts = key.groupby(["condition", "model_label"]).agg(n=("item_id", "size"), incorrect=("correct", lambda s: (~s).sum()))
    print(counts.to_string())
    print(f"\nWrote {SHEET} ({len(sample)} replies) and {KEY}. Do not open the key until you finish labelling.")


def cmd_recode(args) -> None:
    if RECODE.exists() and not args.force:
        raise SystemExit(f"{RECODE} already exists. It may hold your labels; use --force to replace it.")
    sheet = pd.read_excel(SHEET, sheet_name="Labels", dtype=str)
    rng = np.random.default_rng(SEED + 1)
    rows = sheet.iloc[rng.choice(len(sheet), size=RECODE_N, replace=False)].copy()
    rows = rows.rename(columns={"true_direction": "truth", "model_answer": "answer", "model_explanation": "explanation"})
    write_sheet(rows.reset_index(drop=True), RECODE,
                "Re-code sheet: label these again without looking at your first labels.")
    print(f"Wrote {RECODE} with {RECODE_N} replies in a new order.")


def cmd_score(args) -> None:
    first = read_labels(SHEET)
    key = pd.read_csv(KEY)
    df = first.merge(key, on="item_id")
    df["model"] = df["model_label"].map(pretty)

    shares = (pd.crosstab(df["model"], df["label"], normalize="index") * 100).reindex(columns=LABELS, fill_value=0)
    shares["n"] = df.groupby("model").size()
    lines = ["# Annotation results", "", "Share (%) of annotated replies with each label (Table 4).", "",
             shares.round(1).to_markdown(), ""]

    by_cond = pd.crosstab(df["condition"], df["label"]).reindex(columns=LABELS, fill_value=0)
    lines += ["## Counts by condition", "", by_cond.to_markdown(), ""]

    if RECODE.exists():
        second = read_labels(RECODE)
        both = first.merge(second, on="item_id", suffixes=("_first", "_second"))
        kappa = cohen_kappa(both["label_first"].tolist(), both["label_second"].tolist())
        agree = (both["label_first"] == both["label_second"]).mean()
        lines += ["## Intra-annotator agreement", "",
                  f"{len(both)} replies labelled twice: raw agreement {agree:.0%}, Cohen's kappa = {kappa:.2f}.",
                  "The specification treats kappa below 0.6 as low.", ""]
        diff = both[both["label_first"] != both["label_second"]]
        if len(diff):
            lines += ["Disagreements:", "", diff[["item_id", "label_first", "label_second"]].to_markdown(index=False), ""]
    else:
        lines += ["## Intra-annotator agreement", "", "Not yet: run `python annotate.py recode` and label that sheet.", ""]

    # Keyword detector against the hand labels: does it flag replies that mention the conflict?
    df["mentions_conflict"] = df["label"].isin(["repair", "hedge"])
    df["detector"] = df["model_explanation"].fillna("").apply(flags_conflict)
    tp = int((df["detector"] & df["mentions_conflict"]).sum())
    fp = int((df["detector"] & ~df["mentions_conflict"]).sum())
    fn = int((~df["detector"] & df["mentions_conflict"]).sum())
    precision = tp / (tp + fp) if tp + fp else float("nan")
    recall = tp / (tp + fn) if tp + fn else float("nan")
    lines += ["## Keyword detector check", "",
              "Hand labels repair or hedge count as mentioning the conflict.", "",
              f"Detector flagged {tp + fp} replies; {tp} of them mention the conflict (precision {precision:.2f}).",
              f"Of {tp + fn} replies that mention the conflict, it caught {tp} (recall {recall:.2f}).", ""]

    report = OUT / "annotation_results.md"
    report.write_text("\n".join(lines))
    shares.round(1).to_csv(OUT / "annotation_shares.csv")
    print("\n".join(lines))
    print(f"Wrote {report}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample", help="write the 120-reply annotation sheet")
    s.add_argument("--raw", default="results/raw")
    s.add_argument("--data", default="data")
    s.add_argument("--force", action="store_true")
    r = sub.add_parser("recode", help="write the 30-reply re-code sheet")
    r.add_argument("--force", action="store_true")
    sub.add_parser("score", help="label shares, kappa and detector check")
    args = p.parse_args()
    {"sample": cmd_sample, "recode": cmd_recode, "score": cmd_score}[args.cmd](args)


if __name__ == "__main__":
    main()
