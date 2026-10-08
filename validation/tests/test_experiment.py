import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from experiment import analyze, generate, split_indices, fit_predict, load_csv, parser, run


class ExperimentTests(unittest.TestCase):
    def test_determinism(self):
        a = generate(400, 42, 'compatible')
        np.testing.assert_array_equal(a, generate(400, 42, 'compatible'))
        self.assertEqual(analyze(a, 42, 100), analyze(a, 42, 100))

    def test_disjoint_complete_split(self):
        parts = split_indices(801, 42)
        self.assertEqual(sorted(np.concatenate(parts).tolist()), list(range(801)))
        self.assertEqual([len(p) for p in parts], [480, 160, 161])
        self.assertTrue(np.all(np.diff(split_indices(100, 42, True)[2]) == 1))

    def test_positive_and_negative_controls(self):
        for scenario in ('compatible', 'additive_violation', 'interaction_violation', 'nonlinear_violation'):
            r, _ = analyze(generate(800, 42, scenario), 42, 200)
            self.assertEqual(r['predictive_decision'], 'not_falsified_not_validated' if scenario == 'compatible' else 'falsified_operationally')

    def test_exact_theory_and_independent_baselines(self):
        d = generate(200, 12, 'compatible')
        d[:, 2] = d[:, 0] - d[:, 1]
        for m in ('theory', 'additive', 'interaction', 'nonlinear'):
            np.testing.assert_allclose(fit_predict(d[:150], d[150:], m), d[150:, 2], atol=1e-10)
        changed = d[150:].copy()
        changed[:, 2] += 1000
        np.testing.assert_array_equal(fit_predict(d[:150], changed, 'nonlinear'), fit_predict(d[:150], d[150:], 'nonlinear'))

    def test_invalid_inputs(self):
        for d in (np.empty((0, 3)), np.ones((100, 3)), np.full((100, 3), np.nan)):
            with self.assertRaises(ValueError):
                analyze(d, bootstrap=100)
        with self.assertRaises(ValueError):
            analyze(generate(100, 1, 'compatible'), bootstrap=10)

    def test_csv_and_cli_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / 'bad.csv').write_text('a,b\n1,2\n')
            with self.assertRaises(ValueError):
                load_csv(p / 'bad.csv')
            run(parser().parse_args(['--out', str(p / 'run'), '--n', '100', '--bootstrap', '100']))
            result = json.loads((p / 'run/results.json').read_text())
            self.assertTrue(result['synthetic'])
            self.assertEqual(len(result['results']), 24)
            self.assertTrue((p / 'run/case_00/data.csv').exists())

    def test_external_requires_metadata(self):
        with self.assertRaises(ValueError):
            run(parser().parse_args(['--csv', 'missing.csv']))


if __name__ == '__main__':
    unittest.main()
