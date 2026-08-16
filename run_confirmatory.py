#!/usr/bin/env python3
from pathlib import Path
import csv, time, numpy as np
from simulator import simulate
from monitors import baseline_score, efmw_score, BASELINE_THRESHOLD, EFMW_THRESHOLD, first_sustained_after

ROOT=Path(__file__).resolve().parent
WARMUP=20

def seeds():
    return [int(x) for x in (ROOT/"CONFIRMATORY_SEEDS_FROZEN.txt").read_text().split()]

rows_out=[]
raw_out=[]
for seed in seeds():
    rows=simulate(seed)
    y=np.array([r[2] for r in rows]); u=np.array([r[3] for r in rows])
    onset=rows[0][5]; failure=rows[0][6]

    t0=time.perf_counter_ns()
    b=baseline_score(y,u)
    t1=time.perf_counter_ns()
    c=efmw_score(y,u)
    t2=time.perf_counter_ns()

    tb=first_sustained_after(b,BASELINE_THRESHOLD,onset)
    tc=first_sustained_after(c,EFMW_THRESHOLD,onset)
    lb=failure-tb if tb is not None else -999
    lc=failure-tc if tc is not None else -999
    fb=float(np.mean(b[WARMUP:onset] > BASELINE_THRESHOLD))
    fc=float(np.mean(c[WARMUP:onset] > EFMW_THRESHOLD))

    rows_out.append([seed,onset,failure,tb if tb is not None else "",tc if tc is not None else "",
                     lb,lc,lc-lb,fb,fc,t1-t0,t2-t1])
    for i,r in enumerate(rows):
        raw_out.append([*r,b[i],c[i]])

with (ROOT/"RAW_DATA"/"confirmatory_trials.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["seed","time","observed_state","control_input","latent_degradation",
      "degradation_onset","physical_failure_time","physical_failure_flag","baseline_score","efmw_score"])
    w.writerows(raw_out)

with (ROOT/"PROCESSED_DATA"/"confirmatory_summary.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["seed","degradation_onset","failure_time","baseline_detection_time",
      "efmw_detection_time","baseline_lead_time","efmw_lead_time","paired_lead_gain",
      "baseline_raw_fpr","efmw_raw_fpr","baseline_runtime_ns","efmw_runtime_ns"])
    w.writerows(rows_out)

print("Confirmatory execution complete. Data are now unsealed and must not be used to alter the frozen packet.")
