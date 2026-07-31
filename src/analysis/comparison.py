import json


def load_results(path="results/benchmark_results.json"):

    with open(path, "r") as file:
        return json.load(file)


def compare_algorithms(results):

    comparison = {}

    for result in results:

        algorithm = result["algorithm"]

        comparison[algorithm] = {
            "keygen_time": result["keygen_time"],
            "sign_time": result["sign_time"],
            "verify_time": result["verify_time"],
            "public_key_size": result["public_key_size"],
            "private_key_size": result["private_key_size"],
            "signature_size": result["signature_size"]
        }

    return comparison


if __name__ == "__main__":

    results = load_results()

    comparison = compare_algorithms(results)

    for algorithm, metrics in comparison.items():
        print(algorithm)
        print(metrics)
