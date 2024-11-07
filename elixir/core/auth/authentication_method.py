from abc import ABC, abstractmethod


class AuthenticationMethod(ABC):
    @staticmethod
    @abstractmethod
    def handle_key(received_key: str) -> tuple:
        pass
