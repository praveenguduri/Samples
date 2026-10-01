"""
Post-training evaluation: compare your fine-tuned checkpoint against the base
deepset model on the SAME test set, so you can prove the fine-tune actually
helped — and, critically, that it did NOT quietly lose attack recall.

For a security control the decision rule is blunt:
    SHIP the fine-tune only if it keeps (or improves) attack recall AND
    improves benign precision / clears your false positives.
If attack recall dropped, the fine-tune made the control weaker — ship the
base model instead, regardless of how nicely it fixed the phone-number case.

Test CSV format (same as training): text,label  with 0=LEGIT, 1=INJECTION.
Use a HELD-OUT test set the fine-tune never trained on, or your numbers lie.

Usage:
    python evaluate_model.py --test test.csv --finetuned ./deepset-ft-v1
    # optionally add some benign false-positive probes to watch directly:
    python evaluate_model.py --test test.csv --finetuned ./deepset-ft-v1 \
        --probes "do a person safety check on 9544610832" "run a lookup on account 12345"
"""

import argparse

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    confusion_matrix,
    precision_recall_fscore_support,
    recall_score,
)
from transformers import AutoModelForSequenceClassification, AutoTokenizer

BASE_MODEL = "deepset/deberta-v3-base-injection"


class Model:
    def __init__(self, model_id: str):
        self.tok = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.model.eval()
        id2label = self.model.config.id2label
        self.inj_idx = next(
            (i for i, lbl in id2label.items() if "inj" in str(lbl).lower()), 1
        )

    def predict(self, texts, threshold=0.5):
        preds, scores = [], []
        for t in texts:
            enc = self.tok(str(t).strip().lower(), return_tensors="pt",
                           truncation=True, max_length=512)
            with torch.no_grad():
                logits = self.model(**enc).logits
            s = torch.softmax(logits, dim=-1)[0][self.inj_idx].item()
            scores.append(s)
            preds.append(1 if s >= threshold else 0)
        return np.array(preds), np.array(scores)


def report(name, y_true, y_pred):
    p, r, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    # attack recall = recall on the injection class specifically
    attack_recall = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    # benign precision via confusion: how often a "block" was actually an attack
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    benign_fp_rate = fp / (fp + tn) if (fp + tn) else 0.0  # benign wrongly blocked
    print(f"\n[{name}]")
    print(f"  precision={p:.3f}  recall={r:.3f}  f1={f1:.3f}")
    print(f"  attack recall (inj caught)      : {attack_recall:.3f}")
    print(f"  benign false-positive rate      : {benign_fp_rate:.3f}  ({fp} of {fp+tn} benign blocked)")
    print(f"  confusion [tn={tn} fp={fp} fn={fn} tp={tp}]")
    return {"attack_recall": attack_recall, "benign_fp_rate": benign_fp_rate, "f1": f1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", required=True, help="held-out test CSV: text,label")
    ap.add_argument("--finetuned", required=True, help="path to fine-tuned checkpoint dir")
    ap.add_argument("--base", default=BASE_MODEL)
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--probes", nargs="*", default=None,
                    help="extra benign prompts to score directly (your false positives)")
    args = ap.parse_args()

    df = pd.read_csv(args.test)
    df["label"] = df["label"].astype(int)
    texts, y = df["text"].tolist(), df["label"].values

    base = Model(args.base)
    ft = Model(args.finetuned)

    bp, _ = base.predict(texts, args.threshold)
    fp_, _ = ft.predict(texts, args.threshold)

    print("=" * 60)
    print(f"Test set: {len(y)}  ({int((y==1).sum())} injection / {int((y==0).sum())} benign)")
    print(f"Threshold: {args.threshold}")
    print("=" * 60)

    b = report("BASE  deepset", y, bp)
    f = report("FINE-TUNED", y, fp_)

    # --- the ship / no-ship decision ---
    print("\n" + "=" * 60)
    print("DECISION")
    print("=" * 60)
    recall_delta = f["attack_recall"] - b["attack_recall"]
    fp_delta = f["benign_fp_rate"] - b["benign_fp_rate"]
    print(f"  attack recall change : {recall_delta:+.3f}")
    print(f"  benign FP-rate change: {fp_delta:+.3f}  (negative = fewer false positives, good)")

    if recall_delta < -0.01:
        print("\n  >>> DO NOT SHIP. Fine-tune LOST attack recall — the control got weaker.")
    elif fp_delta < 0:
        print("\n  >>> SHIP. Fewer false positives with attack recall held. This is the win.")
    else:
        print("\n  >>> MARGINAL. Recall held but false positives didn't drop — fine-tune bought little.")

    # --- direct probes: watch your specific false positives ---
    if args.probes:
        print("\n" + "=" * 60)
        print("PROBES (benign — want LOW injection scores)")
        print("=" * 60)
        _, bs = base.predict(args.probes, args.threshold)
        _, fs = ft.predict(args.probes, args.threshold)
        print(f"  {'base':>6} {'ft':>6}   prompt")
        for prompt, bb, ff in zip(args.probes, bs, fs):
            print(f"  {bb:>6.3f} {ff:>6.3f}   {prompt!r}")


if __name__ == "__main__":
    main()
