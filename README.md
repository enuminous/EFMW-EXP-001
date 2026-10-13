# EFMW-EXP-001-v1.0

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/EFMW-EXP-001) · This repository is linked through its source; GitHub Pages is not enabled.
<!-- ENUMINOUS-NETWORK:END -->

## Recursive Coherence Early-Warning Benchmark

**Design status:** Frozen before confirmatory execution. The preregistered design, thresholds, seeds, and scoring rules remain unchanged.  
**Execution status:** Reproduced from the frozen source on 2026-10-12; the primary criterion is confirmed on the synthetic benchmark.

The full reconciliation, exact results, artifact hashes, and limitations are in [CONFIRMATORY_RECONCILIATION.md](CONFIRMATORY_RECONCILIATION.md).

### Confirmatory result

On 40 held-out synthetic control-degradation seeds (1001-1040), the recursive-coherence monitor achieved a median paired warning-lead gain of **16.5 timesteps** over residual EWMA, above the preregistered **10-timestep** criterion (95% bootstrap CI [3.5, 18.5]; two-sided Wilcoxon p=0.003923). Median lead was 78.0 timesteps for EFMW and 59.0 for baseline. EFMW's raw pre-onset false-positive rate was 6.15%, versus 5.13% for baseline. These results are synthetic benchmark evidence only.

The per-seed output and raw confirmatory time series are now published at [PROCESSED_DATA/confirmatory_summary.csv](PROCESSED_DATA/confirmatory_summary.csv) and [RAW_DATA/confirmatory_trials.csv](RAW_DATA/confirmatory_trials.csv).

### Frozen protocol

Primary frozen claim: the EFMW-style recursive coherence monitor must achieve a median paired warning-lead advantage of at least **10 timesteps** over the conventional residual EWMA monitor on 40 held-out seeds.

Calibration seeds: 101-120. Confirmatory seeds: 1001-1040.

Frozen thresholds derived only from calibration pre-onset samples:

- Baseline: 0.0455502027202869
- EFMW coherence: 0.00834791535743751

Calibration descriptive medians:

- Baseline lead: 41.0
- EFMW lead: 80.0
- Paired gain: 33.5

The freeze-time [packet metadata](packet_metadata.json) and [manifest](MANIFEST_SHA256.txt) record the original v1.0 packet state. The later DOCX report includes an exploratory efficiency comparison in section 7 that is not supported by the frozen runner's artifacts; see the reconciliation before relying on that section.

Reproduce with:

    python run_confirmatory.py
    python analysis.py

The confirmatory results are included; do not use them to tune or revise the frozen model or thresholds. The core rule remains: **EFMW receives no credit for explaining a result it did not predict.**

### Scope

This is a proof-of-method experiment for recursive coherence monitoring on a synthetic control benchmark. It is not a general experimental validation of EFMW, the canonical physical field equation, or performance in energy infrastructure.

### Follow-up specificity screen

[EFMW-EXP-002](EXP-002/README.md) reuses the frozen monitors and thresholds to measure sustained false alarms on synthetic no-degradation traces, including a brief benign sensor-offset pulse. Its preregistered absolute false-alarm criterion failed; it is not field validation.
