# EFMW-EXP-003: 2x2 control and variance-fault stress test, run on the original code

Prepared by Garret Sutherland (MirrorEthic), October 28 2026.

## What this is
1. A reproduction of EFMW-EXP-003 exactly as published (`EXP-003/run.py`, `EXP-003/analyze.py`, unchanged).
2. The 2x2 control requested by the author: {absolute value then average, average signed residuals then absolute value} x {decay 0.90, decay 0.97}, using the published `monitors.py` and `simulator.py`, calibration rule, alert rule, seeds, endpoint, bootstrap and McNemar test. One arm (abs, 0.97) is the preregistered ablation A2 in `ABLATIONS.csv`.
3. A **new stress test that is not part of the preregistration**: a zero-mean variance fault, added by Garret Sutherland. It is a patch to a copy of `simulator.py` (`variance_fault.patch`). The published `EXP-003/` files are never modified.

## Source and environment
- Repository: github.com/enuminous/EFMW-EXP-001, commit `8f11bc5320cffb10932d5d31da7072d6ad4f65c2`. `EXP-003/` is byte-identical to commit `65134993069c2dc0c46a60fccd8bcdb2d951cdd3` (the commit linked in the request) and to `aa7cc9183220df1eb39537107f38cbce8f51e515` (the commit that added EXP-003). See `provenance.txt`.
- Container: `docker.io/library/python@sha256:97aadec60ff8a5dae2a9790f626a3e4cadd2cc3a14891d385d2ef8fc889579d7`, Python 3.11.18, x86_64, numpy 2.4.6 (only package installed). CPU only, no network during the run. Wall time about 5 s.

## Reproduce
```sh
git clone https://github.com/enuminous/EFMW-EXP-001 && cd EFMW-EXP-001
git checkout 8f11bc5320cffb10932d5d31da7072d6ad4f65c2
pip install numpy==2.4.6
mkdir audit && cp /path/to/exp003_2x2_package.py /path/to/variance_fault.patch /path/to/run_package.sh audit/
sh audit/run_package.sh        # writes everything to repro_out/
```
`run_package.sh` records provenance and environment, runs the published `run.py` and `analyze.py`, checks the CSVs (below), then runs `exp003_2x2_package.py`. Note: `run.py` rewrites `EXP-003/calibration.csv` and `results.csv` in the working tree; `git checkout -- EXP-003` restores them.

## Calibration (all four arms)
Each arm is calibrated separately with the EXP-003 rule: on null seeds 3001-3080, take each trace's maximum over steps 20-499 of the 3-sample sliding-window minimum score; threshold = 76th ordered value (1-indexed) of the 80; alert = first 3 consecutive samples with score strictly > threshold, from step 20. Per-seed calibration maxima are in `calibration_maxima.csv`.

| Arm | Averaging | Decay | Threshold | Calibration FAR | Held-out null false alarms (seeds 4001-4080) |
|---|---|---|---|---|---|
| abs_0.90_baseline (published residual_ewma) | abs then average | 0.90 | 0.05420151828535452 | 5.0% | 6/80 (7.5%) |
| abs_0.97 (= preregistered A2) | abs then average | 0.97 | 0.04421011383162915 | 5.0% | 8/80 (10.0%) |
| signed_0.90 | signed average, then abs | 0.90 | 0.02839873873022945 | 5.0% | 1/80 (1.25%) |
| signed_0.97_efmw (published recursive_coherence) | signed average, then abs | 0.97 | 0.01360696789702808 | 5.0% | 2/80 (2.5%) |

Check: the driver's generic arms reproduce the published `baseline_score` and `efmw_score` to a maximum absolute difference of 4.2e-17 on 20 traces.

