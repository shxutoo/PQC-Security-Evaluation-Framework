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

    pqc_results = filter_pqc_algorithms(results)

    print(
        "Quantum-resistant algorithms: "
        + ", ".join(
            result["algorithm"]
            for result in pqc_results
        )
    )


    print("\nPost-Quantum Analysis:")


    algorithm, value = find_fastest(
        pqc_results,
        "keygen_time"
    )

    print(
        f"Fastest PQC key generation: "
        f"{algorithm} ({value:.6f}s)"
    )


    algorithm, value = find_fastest(
        pqc_results,
        "sign_time"
    )

    print(
        f"Fastest PQC signing: "
        f"{algorithm} ({value:.6f}s)"
    )


    algorithm, value = find_fastest(
        pqc_results,
        "verify_time"
    )

    print(
        f"Fastest PQC verification: "
        f"{algorithm} ({value:.6f}s)"
    )


    mldsa = next(
        result for result in pqc_results
        if result["algorithm"] == "MLDSA"
    )

    sphincs = next(
        result for result in pqc_results
        if result["algorithm"] == "SPHINCS"
    )


    overhead = calculate_overhead(
        sphincs["signature_size"],
        mldsa["signature_size"]
    )


    print(
        "\nSPHINCS signature overhead compared "
        f"with MLDSA: {overhead:.2f}x larger"
    )


if __name__ == "__main__":

    results = load_results()

    generate_summary(results)
