#!/usr/bin/env python3
"""Analyze frozen EFMW-EXP-003 holdout without tuning."""
import csv
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 80
SEEDS = {
    "heldout_null": list(range(4001, 4081)),
    "heldout_degradation": list(range(5001, 5081)),
}
MONITORS = ("residual_ewma", "recursive_coherence")


def mcnemar_exact(a_only, b_only):
    n = a_only + b_only
    if not n:
        return 1.0
    k = min(a_only, b_only)
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / (2 ** n))


def main():
    with (ROOT / "results.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    data = {}
    for r in rows:
        data[(r["condition"], r["monitor"], int(r["seed"]))] = r

    print("whole_run_false_alarm_incidence (heldout null)")
    null_far = {}
    for monitor in MONITORS:
        vals = np.array([
            int(data[("heldout_null", monitor, s)]["false_alarm"])
            for s in SEEDS["heldout_null"]
        ])
        null_far[monitor] = float(vals.mean())
        print(f"{monitor}={vals.sum()}/{N} ({vals.mean():.3%})")

    actionable = {}
    leads = {}
    print("actionable_warning_detection (heldout degradation)")
    for monitor in MONITORS:
        rs = [data[("heldout_degradation", monitor, s)] for s in SEEDS["heldout_degradation"]]
        actionable[monitor] = np.array([int(r["actionable_warning"]) for r in rs])
        leads[monitor] = np.array([int(r["lead_time"]) for r in rs])
        detected_leads = leads[monitor][leads[monitor] != -999]
        print(f"{monitor}_actionable_warnings={actionable[monitor].sum()}/{N} ({actionable[monitor].mean():.3%})")
        print(f"{monitor}_median_lead_all_runs={np.median(leads[monitor]):.1f}")
        print(f"{monitor}_median_lead_when_detected={np.median(detected_leads) if len(detected_leads) else 'none'}")

    gain = leads["recursive_coherence"] - leads["residual_ewma"]
    rng = np.random.default_rng(230048)
    boot = np.array([
        np.median(rng.choice(gain, size=N, replace=True))
        for _ in range(10000)
    ])
    ci = np.quantile(boot, [0.025, 0.975])
    med_gain = float(np.median(gain))
    e = actionable["recursive_coherence"]
    b = actionable["residual_ewma"]
    e_only = int(np.sum((e == 1) & (b == 0)))
    b_only = int(np.sum((e == 0) & (b == 1)))
    print(f"median_paired_lead_gain={med_gain:.1f}")
    print(f"median_gain_bootstrap_95_ci=[{ci[0]:.1f}, {ci[1]:.1f}]")
    print(f"mcnemar_efmw_only={e_only},baseline_only={b_only},p={mcnemar_exact(e_only,b_only):.8g}")

    passed = (
        med_gain >= 10.0
        and null_far["residual_ewma"] <= 0.10
        and null_far["recursive_coherence"] <= 0.10
        and actionable["recursive_coherence"].mean() >= 0.60
    )
    print("PRIMARY_OUTCOME=" + ("passed" if passed else "failed"))


if __name__ == "__main__":
    main()
