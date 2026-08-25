from src.analysis.security import get_security_info


DEFAULT_WEIGHTS = {
    "signing": 0.20,
    "verification": 0.15,
    "signature_size": 0.15,
    "key_generation": 0.10,
    "security": 0.40
}


def normalize_weights(weights):
    """
    Normalize weights so their total equals 1.0.
    """

    total = sum(weights.values())

    if total <= 0:
        raise ValueError(
            "At least one weight must be greater than zero."
        )

    return {
        key: value / total
        for key, value in weights.items()
    }


def normalize_score(value, values):
    """
    Convert a metric value into a 0-100 score.
    Lower values receive higher scores.
    """

    best = min(values)

    if value == 0:
        return 100.0

    return (best / value) * 100


def score_candidates(
    results,
    weights=None
):
    """
    Score all quantum-resistant candidates.

    weights:
        Optional dictionary controlling the importance
        of each performance metric.
    """

    if not results:
        return []

    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    weights = normalize_weights(weights)

    pqc_results = []

    for result in results:

        security = get_security_info(
            result["algorithm"]
        )

        if security["quantum_resistant"]:
            pqc_results.append(result)

    if not pqc_results:
        return []

    signing_values = [
        result["sign_time"]
        for result in pqc_results
    ]

    verification_values = [
        result["verify_time"]
        for result in pqc_results
    ]

    signature_size_values = [
        result["signature_size"]
        for result in pqc_results
    ]

    keygen_values = [
        result["keygen_time"]
        for result in pqc_results
    ]

    scored_candidates = []

    for result in pqc_results:

        signing_score = normalize_score(
            result["sign_time"],
            signing_values
        )

        verification_score = normalize_score(
            result["verify_time"],
            verification_values
        )

        signature_size_score = normalize_score(
            result["signature_size"],
            signature_size_values
        )

        keygen_score = normalize_score(
            result["keygen_time"],
            keygen_values
        )

        # All candidates reaching this point are already
        # classified as quantum-resistant.
        security_score = 100.0

        total_score = (
            signing_score * weights["signing"]
            + verification_score * weights["verification"]
            + signature_size_score * weights["signature_size"]
            + keygen_score * weights["key_generation"]
            + security_score * weights["security"]
        )

        scored_candidates.append(
            {
                "algorithm": result["algorithm"],
                "score": total_score,
                "scores": {
                    "security": security_score,
                    "signing": signing_score,
                    "verification": verification_score,
                    "signature_size": signature_size_score,
                    "key_generation": keygen_score
                }
            }
        )

    scored_candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_candidates


def generate_recommendation(
    results,
    current_algorithm,
    weights=None
):
    """
    Generate a PQC migration recommendation.

    If weights are not provided, the default weighting
    model is used.
    """

    current_security = get_security_info(
        current_algorithm
    )

    if current_security["quantum_resistant"]:

        return {
            "current_algorithm": current_algorithm,
            "migration_required": False,
            "recommended_algorithm": current_algorithm,
            "reason": (
                "The current algorithm is already "
                "classified as quantum-resistant."
            ),
            "candidates": []
        }

    candidates = score_candidates(
        results,
        weights
    )

    if not candidates:

        return {
            "current_algorithm": current_algorithm,
            "migration_required": True,
            "recommended_algorithm": None,
            "reason": (
                "No quantum-resistant candidates "
                "were found."
            ),
            "candidates": []
        }

    recommended = candidates[0]

    return {
        "current_algorithm": current_algorithm,
        "migration_required": True,
        "recommended_algorithm": recommended["algorithm"],
        "reason": (
            "The recommended algorithm provides the "
            "highest weighted score among the evaluated "
            "quantum-resistant candidates."
        ),
        "score": recommended["score"],
        "scores": recommended["scores"],
        "weights": normalize_weights(
            weights
            if weights is not None
            else DEFAULT_WEIGHTS
        ),
        "candidates": candidates
    }


if __name__ == "__main__":

    import json

    with open(
        "results/benchmark_results.json",
        "r"
    ) as file:

        results = json.load(file)

    recommendation = generate_recommendation(
        results,
        "ECDSA"
    )

    print(
        json.dumps(
            recommendation,
            indent=4
        )
    )
