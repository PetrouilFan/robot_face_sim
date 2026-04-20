import time
from typing import List
from dataclasses import dataclass, field

from .base import WakeWordDetector
from ..core.types import Event, EventType
from ..config import WakeWordConfig


@dataclass
class FakeWakeWordDetector(WakeWordDetector):
    config: WakeWordConfig
    _active: bool = False
    _events: List[Event] = field(default_factory=list)
    _last_auto_trigger: float = 0.0

    def start(self) -> None:
        self._active = True

    def stop(self) -> None:
        self._active = False

    def update(self) -> None:
        if not self._active:
            return

        if self.config.auto_trigger:
            now = time.time()
            if now - self._last_auto_trigger > self.config.auto_trigger_interval:
                self.trigger()
                self._last_auto_trigger = now

    def pending_events(self) -> List[Event]:
        evts = self._events.copy()
        self._events.clear()
        return evts

    def trigger(self) -> None:
        self._events.append(Event(EventType.WAKE_WORD_DETECTED, time.time()))
