import time
import random
from typing import List
from dataclasses import dataclass, field

from .base import AudioBackend
from ..core.types import Event, EventType
from ..config import AudioConfig

# Threshold for considering audio "loud" (RMS level)
LOUD_NOISE_THRESHOLD = 0.6
# Probability per update call of simulating a loud noise spike
LOUD_NOISE_PROBABILITY = 0.002


@dataclass
class FakeAudioBackend(AudioBackend):
    config: AudioConfig
    _capture_active: bool = False
    _playback_active: bool = False
    _rms_level: float = 0.0
    _events: List[Event] = field(default_factory=list)
    _loud_noise_cooldown: float = 0.0

    def __post_init__(self) -> None:
        self._events = []

    def start_capture(self) -> None:
        self._capture_active = True

    def stop_capture(self) -> None:
        self._capture_active = False

    def start_playback(self, data: bytes) -> None:
        self._playback_active = True
        self._events.append(Event(EventType.PLAYBACK_STARTED, time.time()))

    def stop_playback(self) -> None:
        self._playback_active = False
        self._events.append(Event(EventType.PLAYBACK_FINISHED, time.time()))

    def update(self) -> None:
        now = time.time()
        if self._capture_active:
            # Occasionally simulate a loud noise spike
            if now > self._loud_noise_cooldown and random.random() < LOUD_NOISE_PROBABILITY:
                self._rms_level = random.uniform(0.7, 1.0)
                self._events.append(Event(EventType.LOUD_NOISE_DETECTED, now))
                # Don't fire another loud noise for at least 15 seconds
                self._loud_noise_cooldown = now + 15.0
            else:
                self._rms_level = random.uniform(0.0, 0.3)

    def pending_events(self) -> List[Event]:
        evts = self._events.copy()
        self._events.clear()
        return evts

    @property
    def rms_level(self) -> float:
        return self._rms_level