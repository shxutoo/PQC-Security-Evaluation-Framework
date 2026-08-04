import json

from src.analysis.security import get_security_info


def load_results(path="results/benchmark_results.json"):

    with open(path, "r") as file:
        return json.load(file)


def find_fastest(results, metric):

    fastest = min(
        results,
        key=lambda x: x[metric]
    )

    return {
        "algorithm": fastest["algorithm"],
        "value": fastest[metric]
    }


def find_smallest(results, metric):

    smallest = min(
        results,
        key=lambda x: x[metric]
    )

    return {
        "algorithm": smallest["algorithm"],
        "value": smallest[metric]
    }


def find_largest(results, metric):

    largest = max(
        results,
        key=lambda x: x[metric]
    )

    return {
        "algorithm": largest["algorithm"],
        "value": largest[metric]
    }


def filter_pqc_algorithms(results):

    pqc_results = []

    for result in results:

        security = get_security_info(
            result["algorithm"]
        )

        if security["quantum_resistant"]:
            pqc_results.append(result)

    return pqc_results


def calculate_overhead(value, baseline):

    return value / baseline


def generate_summary(results):

    pqc_results = filter_pqc_algorithms(results)

    mldsa = next(
        result for result in pqc_results
        if result["algorithm"] == "MLDSA"
    )

    sphincs = next(
        result for result in pqc_results
        if result["algorithm"] == "SPHINCS"
    )


    summary = {

        "performance": {

            "fastest_key_generation": find_fastest(
                results,
                "keygen_time"
            ),

            "fastest_signing": find_fastest(
                results,
                "sign_time"
            ),

            "fastest_verification": find_fastest(
                results,
                "verify_time"
            )
        },


        "sizes": {

            "smallest_signature": find_smallest(
                results,
                "signature_size"
            ),

            "largest_signature": find_largest(
                results,
                "signature_size"
            )
        },


        "security": {

            "quantum_resistant_algorithms": [
                result["algorithm"]
                for result in pqc_results
            ]

        },


        "post_quantum_analysis": {

            "fastest_pqc_key_generation": find_fastest(
                pqc_results,
                "keygen_time"
            ),

            "fastest_pqc_signing": find_fastest(
                pqc_results,
                "sign_time"
            ),

            "fastest_pqc_verification": find_fastest(
                pqc_results,
                "verify_time"
            ),

            "sphincs_signature_overhead_vs_mldsa":
                calculate_overhead(
                    sphincs["signature_size"],
                    mldsa["signature_size"]
                )

        }

    }


    return summary


if __name__ == "__main__":

    results = load_results()

    summary = generate_summary(results)

    print(json.dumps(
        summary,
        indent=4
    ))
