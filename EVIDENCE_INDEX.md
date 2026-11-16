# EXP-001–003 evidence index

| Record | Evidence and disposition |
|---|---|
| [EXP-001 frozen reconciliation](CONFIRMATORY_RECONCILIATION.md) | On 40 held-out synthetic seeds, the median paired gain over residual EWMA was **+16.5 timesteps**. Use the linked frozen inputs and per-seed outputs for this comparison. The older DOCX availability note predates the published outputs. Its section 7 RMS-EWMA/CUSUM and runtime figures remain exploratory and unverified. [EFMW-FULL](https://github.com/enuminous/EFMW-FULL/blob/df1117ebb00d7de5b89cece5af67943a6cfde9c5/README.md) preserves a historical transcription and duplicated layouts. |
| [EXP-002 benign pulse](EXP-002/README.md) | **FAIL** on the frozen whole-run false-alarm gate. Recursive coherence alarmed on **66/80** benign-pulse runs. |
| [EXP-003 frozen mean drift](EXP-003/README.md) | **PASS** on the specified synthetic mean-drift comparison with a matched whole-run calibration target. Median paired gain **+41.5 timesteps**. Actionable warnings were 77/80 versus 65/80 for the baseline. |
| [External four-arm audit](EXP-003/audits/2026-10-28-garret/README.md) | The supplied data reproduce the mean-drift result. The signed .90 arm gives +33.5 timesteps on mean drift. In the exploratory variance-fault extension, signed .97 gave **41/80** actionable warnings versus **77/80** for absolute .90. These outcomes are specific to their fault classes and comparisons. |

The archive distinguishes the recorded external execution from recomputation of its supplied data. Broad robustness, real-world performance, and physical confirmation remain unresolved. See the [scientific validation roadmap](https://github.com/enuminous/papers/blob/cc04b04b953a14aefb2bf2f58041e99b4820a1ab/EFMW-Scientific-Validation-Roadmap-2026-11-15.md) for open validation gates.
