import time

from src.benchmarks.metrics import BenchmarkResult


def benchmark_algorithm(algorithm):

    message = b"Benchmark message"

    # Key generation benchmark
    start = time.perf_counter()

    public_key, private_key = algorithm.generate_keys()

    end = time.perf_counter()

    keygen_time = end - start


    # Signing benchmark
    start = time.perf_counter()

    signature = algorithm.sign(message, private_key)

    end = time.perf_counter()

    sign_time = end - start


    # Verification benchmark
    start = time.perf_counter()

    algorithm.verify(message, signature, public_key)

    end = time.perf_counter()

    verify_time = end - start


    result = BenchmarkResult(
        algorithm=algorithm.__class__.__name__,
        keygen_time=keygen_time,
        sign_time=sign_time,
        verify_time=verify_time,
        public_key_size=len(public_key),
        private_key_size=len(private_key),
        signature_size=len(signature)
    )

    return result
