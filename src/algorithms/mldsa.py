from .base import CryptoAlgorithm


class MLDSA(CryptoAlgorithm):

    def generate_keys(self):
        public_key = b"mldsa_public_key"
        private_key = b"mldsa_private_key"

        return public_key, private_key

    def sign(self, message, private_key):
        signature = b"mldsa_signature"

        return signature

    def verify(self, message, signature, public_key):
        return True
