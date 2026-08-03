from .base import CryptoAlgorithm

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


class RSA(CryptoAlgorithm):

    def generate_keys(self):

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        return public_key, private_key


    def sign(self, message, private_key):

        signature = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return signature


    def verify(self, message, signature, public_key):

        try:
            public_key.verify(
                signature,
                message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            return True

        except Exception:
            return False
