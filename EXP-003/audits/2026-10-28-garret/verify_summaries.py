"""Verify archived summaries from CSV data; does not import or run audit/simulator code."""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'attachments'


def csv_rows(name):
    with (DATA / name).open(newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    for line in (ROOT / 'SHA256SUMS_attachments.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    rows = csv_rows('per_seed.csv')
    maxima = csv_rows('calibration_maxima.csv')
    summary = json.loads((DATA / 'results.json.txt').read_text())
    assert len(rows) == 960 and len(maxima) == 320
    assert len({(r['condition'], r['seed'], r['arm']) for r in rows}) == 960
    for arm, expected in summary['arms'].items():
        cal = [r for r in maxima if r['arm'] == arm]
        assert sorted(int(r['seed']) for r in cal) == list(range(3001, 3081))
        values = [float(r['max_sliding_min_score_steps20_499']) for r in cal]
        threshold = sorted(values)[75]
        assert math.isclose(threshold, expected['threshold'], rel_tol=1e-13)
        assert sum(v > threshold for v in values) / 80 == expected['calibration_FAR']
        null = [r for r in rows if r['condition'] == 'heldout_null' and r['arm'] == arm]
        assert sorted(int(r['seed']) for r in null) == list(range(4001, 4081))
        assert sum(r['outcome'] == 'false_alarm' for r in null) == expected['heldout_null_false_alarms']
    for fault, arms in summary['faults'].items():
        base = {r['seed']: r for r in rows if r['condition'] == fault and r['arm'] == 'abs_0.90_baseline'}
        for arm, expected in arms.items():
            selected = sorted((r for r in rows if r['condition'] == fault and r['arm'] == arm), key=lambda r: int(r['seed']))
            assert [int(r['seed']) for r in selected] == list(range(5001, 5081))
            for r in selected:
                a = float(r['first_sustained_alert']) if r['first_sustained_alert'] else None
                on, fail = int(r['onset']), int(r['failure'])
                outcome = 'no_alert' if a is None else 'pre_onset_alert' if a < on else 'actionable' if a < fail else 'alert_at_or_after_failure'
                assert outcome == r['outcome']
                assert float(r['lead']) == (fail - a if outcome == 'actionable' else -999)
            counts = Counter(r['outcome'] for r in selected)
            for outcome in ('actionable', 'pre_onset_alert', 'alert_at_or_after_failure', 'no_alert'):
                assert counts[outcome] == expected[outcome]
            leads = np.array([float(r['lead']) for r in selected])
            gains = np.array([float(r['lead']) - float(base[r['seed']]['lead']) for r in selected])
            assert np.median(leads) == expected['median_lead_all_runs_missed_as_-999']
            assert np.median(leads[leads != -999]) == expected['median_lead_detected_only']
            assert np.median(gains) == expected['median_paired_gain_vs_baseline']
            rng = np.random.default_rng(230048)
            boot = np.median(rng.choice(gains, size=(10000, 80), replace=True), axis=1)
            assert np.array_equal(np.quantile(boot, [.025, .975]), expected['gain_bootstrap_95ci'])
            arm_only = sum(r['outcome'] == 'actionable' and base[r['seed']]['outcome'] != 'actionable' for r in selected)
            base_only = sum(r['outcome'] != 'actionable' and base[r['seed']]['outcome'] == 'actionable' for r in selected)
            n = arm_only + base_only
            p = min(1, 2 * sum(math.comb(n, j) for j in range(min(arm_only, base_only) + 1)) / 2**n)
            assert [arm_only, base_only, p] == expected['mcnemar_arm_only_baseline_only_p']
            both = [float(r['lead']) - float(base[r['seed']]['lead']) for r in selected if r['outcome'] == base[r['seed']]['outcome'] == 'actionable']
            assert len(both) == expected['n_both_detected']
            assert np.median(both) == expected['median_gain_both_detected']
            print(f'PASS {fault}: {arm}')
    print(f'PASS: 9 attachment hashes; 960 per-seed rows; 320 calibration maxima; all 8 summaries. NumPy {np.__version__}.')
    print('Not a simulator rerun: source-generation and monitor-equivalence checks in the supplied logs are not re-executed.')


if __name__ == '__main__':
    main()
