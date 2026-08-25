from src.analysis.security import get_security_info


REQUIREMENT_KEYS = (
    "security",
    "signing",
    "verification",
    "signature_size",
    "key_generation",
)


def normalize_score(value, values):
    """
    Convert a lower-is-better measurement to a 0-100 relative score.
    The best measured candidate receives 100.
    """
    if not values:
        return 0.0

    best = min(values)

    if value == 0:
        return 100.0

    return (best / value) * 100.0


def build_weights(selected_requirements):
    """
    Checkboxes are binary inclusion controls.

    Every selected requirement receives equal weight, so the behavior is easy
    to explain and reproduce in the thesis. Unselected requirements receive 0.

    Example:
        ["signing", "verification"] ->
        {"signing": 0.5, "verification": 0.5}
    """
    selected = [
        key
        for key in selected_requirements or []
        if key in REQUIREMENT_KEYS
    ]

    # Preserve order while removing duplicates.
    selected = list(dict.fromkeys(selected))

    if not selected:
        return {}

    weight = 1.0 / len(selected)

    return {
        key: weight
        for key in selected
    }


def score_candidates(results, selected_requirements):
    """
    Rank only quantum-resistant candidates.

    Security is intentionally an eligibility condition as well as a displayed
    score. ML-DSA and SPHINCS are both treated as quantum-resistant candidates,
    so the security component does not distinguish them from each other.
    """
    weights = build_weights(selected_requirements)

    if not weights:
        return []

    pqc_results = []

    for result in results or []:
        info = get_security_info(result["algorithm"])

        if info["quantum_resistant"]:
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

    candidates = []

    for result in pqc_results:
        component_scores = {
            "security": 100.0,
            "signing": normalize_score(
                result["sign_time"],
                signing_values,
            ),
            "verification": normalize_score(
                result["verify_time"],
                verification_values,
            ),
            "signature_size": normalize_score(
                result["signature_size"],
                signature_size_values,
            ),
            "key_generation": normalize_score(
                result["keygen_time"],
                keygen_values,
            ),
        }

        total_score = sum(
            component_scores[key] * weight
            for key, weight in weights.items()
        )

        candidates.append(
            {
                "algorithm": result["algorithm"],
                "score": total_score,
                "scores": component_scores,
            }
        )

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return candidates


def generate_recommendation(
    results,
    current_algorithm,
    selected_requirements=None,
):
    """
    Keep two questions separate:

    1. Is migration required for quantum security?
    2. Which PQC candidate best matches the selected benchmark requirements?
    """
    weights = build_weights(selected_requirements)

    if not weights:
        return {
            "current_algorithm": current_algorithm,
            "migration_required": False,
            "decision": "REQUIREMENTS NOT SELECTED",
            "recommended_algorithm": None,
            "reason": (
                "Select at least one evaluation requirement before "
                "running the migration analysis."
            ),
            "score": 0.0,
            "scores": {},
            "weights": {},
            "candidates": [],
        }

    candidates = score_candidates(
        results,
        selected_requirements,
    )

    if not candidates:
        return {
            "current_algorithm": current_algorithm,
            "migration_required": False,
            "decision": "NO PQC DATA",
            "recommended_algorithm": None,
            "reason": (
                "No quantum-resistant benchmark candidates were found. "
                "Run the benchmark and try again."
            ),
            "score": 0.0,
            "scores": {},
            "weights": weights,
            "candidates": [],
        }

    current_security = get_security_info(
        current_algorithm
    )

    recommended = candidates[0]

    if not current_security["quantum_resistant"]:
        migration_required = True
        decision = "MIGRATION REQUIRED"
        reason = (
            f"{current_algorithm} is not classified as quantum-resistant. "
            f"{recommended['algorithm']} is the highest-scoring "
            "quantum-resistant candidate for the selected requirements."
        )

    elif current_algorithm == recommended["algorithm"]:
        migration_required = False
        decision = "NO CHANGE REQUIRED"
        reason = (
            f"{current_algorithm} is already quantum-resistant and is the "
            "highest-scoring candidate for the selected requirements."
        )

    else:
        migration_required = False
        decision = "OPTIONAL OPTIMIZATION"
        reason = (
            f"{current_algorithm} is already quantum-resistant, so a "
            "quantum-security migration is not required. "
            f"{recommended['algorithm']} scores higher for the selected "
            "benchmark requirements."
        )

    return {
        "current_algorithm": current_algorithm,
        "migration_required": migration_required,
        "decision": decision,
        "recommended_algorithm": recommended["algorithm"],
        "reason": reason,
        "score": recommended["score"],
        "scores": recommended["scores"],
        "weights": weights,
        "candidates": candidates,
    }
