import json

from src.analysis.summary import (
    load_results,
    generate_summary
)


def export_json(summary, path="results/comparative_summary.json"):

    with open(path, "w") as file:

        json.dump(
            summary,
            file,
            indent=4
        )


def format_summary(summary):

    lines = []

    lines.append("=" * 40)
    lines.append("Comparative Summary")
    lines.append("=" * 40)


    lines.append("\nPerformance:")

    performance = summary["performance"]

    lines.append(
        f"Fastest key generation: "
        f"{performance['fastest_key_generation']['algorithm']} "
        f"({performance['fastest_key_generation']['value']:.6f}s)"
    )

    lines.append(
        f"Fastest signing: "
        f"{performance['fastest_signing']['algorithm']} "
        f"({performance['fastest_signing']['value']:.6f}s)"
    )

    lines.append(
        f"Fastest verification: "
        f"{performance['fastest_verification']['algorithm']} "
        f"({performance['fastest_verification']['value']:.6f}s)"
    )


    lines.append("\nSizes:")

    sizes = summary["sizes"]

    lines.append(
        f"Smallest signature: "
        f"{sizes['smallest_signature']['algorithm']} "
        f"({sizes['smallest_signature']['value']} bytes)"
    )

    lines.append(
        f"Largest signature: "
        f"{sizes['largest_signature']['algorithm']} "
        f"({sizes['largest_signature']['value']} bytes)"
    )


    lines.append("\nSecurity:")

    lines.append(
        "Quantum-resistant algorithms: "
        + ", ".join(
            summary["security"]["quantum_resistant_algorithms"]
        )
    )


    lines.append("\nPost-Quantum Analysis:")

    pqc = summary["post_quantum_analysis"]

    lines.append(
        f"Fastest PQC key generation: "
        f"{pqc['fastest_pqc_key_generation']['algorithm']} "
        f"({pqc['fastest_pqc_key_generation']['value']:.6f}s)"
    )

    lines.append(
        f"Fastest PQC signing: "
        f"{pqc['fastest_pqc_signing']['algorithm']} "
        f"({pqc['fastest_pqc_signing']['value']:.6f}s)"
    )

    lines.append(
        f"Fastest PQC verification: "
        f"{pqc['fastest_pqc_verification']['algorithm']} "
        f"({pqc['fastest_pqc_verification']['value']:.6f}s)"
    )

    lines.append(
        f"SPHINCS signature overhead compared with MLDSA: "
        f"{pqc['sphincs_signature_overhead_vs_mldsa']:.2f}x larger"
    )


    return "\n".join(lines)


def export_text(summary, path="results/comparative_summary.txt"):

    report = format_summary(summary)

    with open(path, "w") as file:

        file.write(report)


def generate_exports():

    results = load_results()

    summary = generate_summary(results)

    export_json(summary)

    export_text(summary)


if __name__ == "__main__":

    generate_exports()

    print(
        "Comparative analysis exported successfully."
    )
