# EFMW-EXP-001 Analysis Freeze

## Confirmatory sample
40 frozen held-out seeds: 1001 through 1040 inclusive.

These seeds SHALL NOT be used for calibration, tuning, threshold setting, equation selection,
or prediction revision before the packet is unsealed for confirmatory execution.

## Primary endpoint
Paired lead-time gain:

gain_i = EFMW_lead_i - baseline_lead_i

Primary statistic = median(gain_i) across confirmatory seeds.

Primary success criterion:
median paired lead-time gain >= 10 timesteps.

## Lead time
lead = physical_failure_time - first_sustained_alert_time

If no post-onset sustained alert occurs, lead is assigned -999 for deterministic scoring.
Negative lead indicates detection after physical failure.

## False-positive rate
Raw pre-onset FPR is the fraction of score samples exceeding the frozen threshold from
warmup step 20 through onset-1. This is distinct from sustained-alert incidence.

## Secondary endpoints
- median EFMW warning lead >= 55 timesteps;
- EFMW raw pre-onset FPR in [0.03, 0.07];
- baseline raw pre-onset FPR in [0.03, 0.07];
- EFMW beats baseline lead time on >= 60% of confirmatory seeds;
- median monitor compute-time ratio EFMW/baseline <= 1.50.

## Statistical reporting
Report:
- all 40 per-seed paired results;
- medians and interquartile ranges;
- two-sided Wilcoxon signed-rank test for paired lead-time differences where defined;
- bootstrap 95% CI for median paired gain using 10,000 resamples with RNG seed 230046;
- raw FPRs;
- win rate;
- runtime ratio.

Statistical significance does not override the frozen primary success criterion.

## Failure classes
confirmed
partially_confirmed
contradicted
indeterminate
protocol_failure

## No rescue
No thresholds, equations, seeds, endpoint definitions, exclusions, or scoring rules may change
after freeze. Any modification requires EFMW-EXP-001-v2.0 or later.
