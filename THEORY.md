# EFMW-EXP-001 Theory Freeze

## Primary claim

On the frozen synthetic partially observed sequential-control benchmark, the frozen EFMW-style
recursive coherence monitor will provide earlier warning of impending physical-control degradation
than a conventional absolute-residual EWMA monitor while maintaining a comparable raw false-positive
rate and comparable computational cost.

This is a proof-of-method claim about this benchmark. It is **not** a validation of the full EFMW
physical theory or the canonical EFMW root field equation.

## Shared model residual

r_t = y_t - (0.82*y_(t-1) + u_t)

## Conventional baseline monitor

B_t = 0.90*B_(t-1) + 0.10*abs(r_t)

Frozen threshold:

B_threshold = 0.0455502027202869

## EFMW-style recursive coherence monitor

M_t = 0.97*M_(t-1) + 0.03*r_t

C_t = abs(M_t)

Frozen threshold:

C_threshold = 0.00834791535743751

The EFMW-specific hypothesis tested here is that persistent signed inconsistency accumulated
recursively contains earlier degradation information than magnitude-only residual monitoring.

## Alert rule

An alert is registered at the first sample at which the relevant score exceeds its frozen threshold
for 3 consecutive samples.

For lead-time scoring, the first sustained alert at or after hidden degradation onset is used.
Pre-onset threshold exceedances are scored separately as false positives.

## Physical-failure definition

Hidden degradation begins at a seed-determined integer onset in [140, 199].
It increases linearly for 120 steps. Physical failure time is onset + 120.

The monitors do not observe the onset, degradation state, or physical-failure time.
