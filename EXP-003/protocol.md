# EFMW-EXP-003 protocol freeze

**Question:** Does recursive-coherence monitoring retain an early-warning advantage over residual EWMA when each monitor's threshold is calibrated to the same whole-run false-alarm budget?
**Scope:** Synthetic follow-up to EFMW-EXP-001 and EFMW-EXP-002. No physical or field validation is attempted.

## Frozen methods and split

- Simulator and scoring equations are those used in EXP-001 (source revision `048e26372279de6da70e0db71033a883dba67b87`).
- Both monitors use the same 3-consecutive-sample alert rule and warmup begins at step 20.
- Calibrate each monitor's threshold separately on 80 no-degradation traces, seeds 3001–3080.
- Whole-run false-alarm budget: 5%. For each calibration trace, calculate its maximum sliding-window minimum score over steps 20–499. Set the threshold to the 76th ordered value (1-indexed) among the 80 values, with alerts defined by strict `score > threshold`.
- Freeze both thresholds after calibration. Do not use holdout data to revise them.
- Evaluate on two disjoint holdouts: 80 no-degradation traces (seeds 4001–4080) and 80 degradation traces (seeds 5001–5080).
- Use common seeds only to pair monitor comparisons within a condition. Calibration and evaluation seed ranges do not overlap.

## Endpoints and decision criteria

Primary statistic: median paired warning-lead gain on all 80 degradation traces. For each monitor, lead is `failure_time - first_sustained_alert_time` only when its first alert occurs at or after degradation onset and before failure; otherwise lead is `-999`. Thus a pre-onset alarm counts as a missed actionable warning, not a success.

The project screen passes only if all three conditions hold: (1) median paired lead gain is at least 10 timesteps; (2) held-out whole-run false-alarm incidence is at most 10% for each monitor; and (3) recursive-coherence actionable warning detection is at least 60% of degradation runs. These are predeclared project screening thresholds, not industry safety standards.

Report calibrated thresholds, calibration false-alarm incidence, held-out null false-alarm incidence, all per-seed detection/lead outcomes, median gain with a 95% paired bootstrap interval (10,000 resamples, RNG seed 230048), actionable detection rates, and exact two-sided McNemar test for the paired actionable-detection indicators. No rescue tuning is permitted.

## Anti-circularity and limitations

This is not an independent simulator replication: it reuses the EXP-001 generator and monitor definitions. Its new feature is the separate no-degradation threshold calibration against a whole-run alert budget. EXP-002's results motivated the endpoint, but no EXP-002 outcomes or seeds enter calibration or evaluation. A pass would show only that the frozen algorithms satisfy this specified synthetic screen. External streaming data, realistic plant dynamics, operator consequences, and hardware deployment remain untested.

## Reproduction

Run `python run.py` followed by `python analyze.py` from this directory. Requires Python 3.10+ and NumPy.
