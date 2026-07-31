from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    algorithm: str
    keygen_time: float
    sign_time: float
    verify_time: float
    public_key_size: int
    private_key_size: int
    signature_size: int
