from .base import CryptoAlgorithm

from pqcrypto.sign import ml_dsa_65


class MLDSA(CryptoAlgorithm):

    def generate_keys(self):

        public_key, secret_key = ml_dsa_65.generate_keypair()

        return public_key, secret_key


    def sign(self, message, private_key):

        signature = ml_dsa_65.sign(
            private_key,
            message
        )

        return signature


    def verify(self, message, signature, public_key):

        try:
            ml_dsa_65.verify(
                public_key,
                message,
                signature
            )

            return True

        except Exception:
            return False
