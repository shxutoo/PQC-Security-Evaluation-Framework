from .base import CryptoAlgorithm


class ECDSA(CryptoAlgorithm):

    def generate_keys(self):
        public_key = b"ecdsa_public_key"
        private_key = b"ecdsa_private_key"

        return public_key, private_key

    def sign(self, message, private_key):
        signature = b"ecdsa_signature"

        return signature

    def verify(self, message, signature, public_key):
        return True
