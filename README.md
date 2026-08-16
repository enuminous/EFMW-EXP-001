# EFMW-EXP-001-v1.0
## Recursive Coherence Early-Warning Benchmark

Status: **FROZEN BEFORE CONFIRMATORY EXECUTION**

Primary frozen claim:
The EFMW-style recursive coherence monitor must achieve a median paired warning-lead advantage
of at least **10 timesteps** over the conventional residual EWMA monitor on 40 held-out seeds.

Calibration seeds: 101-120.
Confirmatory seeds: 1001-1040.

Frozen thresholds derived only from calibration pre-onset samples:
- baseline: 0.0455502027202869
- EFMW coherence: 0.00834791535743751

Calibration descriptive medians:
- baseline lead: 41.0
- EFMW lead: 80.0
- paired gain: 33.5

The confirmatory seeds have not been executed in construction of this distribution.

To execute after accepting the freeze:

    python run_confirmatory.py
    python analysis.py

Core rule:
**EFMW receives no credit for explaining a result it did not predict.**

Scope:
This is a proof-of-method benchmark for recursive coherence monitoring. It is not a general
experimental validation of EFMW or of the canonical EFMW physical field equation.
