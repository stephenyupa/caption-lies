"""Send every chart, in every condition, to one model and save the raw replies.

Results are appended to results/raw/<provider>__<model>__<polarity>.jsonl.
The run can be stopped and restarted at any time: finished items are skipped.

Examples:
    # Test the pipeline with no API key
    python run_experiment.py --provider mock --limit 40

    # See exactly what a model will be sent, without calling it
    python run_experiment.py --provider mock --dry-run --limit 1

    # Pilot on Gemini's free tier (about 100 requests per day)
    python run_experiment.py --provider gemini --limit 25 --sleep 13

    # A local open-weight model with Ollama
    python run_experiment.py --provider ollama --model qwen2.5vl:7b

    # Any OpenAI-compatible service, such as OpenRouter
    python run_experiment.py --provider openai --base-url https://openrouter.ai/api/v1 \\
        --key-env OPENROUTER_API_KEY --model <model-id>
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from caption_lies.charts import load_charts
from caption_lies.conditions import (CONDITIONS, NEEDS_DESCRIPTION, NO_CLAIM, VERB_SETS, build_messages,
                                     claim_direction, describe_messages, render_text)
from caption_lies.models import DEFAULT_MODELS, ModelError, get_model


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9.-]+", "-", s).strip("-")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", required=True, choices=list(DEFAULT_MODELS))
    p.add_argument("--model", help="model id (defaults depend on provider)")
    p.add_argument("--base-url", help="API base URL for openai-compatible or ollama providers")
    p.add_argument("--key-env", help="name of the environment variable holding the API key (openai provider)")
    p.add_argument("--data", default="data", help="chart folder made by generate_charts.py")
    p.add_argument("--conditions", nargs="+", default=CONDITIONS, choices=CONDITIONS)
    p.add_argument("--polarity", choices=["contradict", "consistent"], default="contradict",
                   help="whether the claim contradicts the chart (default) or agrees with it")
    p.add_argument("--verbs", choices=list(VERB_SETS), default="rose",
                   help="verb pair used in the claim: rose/fell (default), increased/decreased, went up/went down")
    p.add_argument("--limit", type=int, help="only use the first N charts (for pilots)")
    p.add_argument("--sleep", type=float, default=0.0, help="seconds to wait between calls (rate limits)")
    p.add_argument("--out", default="results/raw")
    p.add_argument("--dry-run", action="store_true", help="print the conversations instead of calling the model")
    args = p.parse_args()

    charts = load_charts(args.data)
    if args.limit:
        charts = charts[: args.limit]

    if args.dry_run:
        for meta in charts:
            for cond in args.conditions:
                print(f"===== {meta['chart_id']} | {cond} | truth={meta['direction']} =====")
                own = "<the model's own description, from a first call>" if cond in NEEDS_DESCRIPTION else None
                print(render_text(build_messages(meta, cond, Path(args.data), args.polarity,
                                                 own_description=own, verbs=args.verbs)))
                print()
        return

    model = get_model(args.provider, args.model, base_url=args.base_url, key_env=args.key_env)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{args.provider}__{slug(model.model)}"
    suffix = "" if args.verbs == "rose" else f"__{args.verbs}"
    out_path = out_dir / f"{stem}__{args.polarity}{suffix}.jsonl"

    # The model's own chart descriptions, saved by earlier runs of this model.
    # Reusing them keeps the self-caption conditions paired: every condition
    # that needs a description sees the identical one for a given chart.
    own_descriptions = {}
    for path in sorted(out_dir.glob(f"{stem}__*.jsonl")):
        with open(path) as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    if r.get("own_description") and r.get("error") is None:
                        own_descriptions.setdefault(r["chart_id"], r["own_description"])

    done = set()
    if out_path.exists():
        with open(out_path) as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    if r.get("error") is None:
                        done.add((r["chart_id"], r["condition"]))

    todo = [(m, c) for m in charts for c in args.conditions if (m["chart_id"], c) not in done]
    print(f"{args.provider}/{model.model}: {len(done)} done already, {len(todo)} to run -> {out_path}")

    errors = 0
    with open(out_path, "a") as f:
        for i, (meta, cond) in enumerate(todo, 1):
            claim_dir = None if cond in NO_CLAIM else claim_direction(meta, args.polarity)
            call_meta = {**meta, "condition": cond, "claim_direction": claim_dir}
            started = time.time()
            reply, err, own = None, None, None
            try:
                if cond in NEEDS_DESCRIPTION:
                    own = own_descriptions.get(meta["chart_id"])
                    if own is None:
                        # Step 1: the model describes the chart in its own words.
                        own = model.complete(describe_messages(meta, Path(args.data)),
                                             meta={**call_meta, "condition": "describe"})
                        own_descriptions[meta["chart_id"]] = own
                        if args.sleep:
                            time.sleep(args.sleep)
                messages = build_messages(meta, cond, Path(args.data), args.polarity,
                                          own_description=own, verbs=args.verbs)
                reply = model.complete(messages, meta=call_meta)
            except ModelError as e:
                err = str(e)
                errors += 1
            rec = {
                "chart_id": meta["chart_id"],
                "condition": cond,
                "polarity": args.polarity,
                "verbs": args.verbs,
                "provider": args.provider,
                "model": model.model,
                "truth": meta["direction"],
                "claim_direction": claim_dir,
                "reply": reply,
                "own_description": own,
                "error": err,
                "latency_s": round(time.time() - started, 2),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            f.write(json.dumps(rec) + "\n")
            f.flush()
            status = "ERROR " + err[:80] if err else (reply or "")[:70].replace("\n", " ")
            print(f"[{i}/{len(todo)}] {meta['chart_id']} {cond:<20} {status}")
            if errors >= 10 and errors == i:
                sys.exit("Stopping: the first 10 calls all failed. Check the key, model id, or base URL.")
            if args.sleep:
                time.sleep(args.sleep)

    print(f"Finished. {errors} errors. Failed items are retried on the next run.")


if __name__ == "__main__":
    main()