## Seed splits
Calibration nulls 3001-3080; held-out nulls 4001-4080; degradation 5001-5080. The variance-fault test uses the same degradation seeds and the same thresholds (no recalibration; the patched simulator's null path is identical to the published one, checked on all calibration seeds).

## Missed detections
As in the frozen protocol: lead = failure_time - first_alert only when onset <= first_alert < failure; otherwise lead = -999 and the run counts as a missed actionable warning. Medians are over all 80 runs with -999 included; the paired gain is per seed, arm lead minus baseline lead; bootstrap is 10,000 resamples of the 80 paired gains with RNG seed 230048. Every degradation run produced some alert in every arm (no_alert = 0); misses are pre-onset alerts or alerts at or after failure. Because -999 enters the paired differences, the variance-fault bootstrap intervals have lower bounds near -1000. The table also reports the median gain on seeds where both arms gave an actionable warning, as a sensitivity check.

## Results: mean-drift fault (published simulator, unchanged)
| Arm | Actionable /80 | Pre-onset | At/after failure | Median lead (all runs) | Median gain vs baseline [95% CI] | McNemar arm-only / baseline-only, p | Median gain, both detected (n) |
|---|---|---|---|---|---|---|---|
| abs_0.90_baseline | 65 | 3 | 12 | 16.5 | 0 | | |
| abs_0.97 (A2) | 74 | 1 | 5 | 25.0 | +2.0 [0.5, 5.0] | 10 / 1, p = 0.0117 | +2.0 (64) |
| signed_0.90 | 80 | 0 | 0 | 53.5 | +33.5 [28.5, 41.0] | 15 / 0, p = 6.1e-05 | +29.0 (65) |
| signed_0.97_efmw | 77 | 3 | 0 | 59.0 | +41.5 [37.0, 47.0] | 15 / 3, p = 0.0075 | +38.5 (62) |

## Results: zero-mean variance fault (new test, not preregistered)
Patch: the drift bias and sinusoid are replaced by process noise scaled by (1 + 1.5 d). RNG draws, onset, failure and a = 0.82 + 0.08 d are unchanged. See `variance_fault.patch`.

| Arm | Actionable /80 | Pre-onset | At/after failure | Median lead (all runs) | Median gain vs baseline [95% CI] | McNemar arm-only / baseline-only, p | Median gain, both detected (n) |
|---|---|---|---|---|---|---|---|
| abs_0.90_baseline | 77 | 3 | 0 | 58.5 | 0 | | |
| abs_0.97 | 79 | 1 | 0 | 60.5 | 0.0 [0.0, 1.5] | 3 / 1, p = 0.625 | 0.0 (76) |
| signed_0.90 | 47 | 0 | 33 | 10.0 | -50.5 [-1017, -34] | 2 / 32, p = 6.9e-08 | -24.0 (45) |
| signed_0.97_efmw | 41 | 3 | 36 | 1.0 | -61.5 [-1041, -38] | 1 / 37, p = 2.8e-10 | -24.0 (40) |

## CSV line endings (EXP-003/calibration.csv, EXP-003/results.csv)
| File | Committed (LF) sha256, bytes | Regenerated by run.py (CRLF) sha256, bytes | SHA256SUMS.txt entry |
|---|---|---|---|
| calibration.csv | ad82b1e8d7388f472fd8a3b2f94182b8944b34ac4a2530cea7c81c61f1c930c2, 183 | 77964aaf8a2170e553d98574d2bd4d73b5b50a01488a7cd842ef0da7f05c861b, 186 | 77964aaf... (matches regenerated) |
| results.csv | 93eac5c1f6b0b6f4a6782d75731b4d2ca0359c9e1f584796c66cc02ce2007b00, 23084 | 8878460b1817b164aaffd9c3b4156b372d5876f764f8a2b5f91e971c8ff88a9d, 23405 | 8878460b... (matches regenerated) |

Git blob ids of the committed files: calibration.csv 4af3084e70d3a55cddb815bc97f57a5293e8e78d, results.csv 4c357ee8799b843839105b6987a9b067bd10878c.

How equivalence was established (`csv_equivalence.txt`): the committed files contain 0 CR bytes; the regenerated files have one CR per line (3 and 321) because `csv.writer` defaults to CRLF. Stripping CR from the regenerated files gives byte-identical files (`cmp`) with the committed sha256s above; adding CR before each LF in the committed files gives exactly the SHA256SUMS.txt hashes; `git diff --ignore-cr-at-eol` is empty. The difference is line endings only. Nothing in the repository was modified; the original files are preserved.

## Files
- `exp003_2x2_package.py`, `variance_fault.patch`, `run_package.sh`: code written by the auditor.
- `calibration_4arms.csv`, `calibration_maxima.csv`, `per_seed.csv`, `results.json`: outputs.
- `provenance.txt`, `his_run_and_analyze.txt`, `csv_equivalence.txt`, `package_stdout.txt`: logs.
- `SHA256SUMS_package.txt`: hashes of the outputs and logs above.
