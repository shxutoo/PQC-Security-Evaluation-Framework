import json
from dataclasses import asdict

from src.algorithms.rsa import RSA
from src.algorithms.ecdsa import ECDSA
from src.algorithms.mldsa import MLDSA
from src.algorithms.sphincs import SPHINCS

from src.benchmarks.runner import benchmark_algorithm


algorithms = [
    RSA(),
    ECDSA(),
    MLDSA(),
    SPHINCS()
]


results = []

for algorithm in algorithms:
    result = benchmark_algorithm(algorithm)
    results.append(result)


for result in results:
    print(result)


with open("results/benchmark_results.json", "w") as file:
    json.dump(
        [asdict(result) for result in results],
        file,
        indent=4
    )
