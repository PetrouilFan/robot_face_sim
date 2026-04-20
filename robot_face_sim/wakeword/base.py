from abc import ABC, abstractmethod
from typing import List

from ..core.types import Event


class WakeWordDetector(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def pending_events(self) -> List[Event]:
        pass

    @abstractmethod
    def trigger(self) -> None:
        pass
