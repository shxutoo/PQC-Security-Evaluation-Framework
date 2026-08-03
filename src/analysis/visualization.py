import matplotlib.pyplot as plt

from src.analysis.comparison import load_results


def plot_metric(results, metric, title, filename):

    algorithms = []
    values = []

    for result in results:
        algorithms.append(result["algorithm"])
        values.append(result[metric])

    plt.figure(figsize=(8, 5))

    plt.bar(algorithms, values)

    plt.title(title)
    plt.ylabel(metric)

    plt.tight_layout()

    plt.savefig(
        f"results/{filename}.png"
    )

    plt.close()


def generate_visualizations():

    results = load_results()

    plot_metric(
        results,
        "keygen_time",
        "Key Generation Time Comparison",
        "keygen_comparison"
    )

    plot_metric(
        results,
        "sign_time",
        "Signing Time Comparison",
        "sign_comparison"
    )

    plot_metric(
        results,
        "verify_time",
        "Verification Time Comparison",
        "verify_comparison"
    )

    plot_metric(
        results,
        "signature_size",
        "Signature Size Comparison",
        "signature_size_comparison"
    )


if __name__ == "__main__":

    generate_visualizations()
