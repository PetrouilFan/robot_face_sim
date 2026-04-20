from abc import ABC, abstractmethod
from typing import List
import time

from ..core.types import Event


class AudioBackend(ABC):
    @abstractmethod
    def start_capture(self) -> None:
        pass

    @abstractmethod
    def stop_capture(self) -> None:
        pass

    @abstractmethod
    def start_playback(self, data: bytes) -> None:
        pass

    @abstractmethod
    def stop_playback(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def pending_events(self) -> List[Event]:
        pass

    @property
    @abstractmethod
    def rms_level(self) -> float:
        pass
