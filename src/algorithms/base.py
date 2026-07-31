from abc import ABC, abstractmethod


class CryptoAlgorithm(ABC):

    @abstractmethod
    def generate_keys(self):
        pass

    @abstractmethod
    def sign(self, message, private_key):
        pass

    @abstractmethod
    def verify(self, message, signature, public_key):
        pass
