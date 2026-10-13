#!/usr/bin/env python3
"""Monitor equations from EFMW-EXP-001; thresholds calibrated in this experiment."""
import numpy as np

SUSTAINED_K = 3
WARMUP = 20


def residuals(y, u):
    y = np.asarray(y, dtype=float)
    u = np.asarray(u, dtype=float)
    prev = np.r_[0.0, y[:-1]]
    return y - (0.82 * prev + u)


def baseline_score(y, u):
    r = residuals(y, u)
    b = np.zeros_like(r)
    for t in range(1, len(r)):
        b[t] = 0.90 * b[t - 1] + 0.10 * abs(r[t])
    return b


def efmw_score(y, u):
    r = residuals(y, u)
    m = np.zeros_like(r)
    c = np.zeros_like(r)
    for t in range(1, len(r)):
        m[t] = 0.97 * m[t - 1] + 0.03 * r[t]
        c[t] = abs(m[t])
    return c


def first_sustained_after(score, threshold, start=WARMUP, k=SUSTAINED_K):
    above = np.asarray(score) > threshold
    for t in range(start, len(score) - k + 1):
        if bool(np.all(above[t:t + k])):
            return t
    return None


def max_sustained_score(score, start=WARMUP, k=SUSTAINED_K):
    values = np.asarray(score, dtype=float)[start:]
    windows = np.lib.stride_tricks.sliding_window_view(values, k)
    return float(np.max(np.min(windows, axis=1)))
