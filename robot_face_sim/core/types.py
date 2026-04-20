from dataclasses import dataclass, field
from enum import Enum, auto
from typing import NamedTuple, Optional, Tuple

# Core types, portable to C++ structs directly


class State(Enum):
    BOOTING = auto()
    IDLE = auto()
    SLEEPING = auto()
    WAKING = auto()
    LISTENING = auto()
    THINKING = auto()
    SPEAKING = auto()
    HAPPY = auto()
    SAD = auto()
    CONFUSED = auto()
    ANGRY = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()


class EventType(Enum):
    WAKE_WORD_DETECTED = auto()
    USER_ACTIVITY = auto()
    IDLE_TIMEOUT = auto()
    SPEECH_STARTED = auto()
    SPEECH_STOPPED = auto()
    PLAYBACK_STARTED = auto()
    PLAYBACK_FINISHED = auto()
    ERROR_DETECTED = auto()
    SLEEP_REQUESTED = auto()
    WAKE_REQUESTED = auto()
    ANIMATION_FINISHED = auto()
    LOUD_NOISE_DETECTED = auto()


@dataclass
class Event:
    type: EventType
    timestamp: float
    data: Optional[dict] = None


@dataclass
class EyeParameters:
    # Silhouette shape parameters - all values 0.0-1.0 unless noted
    center_x: float = 0.0
    center_y: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation_deg: float = 0.0
    inner_corner_raise: float = 0.0
    outer_corner_raise: float = 0.0
    top_cut: float = 0.0
    bottom_cut: float = 0.0
    inner_tension: float = 0.5
    outer_tension: float = 0.5
    roundness: float = 0.6
    squash: float = 1.0
    stretch: float = 1.0
    brightness: float = 1.0
    visible: bool = True


@dataclass
class FaceRigTransform:
    face_offset_x: float = 0.0
    face_offset_y: float = 0.0
    face_scale: float = 1.0
    face_tilt: float = 0.0
    eye_gap: float = 1.0


@dataclass
class FaceState:
    left: EyeParameters
    right: EyeParameters
    overall_brightness: float = 1.0
    rig: FaceRigTransform = field(default_factory=FaceRigTransform)


class Rect(NamedTuple):
    x: int
    y: int
    w: int
    h: int

    @property
    def area(self) -> int:
        return self.w * self.h

    def merge(self, other: "Rect") -> "Rect":
        x1 = min(self.x, other.x)
        y1 = min(self.y, other.y)
        x2 = max(self.x + self.w, other.x + other.w)
        y2 = max(self.y + self.h, other.y + other.h)
        return Rect(x1, y1, x2 - x1, y2 - y1)


@dataclass
class KeyFrame:
    time: float
    value: float
    easing: str = "linear"


@dataclass
class Clip:
    id: str
    duration: float
    priority: int = 0
    interruptible: bool = True
    loop: bool = False
    tracks: dict[str, list[KeyFrame]] | None = None


class DisplayMetrics(NamedTuple):
    dirty_area: int
    dirty_percent: float
    bytes_transferred: int
    estimated_transfer_us: int
    frame_budget_ok: bool
