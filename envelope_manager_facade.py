from abc import ABC, abstractmethod

class EnvelopeManagerFacade(ABC):
    @abstractmethod
    def current_envelope_name(self) -> str:
        pass

    @abstractmethod
    def get_id_for_name(self, name: str) -> int:
        pass
