from abc import ABC, abstractmethod


class CryptoAlgorithm(ABC):

    @abstractmethod
    def generate_keys(self):
        pass

    @abstractmethod
    def sign(self, message):
        pass

    @abstractmethod
    def verify(self, message, signature):
        pass
