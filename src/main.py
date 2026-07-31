from algorithms.rsa import RSA
from algorithms.ecdsa import ECDSA
from algorithms.mldsa import MLDSA


algorithms = [
    RSA(),
    ECDSA(),
    MLDSA()
]


for algorithm in algorithms:
    print(type(algorithm).__name__)
