from .base import CryptoAlgorithm


class RSA(CryptoAlgorithm):

    def generate_keys(self):
        public_key = b"rsa_public_key"
        private_key = b"rsa_private_key"

        return public_key, private_key

    def sign(self, message, private_key):
        signature = b"rsa_signature"

        return signature

    def verify(self, message, signature, public_key):
        return True
