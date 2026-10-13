# EFMW-EXP-003: Matched Whole-Run False-Alarm Budget

**Status:** Protocol frozen and executed.  
**Scope:** Synthetic follow-up; not physical or field validation.

EXP-001 found an early-warning gain using thresholds calibrated on pre-onset samples. EXP-002 then showed that raw pointwise exceedance rates did not control the probability of a sustained alert over a 480-step no-degradation horizon. EXP-003 asks whether the early-warning comparison survives when each monitor is calibrated on separate no-degradation traces to the same whole-run false-alarm budget.

Each monitor receives its own threshold calibrated to a 5% empirical whole-run false-alarm target on seeds 3001–3080. Thresholds are then frozen and evaluated on distinct no-degradation seeds 4001–4080 and degradation seeds 5001–5080. The experiment reuses the EXP-001 synthetic generator and monitor equations; it adds independent seed splits and operationally aligned threshold calibration. Read [protocol.md](protocol.md) for exact endpoints and failure conditions.

## Result

The frozen screen **passed**. The separate calibration set produced thresholds of 0.0542015183 for residual EWMA and 0.0136069679 for recursive coherence, each with 5.0% calibration false-alarm incidence. On held-out null runs, incidence was 6/80 (7.5%) for EWMA and 2/80 (2.5%) for recursive coherence. On held-out degradation runs, actionable warnings occurred in 65/80 (81.25%) and 77/80 (96.25%), respectively. Median paired lead gain across all 80 degradation runs was 41.5 timesteps (bootstrap 95% interval [37.0, 47.0]); paired detection discordances favored recursive coherence (15 vs. 3; exact McNemar p=0.00754).

These are results on the same synthetic generator as EXP-001. Threshold calibration was changed to match a whole-run false-alarm budget, so this is a new operating-point comparison, not a revision of EXP-001's frozen result or an independent replication on real data. See [calibration.csv](calibration.csv) for the frozen thresholds and [results.csv](results.csv) for every per-seed holdout outcome (80 seeds per condition for each monitor). Reproduce with:

```sh
python run.py
python analyze.py
```

This is not a model of a named utility or plant, and it does not establish deployment performance. A pass would support only the specified synthetic comparison.
