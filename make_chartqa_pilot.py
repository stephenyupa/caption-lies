"""Build the real-chart pilot: 40 charts from the ChartQA test set (Masry et al., 2022).

The pilot asks whether the main findings hold on real, published charts, which are
noisier and more varied than the synthetic set. It uses the same conditions, claim
template, question and scoring as the main experiment; only the charts change.

Selection (reproducible from the ChartQA repository):
  1. Single-series time series only: ChartQA tables with two columns, a year in
     every row, years in order, 6 to 16 points, and all values positive.
  2. A trend that passes the same three direction checks as the synthetic charts
     (endpoints, least-squares slope, order of minimum and maximum), a change of
     at least 15%, and a straight line explaining at least half the variance.
  3. Metrics that are not themselves changes or growth rates, where "rose" and
     "fell" would be ambiguous.
  4. A seeded random draw, at most two charts per metric name per direction, then
     a visual check of every chart. The 40 kept charts (20 rising, 20 falling)
     and their chart types are listed in SELECTED below.

The claim names the metric instead of a company, for example "The revenue fell
between 2013 and 2020." The expert framing becomes "According to a senior analyst
who covers this data," because most of these charts are not about one company.

ChartQA is released under the GNU General Public License v3.0. The copied images
and tables keep that license; see data_chartqa/LICENSE_ChartQA.

Usage:
    git clone --depth 1 https://github.com/vis-nlp/ChartQA ../ChartQA
    python make_chartqa_pilot.py --chartqa "../ChartQA/ChartQA Dataset"
The folder data_chartqa/ is already included in this repository, so this step is
only needed to rebuild it.
"""

import argparse
import csv
import json
import re
import shutil
from pathlib import Path

import numpy as np

SPLIT = "test"
# (ChartQA file id, chart type checked by eye). The first 20 rise, the last 20 fall.
SELECTED = [
    ("two_col_23649", "bar"), ("two_col_82630", "bar"), ("two_col_1809", "bar"), ("two_col_2865", "bar"),
    ("two_col_103058", "bar"), ("two_col_24515", "bar"), ("two_col_102416", "bar"), ("two_col_24203", "bar"),
    ("two_col_104878", "bar"), ("two_col_3226", "bar"), ("two_col_40227", "bar"), ("two_col_43126", "bar"),
    ("two_col_1112", "bar"), ("two_col_104700", "line"), ("two_col_4484", "bar"), ("two_col_4110", "bar"),
    ("two_col_60996", "bar"), ("two_col_100103", "bar"), ("two_col_81950", "bar"), ("two_col_23489", "bar"),
    ("two_col_43933", "bar"), ("two_col_23957", "bar"), ("two_col_40350", "bar"), ("two_col_82336", "bar"),
    ("two_col_103474", "bar"), ("two_col_82607", "bar"), ("two_col_21579", "bar"), ("two_col_60885", "bar"),
    ("two_col_20673", "bar"), ("two_col_43039", "bar"), ("two_col_80443", "bar"), ("two_col_20975", "bar"),
    ("two_col_81937", "line"), ("two_col_22558", "line"), ("two_col_81271", "bar"), ("two_col_63561", "bar"),
    ("two_col_23724", "bar"), ("two_col_83483", "bar"), ("two_col_3712", "bar"), ("two_col_23907", "line"),
]

EXPERT_FRAME = "According to a senior analyst who covers this data, "
# Hand-written subjects where the column header does not read as a noun phrase.
SUBJECTS = {
    "two_col_83483": "the CO2-equivalent emissions",
    "two_col_23957": "the number of deaths per 1,000 live births",
    "two_col_81950": "the number of inhabitants per square kilometer",
    "two_col_1809": "the R&D expenditure",
}
UNIT = re.compile(
    r"\s+in\s+(?:constant\s+)?(?:\d[\d,]*\s+)?(?:million|billion|thousand|trillion|hundred|U\.?S\.?|US|euros?|"
    r"GBP|Canadian|Chinese|Danish|units?|millions|billions|thousands|percent|kilo|tonnes?|metric|cubic)\b.*$",
    re.IGNORECASE)


def number(text: str) -> float:
    return float(text.strip().replace(",", "").replace("%", "").replace("$", "").replace("*", ""))


def subject(metric: str) -> str:
    """'Revenue in million U.S. dollars*' -> 'the revenue'."""
    s = re.sub(r"\(.*?\)", "", metric.replace("*", "")).strip()
    s = re.sub(r"\s+", " ", UNIT.sub("", s)).strip(" ,")
    first = s.split()[0]
    if first[1:] == first[1:].lower():  # leave acronyms such as "GVA" or "R&D" alone
        s = s[0].lower() + s[1:]
    return f"the {s}"


def build(chartqa: Path, out: Path) -> list[dict]:
    (out / "images").mkdir(parents=True, exist_ok=True)
    (out / "tables").mkdir(exist_ok=True)
    rows_out = []
    for file_id, kind in SELECTED:
        table = chartqa / SPLIT / "tables" / f"{file_id}.csv"
        rows = list(csv.reader(open(table, encoding="utf-8", errors="ignore")))
        header, body = rows[0], [r for r in rows[1:] if len(r) == 2]
        labels = [r[0].strip().replace("*", "") for r in body]
        values = [number(r[1]) for r in body]
        if int(labels[0][:4]) > int(labels[-1][:4]):
            labels, values = labels[::-1], values[::-1]
        v = np.asarray(values)
        direction = "increase" if v[-1] > v[0] else "decrease"
        shutil.copy(chartqa / SPLIT / "png" / f"{file_id}.png", out / "images" / f"{file_id}.png")
        shutil.copy(table, out / "tables" / f"{file_id}.csv")
        rows_out.append({
            "chart_id": f"cq_{file_id}", "image": f"images/{file_id}.png", "source": f"ChartQA {SPLIT}/{file_id}",
            "company": None, "subject": SUBJECTS.get(file_id) or subject(header[1]), "metric": header[1].replace("*", "").strip(),
            "expert_frame": EXPERT_FRAME, "kind": kind, "direction": direction,
            "start_label": labels[0], "end_label": labels[-1],
            "start_value": values[0], "end_value": values[-1],
            "pct_change": round((values[-1] - values[0]) / abs(values[0]) * 100, 1),
            "labels": labels, "values": values,
        })
    with open(out / "charts.jsonl", "w") as f:
        for r in rows_out:
            f.write(json.dumps(r) + "\n")
    return rows_out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--chartqa", required=True, help='path to the "ChartQA Dataset" folder of the ChartQA repository')
    p.add_argument("--out", default="data_chartqa")
    args = p.parse_args()
    chartqa = Path(args.chartqa)
    rows = build(chartqa, Path(args.out))
    lic = chartqa.parent / "LICENSE"
    if lic.exists():
        shutil.copy(lic, Path(args.out) / "LICENSE_ChartQA")
    up = sum(r["direction"] == "increase" for r in rows)
    print(f"Wrote {len(rows)} charts ({up} rising, {len(rows) - up} falling) to {args.out}/")


if __name__ == "__main__":
    main()
