import unittest

from src.analysis.recommendation import generate_recommendation


RESULTS = [
    {
        "algorithm": "RSA",
        "keygen_time": 0.020,
        "sign_time": 0.0010,
        "verify_time": 0.00004,
        "public_key_size": 294,
        "private_key_size": 1217,
        "signature_size": 256,
    },
    {
        "algorithm": "ECDSA",
        "keygen_time": 0.00002,
        "sign_time": 0.0004,
        "verify_time": 0.00006,
        "public_key_size": 91,
        "private_key_size": 138,
        "signature_size": 72,
    },
    {
        "algorithm": "MLDSA",
        "keygen_time": 0.00015,
        "sign_time": 0.0005,
        "verify_time": 0.00015,
        "public_key_size": 1952,
        "private_key_size": 4032,
        "signature_size": 3309,
    },
    {
        "algorithm": "SPHINCS",
        "keygen_time": 0.0013,
        "sign_time": 0.0300,
        "verify_time": 0.000006,
        "public_key_size": 32,
        "private_key_size": 64,
        "signature_size": 17088,
    },
]


class RecommendationTests(unittest.TestCase):
    def test_classical_algorithm_requires_migration(self):
        result = generate_recommendation(
            RESULTS,
            "ECDSA",
            ["signing"],
        )

        self.assertTrue(
            result["migration_required"]
        )
        self.assertEqual(
            result["decision"],
            "MIGRATION REQUIRED",
        )

    def test_signing_prefers_mldsa(self):
        result = generate_recommendation(
            RESULTS,
            "ECDSA",
            ["signing"],
        )

        self.assertEqual(
            result["recommended_algorithm"],
            "MLDSA",
        )

    def test_verification_prefers_sphincs(self):
        result = generate_recommendation(
            RESULTS,
            "ECDSA",
            ["verification"],
        )

        self.assertEqual(
            result["recommended_algorithm"],
            "SPHINCS",
        )

    def test_mldsa_can_require_no_change(self):
        result = generate_recommendation(
            RESULTS,
            "MLDSA",
            ["signing"],
        )

        self.assertFalse(
            result["migration_required"]
        )
        self.assertEqual(
            result["decision"],
            "NO CHANGE REQUIRED",
        )

    def test_sphincs_can_be_optional_optimization(self):
        result = generate_recommendation(
            RESULTS,
            "SPHINCS",
            ["signing"],
        )

        self.assertFalse(
            result["migration_required"]
        )
        self.assertEqual(
            result["decision"],
            "OPTIONAL OPTIMIZATION",
        )
        self.assertEqual(
            result["recommended_algorithm"],
            "MLDSA",
        )

    def test_empty_requirements_are_rejected(self):
        result = generate_recommendation(
            RESULTS,
            "ECDSA",
            [],
        )

        self.assertEqual(
            result["decision"],
            "REQUIREMENTS NOT SELECTED",
        )


if __name__ == "__main__":
    unittest.main()
