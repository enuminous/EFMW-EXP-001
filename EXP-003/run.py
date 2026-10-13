#!/usr/bin/env python3
"""Run frozen EFMW-EXP-003 threshold calibration and holdout evaluation."""
import csv
from pathlib import Path

import numpy as np

from monitors import (
    WARMUP,
    baseline_score,
    efmw_score,
    first_sustained_after,
    max_sustained_score,
)
from simulator import simulate

ROOT = Path(__file__).resolve().parent
CALIBRATION_SEEDS = range(3001, 3081)
NULL_SEEDS = range(4001, 4081)
DEGRADATION_SEEDS = range(5001, 5081)
TARGET_FAR = 0.05
HOLDOUT_MAX_FAR = 0.10
PRIMARY_GAIN = 10.0

MONITORS = {
    "residual_ewma": baseline_score,
    "recursive_coherence": efmw_score,
}


def series(seed, null):
    rows = simulate(seed, null_degradation=null)
    y = np.array([row[2] for row in rows], dtype=float)
    u = np.array([row[3] for row in rows], dtype=float)
    onset, failure = rows[0][5], rows[0][6]
    return y, u, onset, failure


def main():
    calibration_maxima = {name: [] for name in MONITORS}
    for seed in CALIBRATION_SEEDS:
        y, u, _, _ = series(seed, null=True)
        for name, scorer in MONITORS.items():
            calibration_maxima[name].append(max_sustained_score(scorer(y, u)))

    # 76th value (1-indexed) gives the upper 5% empirical tail for n=80.
    thresholds = {
        name: float(np.sort(values)[75])
        for name, values in calibration_maxima.items()
    }
    cal_far = {
        name: float(np.mean(np.asarray(values) > thresholds[name]))
        for name, values in calibration_maxima.items()
    }
    with (ROOT / "calibration.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["monitor", "threshold", "calibration_false_alarm_incidence", "target_false_alarm_incidence"])
        for name in MONITORS:
            w.writerow([name, f"{thresholds[name]:.16g}", f"{cal_far[name]:.6f}", TARGET_FAR])

    with (ROOT / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "seed", "condition", "monitor", "degradation_onset", "failure_time",
            "first_sustained_alert", "alert_before_onset", "actionable_warning",
            "lead_time", "false_alarm", "raw_pointwise_exceedance_rate",
        ])
        for condition, seeds, is_null in (
            ("heldout_null", NULL_SEEDS, True),
            ("heldout_degradation", DEGRADATION_SEEDS, False),
        ):
            for seed in seeds:
                y, u, onset, failure = series(seed, null=is_null)
                for name, scorer in MONITORS.items():
                    score = scorer(y, u)
                    alert = first_sustained_after(score, thresholds[name])
                    before = alert is not None and alert < onset
                    actionable = alert is not None and onset <= alert < failure
                    lead = failure - alert if actionable else -999
                    raw_rate = float(np.mean(score[WARMUP:] > thresholds[name]))
                    w.writerow([
                        seed, condition, name, onset, failure,
                        "" if alert is None else alert,
                        int(before), int(actionable), lead,
                        int(alert is not None) if is_null else "",
                        f"{raw_rate:.10f}",
                    ])
    print("Thresholds frozen from 80 calibration null seeds:")
    for name in MONITORS:
        print(f"{name},{thresholds[name]:.16g},calibration_FAR={cal_far[name]:.3%}")
    print("Wrote calibration.csv and 320 per-seed evaluation rows to results.csv.")


if __name__ == "__main__":
    main()
