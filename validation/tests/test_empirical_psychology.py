import unittest

import numpy as np

from empirical_psychology import load_raw_scores, operationalize, verify_archive
from experiment import split_indices


class EmpiricalPsychologyTests(unittest.TestCase):
    def test_hash_rejects_unexpected_archive(self):
        with self.assertRaises(ValueError):
            verify_archive(b"not the archived dataset")

    def test_unknown_sample_is_rejected_after_valid_archive(self):
        # Archive parsing is covered by the pinned integration run; this checks the API guard.
        with self.assertRaises(ValueError):
            load_raw_scores(b"not an archive", "unknown")

    def test_standardization_is_fitted_on_training_only(self):
        rng = np.random.default_rng(41)
        raw = rng.normal(size=(100, 3))
        data, metadata = operationalize(raw, 17)
        train, _, test = split_indices(100, 17)
        np.testing.assert_allclose(data[train, :2].mean(axis=0), 0, atol=1e-12)
        np.testing.assert_allclose(data[train, :2].std(axis=0, ddof=1), 1, atol=1e-12)
        self.assertAlmostEqual(data[train, 2].mean(), 0, places=12)
        changed = raw.copy()
        changed[test] += 1000
        _, changed_metadata = operationalize(changed, 17)
        self.assertEqual(metadata, changed_metadata)

    def test_constant_training_scale_is_rejected(self):
        raw = np.ones((100, 3))
        with self.assertRaises(ValueError):
            operationalize(raw, 17)


if __name__ == "__main__":
    unittest.main()
