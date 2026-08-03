from .base import CryptoAlgorithm

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


class ECDSA(CryptoAlgorithm):

    def generate_keys(self):

        private_key = ec.generate_private_key(
            ec.SECP256R1()
        )

        public_key = private_key.public_key()

        return public_key, private_key


    def sign(self, message, private_key):

        signature = private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )

        return signature


    def verify(self, message, signature, public_key):

        try:
            public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )

            return True

        except Exception:
            return False
