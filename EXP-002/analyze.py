#!/usr/bin/env python3
"""Analyze EFMW-EXP-002 outcomes without changing frozen criteria."""
import csv
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "results.csv"
SEEDS = list(range(2001, 2081))


def wilson(successes, n, z=1.959963984540054):
    p = successes / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return center - half, center + half


def exact_mcnemar_p(a_only, b_only):
    n = a_only + b_only
    if n == 0:
        return 1.0
    k = min(a_only, b_only)
    tail = sum(math.comb(n, j) for j in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def main():
    if not DATA.exists():
        raise SystemExit("Run python run.py first.")
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    result = {}
    for row in rows:
        key = (row["condition"], row["monitor"], int(row["seed"]))
        result[key] = {
            "alert": int(row["false_alarm"]),
            "raw": float(row["raw_pointwise_exceedance_rate"]),
        }

    pulse_e = np.array([result[("benign_offset_pulse", "recursive_coherence", s)]["alert"] for s in SEEDS])
    pulse_b = np.array([result[("benign_offset_pulse", "residual_ewma", s)]["alert"] for s in SEEDS])
    stable_e = np.array([result[("stable", "recursive_coherence", s)]["alert"] for s in SEEDS])
    stable_b = np.array([result[("stable", "residual_ewma", s)]["alert"] for s in SEEDS])
    for condition in ("stable", "benign_offset_pulse"):
        for monitor in ("residual_ewma", "recursive_coherence"):
            alerts = [
                int(row["first_sustained_alert"])
                for row in rows
                if row["condition"] == condition and row["monitor"] == monitor
                and row["first_sustained_alert"]
            ]
            print(f"{condition}_{monitor}_first_alert_median_timestep={np.median(alerts) if alerts else 'none'}")
    discordant_e = int(np.sum((pulse_e == 1) & (pulse_b == 0)))
    discordant_b = int(np.sum((pulse_e == 0) & (pulse_b == 1)))
    risk_diff = pulse_e - pulse_b
    rng = np.random.default_rng(230047)
    boot = np.array([
        np.mean(rng.choice(risk_diff, size=len(risk_diff), replace=True))
        for _ in range(10000)
    ])
    ci = np.quantile(boot, [0.025, 0.975])
    n = len(SEEDS)
    e_inc, b_inc = float(pulse_e.mean()), float(pulse_b.mean())
    passed = (e_inc <= 0.10) and (e_inc - b_inc <= 0.05)

    print(f"n_per_condition={n}")
    print(f"pulse_efmw_false_alarm_incidence={pulse_e.sum()}/{n} ({e_inc:.3%})")
    print(f"pulse_baseline_false_alarm_incidence={pulse_b.sum()}/{n} ({b_inc:.3%})")
    print(f"pulse_paired_risk_difference={e_inc - b_inc:.3%}")
    print(f"paired_risk_difference_bootstrap_95_ci=[{ci[0]:.3%}, {ci[1]:.3%}]")
    print(f"mcnemar_discordant_efmw_only={discordant_e}")
    print(f"mcnemar_discordant_baseline_only={discordant_b}")
    print(f"mcnemar_exact_two_sided_p={exact_mcnemar_p(discordant_e, discordant_b):.8g}")
    print(f"stable_efmw_false_alarm_incidence={stable_e.sum()}/{n} ({stable_e.mean():.3%})")
    print(f"stable_baseline_false_alarm_incidence={stable_b.sum()}/{n} ({stable_b.mean():.3%})")
    for condition in ("stable", "benign_offset_pulse"):
        for monitor in ("residual_ewma", "recursive_coherence"):
            raw = [result[(condition, monitor, s)]["raw"] for s in SEEDS]
            print(f"{condition}_{monitor}_mean_raw_exceedance_rate={np.mean(raw):.5%}")
    print("PRIMARY_OUTCOME=" + ("passed" if passed else "failed"))
    print("Criterion: EFMW pulse-condition false-alarm incidence <=10% and paired excess <=5 percentage points.")


if __name__ == "__main__":
    main()
