#!/usr/bin/env python3
from pathlib import Path
import csv, numpy as np
from scipy.stats import wilcoxon

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"PROCESSED_DATA"/"confirmatory_summary.csv"
if not DATA.exists():
    raise SystemExit("No confirmatory data found. Run run_confirmatory.py only after freeze.")

with DATA.open(newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))

gain=np.array([float(r["paired_lead_gain"]) for r in rows])
efmw=np.array([float(r["efmw_lead_time"]) for r in rows])
base=np.array([float(r["baseline_lead_time"]) for r in rows])
fpr_e=np.array([float(r["efmw_raw_fpr"]) for r in rows])
fpr_b=np.array([float(r["baseline_raw_fpr"]) for r in rows])
rt_e=np.array([float(r["efmw_runtime_ns"]) for r in rows])
rt_b=np.array([float(r["baseline_runtime_ns"]) for r in rows])

rng=np.random.default_rng(230046)
boot=np.array([np.median(rng.choice(gain,size=len(gain),replace=True)) for _ in range(10000)])
ci=np.quantile(boot,[0.025,0.975])

try:
    test=wilcoxon(gain,alternative="two-sided")
    p=float(test.pvalue)
except Exception:
    p=float("nan")

metrics={
 "n":len(rows),
 "median_baseline_lead":float(np.median(base)),
 "median_efmw_lead":float(np.median(efmw)),
 "median_paired_gain":float(np.median(gain)),
 "median_gain_ci95_low":float(ci[0]),
 "median_gain_ci95_high":float(ci[1]),
 "wilcoxon_p":p,
 "mean_baseline_raw_fpr":float(np.mean(fpr_b)),
 "mean_efmw_raw_fpr":float(np.mean(fpr_e)),
 "efmw_win_rate":float(np.mean(gain>0)),
 "median_compute_ratio":float(np.median(rt_e/rt_b)),
}
for k,v in metrics.items():
    print(f"{k},{v}")

primary = metrics["median_paired_gain"] >= 10.0
print("PRIMARY_OUTCOME," + ("confirmed" if primary else "contradicted"))
