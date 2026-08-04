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

    return (
        fastest["algorithm"],
        fastest[metric]
    )


def find_smallest(results, metric):

    smallest = min(
        results,
        key=lambda x: x[metric]
    )

    return (
        smallest["algorithm"],
        smallest[metric]
    )


def find_largest(results, metric):

    largest = max(
        results,
        key=lambda x: x[metric]
    )

    return (
        largest["algorithm"],
        largest[metric]
    )


def generate_summary(results):

    print("=" * 40)
    print("Comparative Summary")
    print("=" * 40)

    print("\nPerformance:")

    algorithm, value = find_fastest(
        results,
        "keygen_time"
    )

    print(
        f"Fastest key generation: "
        f"{algorithm} ({value:.6f}s)"
    )


    algorithm, value = find_fastest(
        results,
        "sign_time"
    )

    print(
        f"Fastest signing: "
        f"{algorithm} ({value:.6f}s)"
    )


    algorithm, value = find_fastest(
        results,
        "verify_time"
    )

    print(
        f"Fastest verification: "
        f"{algorithm} ({value:.6f}s)"
    )


    print("\nSizes:")

    algorithm, value = find_smallest(
        results,
        "signature_size"
    )

    print(
        f"Smallest signature: "
        f"{algorithm} ({value} bytes)"
    )


    algorithm, value = find_largest(
        results,
        "signature_size"
    )

    print(
        f"Largest signature: "
        f"{algorithm} ({value} bytes)"
    )


    print("\nSecurity:")

    pqc_algorithms = []

    for result in results:

        security = get_security_info(
            result["algorithm"]
        )

        if security["quantum_resistant"]:
            pqc_algorithms.append(
                result["algorithm"]
            )


    print(
        "Quantum-resistant algorithms: "
        + ", ".join(pqc_algorithms)
    )


if __name__ == "__main__":

    results = load_results()

    generate_summary(results)

