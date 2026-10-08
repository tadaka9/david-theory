import unittest

from empirical_economy import join_indicators, values_by_country


def payload(indicator, values):
    return [
        {"page": 1},
        [
            {
                "indicator": {"id": indicator},
                "country": {"value": name},
                "countryiso3code": code,
                "value": value,
            }
            for code, name, value in values
        ],
    ]


class EmpiricalEconomyTests(unittest.TestCase):
    def test_join_uses_only_complete_series_and_computes_discrepancy(self):
        data = {
            "E": payload("E", [("AAA", "A", 100), ("BBB", "B", 50)]),
            "h": payload("h", [("AAA", "A", 70)]),
            "H": payload("H", [("AAA", "A", 35), ("BBB", "B", 20)]),
        }
        rows = join_indicators(data)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["predicted_E_minus_h"], 30)
        self.assertEqual(rows[0]["discrepancy_H_minus_prediction"], 5)
        self.assertEqual(rows[0]["relative_discrepancy_to_abs_E"], 0.05)

    def test_unexpected_payload_is_rejected(self):
        with self.assertRaises(ValueError):
            values_by_country({"not": "world-bank-format"})


if __name__ == "__main__":
    unittest.main()
