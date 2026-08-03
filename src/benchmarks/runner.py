import time
import statistics

from src.benchmarks.metrics import BenchmarkResult

from cryptography.hazmat.primitives import serialization


def get_size(obj):

    if isinstance(obj, bytes):
        return len(obj)

    if hasattr(obj, "private_bytes"):

        return len(
            obj.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    if hasattr(obj, "public_bytes"):

        return len(
            obj.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    return 0


def benchmark_algorithm(algorithm, runs=10):

    message = b"Benchmark message"

    keygen_times = []
    sign_times = []
    verify_times = []

    public_key = None
    private_key = None
    signature = None

    for _ in range(runs):

        start = time.perf_counter()

        public_key, private_key = algorithm.generate_keys()

        end = time.perf_counter()

        keygen_times.append(end - start)


        start = time.perf_counter()

        signature = algorithm.sign(message, private_key)

        end = time.perf_counter()

        sign_times.append(end - start)


        start = time.perf_counter()

        algorithm.verify(message, signature, public_key)

        end = time.perf_counter()

        verify_times.append(end - start)


    result = BenchmarkResult(
        algorithm=algorithm.__class__.__name__,
        keygen_time=sum(keygen_times) / runs,
        sign_time=sum(sign_times) / runs,
        verify_time=sum(verify_times) / runs,
        keygen_std=statistics.stdev(keygen_times),
        sign_std=statistics.stdev(sign_times),
        verify_std=statistics.stdev(verify_times),
        public_key_size=get_size(public_key),
        private_key_size=get_size(private_key),
        signature_size=len(signature),
        runs=runs
    )

    return result
