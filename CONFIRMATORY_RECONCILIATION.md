# EFMW-EXP-001 Confirmatory Reconciliation

**Reconciled:** 2026-10-12  
**Source revision:** `main` at `e14ea2aebf438f5006b62a7e8d1380efb6388119`  
**Scope:** Reproduction of the frozen synthetic benchmark and reconciliation of later repository claims.

## Result

The checked-in simulator, monitor code, frozen confirmatory seeds, and frozen analysis were run without changing thresholds, equations, endpoints, exclusions, or seeds. Their SHA-256 hashes match the corresponding values in `ANALYSIS_FREEZE_SHA256.txt` and `MANIFEST_SHA256.txt`.

| Measure | Reproduced value |
|---|---:|
| Confirmatory seeds | 40 (1001-1040) |
| Baseline median warning lead | 59.0 timesteps |
| EFMW median warning lead | 78.0 timesteps |
| Median paired gain | +16.5 timesteps |
| Preregistered pass threshold | +10 timesteps |
| Bootstrap 95% CI for median paired gain | [3.5, 18.5] |
| Two-sided Wilcoxon signed-rank p | 0.0039232744 |
| EFMW win rate | 30/40 (75%) |
| Baseline raw pre-onset FPR | 5.1311% |
| EFMW raw pre-onset FPR | 6.1506% |
| Single-run median compute-time ratio, EFMW/baseline | 1.129x |

The primary frozen criterion is **confirmed within this synthetic benchmark**. The timing ratio is a one-run, software-environment-sensitive measurement and is not evidence of hardware or deployment efficiency.

## What changed and what remains frozen

The v1.0 design packet was deliberately frozen before confirmatory execution. Its status fields describe that freeze-time state, not the present state of the repository. The preregistered design remains unchanged; confirmatory outputs have now been added. The existing `RESULTS.csv` agrees with the reproduction to its displayed precision.

The new `RAW_DATA/confirmatory_trials.csv` contains the time-series output for all 40 seeds, including monitor scores. `PROCESSED_DATA/confirmatory_summary.csv` contains the per-seed alert times, lead times, paired gains, FPRs, and timing observations. The commands in the README regenerate these files and the analysis.

## Correction to the later DOCX report

The DOCX report remains a dated historical report. Section 9 accurately describes the repository state when that report was prepared, but its statement that confirmatory artifacts were not yet committed is superseded by the files now published.

Section 7's separate RMS-EWMA/CUSUM comparison has no corresponding frozen runner, per-seed outputs, or analysis artifacts in this repository, so it is not independently reproducible here and is not part of the canonical result. Its EFMW FPR of 6.05% conflicts with the reproduced frozen-run value of 6.1506%; its 1.002x runtime figure also does not match this reproduction's single-run median of 1.129x. Treat those section 7 figures as unverified exploratory claims, not as confirmatory results. The canonical frozen comparison is EFMW versus residual EWMA, summarized above and in `RESULTS.csv`.

## Evidence boundary

This is a synthetic, partially observed control-degradation benchmark. It supports a narrow proof-of-method result for this simulator and scoring protocol. It does not validate EFMW physics generally, the canonical EFMW field equation, real energy infrastructure, customer adoption, or regulatory/safety certification.

No prediction, threshold, seed, equation, or scoring rule was changed in this reconciliation.
