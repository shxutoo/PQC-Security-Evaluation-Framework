import json


def load_results(path="results/benchmark_results.json"):

    with open(path, "r") as file:
        return json.load(file)


def generate_report(results):

    for result in results:

        print("=" * 40)

        print(f"Algorithm: {result['algorithm']}")
        print(f"Benchmark runs: {result['runs']}")

        print("\nPerformance:")

        print(
            f"Key generation: "
            f"{result['keygen_time']:.6f}s "
            f"(std: {result['keygen_std']:.6f})"
        )

        print(
            f"Signing: "
            f"{result['sign_time']:.6f}s "
            f"(std: {result['sign_std']:.6f})"
        )

        print(
            f"Verification: "
            f"{result['verify_time']:.6f}s "
            f"(std: {result['verify_std']:.6f})"
        )

        print("\nSizes:")

        print(f"Public key: {result['public_key_size']} bytes")
        print(f"Private key: {result['private_key_size']} bytes")
        print(f"Signature: {result['signature_size']} bytes")


if __name__ == "__main__":

    results = load_results()

    generate_report(results)
