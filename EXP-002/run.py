#!/usr/bin/env python3
"""Run frozen EFMW-EXP-002 synthetic specificity screen."""
import csv
from pathlib import Path

import numpy as np

from monitors import (
    BASELINE_THRESHOLD,
    EFMW_THRESHOLD,
    baseline_score,
    efmw_score,
    first_sustained_after,
)
from simulator import N_STEPS, simulate

ROOT = Path(__file__).resolve().parent
SEEDS = range(2001, 2081)
WARMUP = 20
PULSE_START = 220
PULSE_END = 231  # inclusive
PULSE_OFFSET = 0.05


def score_one(y, u, scorer, threshold):
    score = scorer(y, u)
    alert = first_sustained_after(score, threshold, WARMUP)
    return alert, float(np.mean(score[WARMUP:] > threshold))


def main():
    output = ROOT / "results.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "seed", "condition", "monitor", "first_sustained_alert",
            "false_alarm", "raw_pointwise_exceedance_rate",
        ])
        for seed in SEEDS:
            rows = simulate(seed, null_degradation=True)
            y_base = np.array([row[2] for row in rows], dtype=float)
            u = np.array([row[3] for row in rows], dtype=float)
            y_pulse = y_base.copy()
            y_pulse[PULSE_START:PULSE_END + 1] += PULSE_OFFSET
            for condition, y in (("stable", y_base), ("benign_offset_pulse", y_pulse)):
                for name, scorer, threshold in (
                    ("residual_ewma", baseline_score, BASELINE_THRESHOLD),
                    ("recursive_coherence", efmw_score, EFMW_THRESHOLD),
                ):
                    alert, raw_rate = score_one(y, u, scorer, threshold)
                    writer.writerow([
                        seed, condition, name,
                        "" if alert is None else alert,
                        int(alert is not None), f"{raw_rate:.10f}",
                    ])
    print(f"Wrote {output} ({len(SEEDS)} paired seeds, two conditions).")


if __name__ == "__main__":
    main()
