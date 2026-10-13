# EFMW-EXP-002 protocol freeze

**Scope:** A synthetic specificity screen for the two monitors frozen in EFMW-EXP-001.
**Question:** With no latent degradation, does a brief benign sensor offset cause the recursive-coherence monitor to issue more sustained false alarms than residual EWMA?
**Evidence boundary:** This can test behavior on the specified synthetic generator only. It does not validate an energy control system, field sensor, operator workflow, or commercial product.

## Frozen inputs

- Simulator equations: `simulator.py`, copied without change from EFMW-EXP-001 at commit `048e26372279de6da70e0db71033a883dba67b87`.
- Monitor equations, sustained-alert rule, and thresholds: `monitors.py`, copied without change from that same commit.
- Baseline threshold: `0.0455502027202869`.
- Recursive-coherence threshold: `0.00834791535743751`.
- Sustained alert: score strictly above threshold for 3 consecutive samples; scan begins at timestep 20.
- Independent seeds: integers 2001 through 2080. For each seed, use the same generated trace in both conditions and for both monitors.
- Conditions: (A) no degradation, no injection; (B) no degradation, with an additive `+0.05` observed-state offset at timesteps 220–231 inclusive. This pulse is a constructed benign telemetry perturbation, not a model of a particular field sensor.
- Latent degradation is disabled in both conditions. Thresholds are not re-estimated or adjusted.

## Endpoints and decision rules

Primary endpoint: in the pulse condition, compare the proportion of runs with any sustained false alarm for recursive coherence and residual EWMA. The paired risk difference is `EFMW incidence - EWMA incidence`.

Primary screen passes only if both (1) EFMW false-alarm incidence is at most 10% (8/80) and (2) its paired excess incidence over EWMA is at most 5 percentage points (4/80). These are project screening limits, not externally validated safety or industry standards. Any other outcome fails this screen; no tuning or rescue analysis is permitted.

Secondary endpoints: stable-condition sustained false-alarm incidence; raw pointwise exceedance rate over timesteps 20–499 in each condition; first sustained-alarm time; paired risk-difference bootstrap interval and exact two-sided McNemar test. Report all per-seed outcomes.

## Anti-circularity and audit

This is a follow-on experiment, not a new independent confirmation of EXP-001's early-warning result: it reuses EXP-001's generator, monitor definitions, and thresholds. Its only new intervention is the explicitly defined benign sensor-offset pulse. Seed range 2001–2080 was not used in EXP-001. All conditions, thresholds, endpoints, and decision limits are recorded before this run. A failed screen remains a failed screen; no threshold or injection changes are allowed in this version.

## Reproduction

From this directory, run:

```sh
python run.py
python analyze.py
```

Requires Python 3.10+ and NumPy. `run.py` writes `results.csv`; `analyze.py` reports aggregate results from that file.
