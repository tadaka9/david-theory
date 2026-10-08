import unittest

from constant_validation import constant_intersection


class ConstantValidationTests(unittest.TestCase):
    def test_disjoint_intervals_reject_shared_constant(self):
        result = constant_intersection(
            [
                {"E": 3, "H": 2, "error_E": 0.1, "error_H": 0.1},
                {"E": 3, "H": 1, "error_E": 0.1, "error_H": 0.1},
            ]
        )
        self.assertFalse(result["compatible_with_one_constant"])
        self.assertIsNone(result["intersection"])
        self.assertAlmostEqual(result["maximum_lower_bound"], 1.8)
        self.assertAlmostEqual(result["minimum_upper_bound"], 1.2)

    def test_overlap_is_compatibility_not_validation(self):
        result = constant_intersection(
            [
                {"E": 3, "H": 2, "error_E": 0.5, "error_H": 0.5},
                {"E": 3, "H": 1, "error_E": 0.5, "error_H": 0.5},
            ]
        )
        self.assertTrue(result["compatible_with_one_constant"])
        self.assertEqual(result["intersection"], [1.0, 2.0])
        self.assertIn("not proof", result["interpretation"])

    def test_invalid_uncertainty_is_rejected(self):
        with self.assertRaises(ValueError):
            constant_intersection(
                [{"E": 3, "H": 2, "error_E": -0.1, "error_H": 0.1}]
            )


if __name__ == "__main__":
    unittest.main()
