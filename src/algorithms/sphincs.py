from pqcrypto.sign import sphincs_sha2_128f_simple


class SPHINCS:

    def generate_keys(self):

        public_key, secret_key = sphincs_sha2_128f_simple.generate_keypair()

        return public_key, secret_key


    def sign(self, message, private_key):

        return sphincs_sha2_128f_simple.sign(
            private_key,
            message
        )


    def verify(self, message, signature, public_key):

        return sphincs_sha2_128f_simple.verify(
            public_key,
            signature,
            message
        )
