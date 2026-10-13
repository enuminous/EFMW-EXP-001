# EFMW-EXP-002: Benign-Transient Specificity Screen

**Status:** Protocol frozen, then executed using the frozen code in this directory.  
**Scope:** Synthetic negative-control follow-up to [EFMW-EXP-001](https://github.com/enuminous/EFMW-EXP-001).

EXP-001 showed a median warning-lead gain of 16.5 timesteps on its synthetic degradation benchmark, with raw pre-onset exceedance rates of 6.15% for recursive coherence and 5.13% for residual EWMA. This experiment asks a different question: when no degradation exists, how often does a brief benign measurement offset become a sustained alert?

The simulator, monitor equations, thresholds, and three-sample alert rule are copied unchanged from EXP-001 commit [`048e263`](https://github.com/enuminous/EFMW-EXP-001/commit/048e26372279de6da70e0db71033a883dba67b87). We run 80 held-out seeds (2001–2080) in a stable null condition and in a paired condition with a synthetic `+0.05` observed-state offset at steps 220–231. No degradation is present and no thresholds are refit. Full design, endpoints, and decision criteria are frozen in [protocol.md](protocol.md).

## Result

The frozen primary screen **failed**. In the benign-pulse condition, recursive coherence produced a sustained false alarm in 66/80 runs (82.5%), exceeding the 10% absolute limit. Residual EWMA alarmed in 78/80 runs (97.5%); the paired EFMW-minus-baseline difference was −15 percentage points (bootstrap 95% interval −25.0 to −6.25 points; exact two-sided McNemar p=0.00418). Stable-condition incidence was also 82.5% for recursive coherence and 97.5% for residual EWMA.

The same counts in the stable and pulse conditions mean the injected pulse did not change aggregate alarm incidence in this run. The key result is the high sustained-alarm incidence even when degradation is disabled. EXP-001's raw pointwise exceedance rates do not answer this longer-horizon operational question. Both methods need a defensible alert policy and calibration against representative external data before an operational pilot; this synthetic screen does not establish what such a policy should be.

See the full per-seed [results.csv](results.csv) and rerun using:

```sh
python run.py
python analyze.py
```

This is a synthetic robustness screen, not field validation. The sensor-offset pulse is a controlled perturbation, not evidence about any particular utility, power plant, industrial control system, or healthcare device. Passing would justify a better external-data test; it would not establish operational suitability.
