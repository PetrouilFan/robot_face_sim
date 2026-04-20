from dataclasses import dataclass
from typing import Literal

from .constants import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    DEFAULT_TARGET_FPS,
    DEFAULT_SPI_CLOCK_HZ,
)


@dataclass
class DisplayConfig:
    width: int = DISPLAY_WIDTH
    height: int = DISPLAY_HEIGHT
    scale: int = 3
    target_fps: int = DEFAULT_TARGET_FPS
    spi_clock_hz: int = DEFAULT_SPI_CLOCK_HZ
    constrained_mode: bool = False
    rgb565_preview: bool = False
    show_dirty_rects: bool = False
    force_full_frame: bool = False


@dataclass
class AudioConfig:
    backend: Literal["fake", "sounddevice"] = "fake"
    sample_rate: int = 16000
    buffer_size: int = 512
    channels: int = 1


@dataclass
class WakeWordConfig:
    backend: Literal["fake"] = "fake"
    trigger_key: str = "w"
    auto_trigger: bool = False
    auto_trigger_interval: float = 10.0


@dataclass
class DebugConfig:
    enabled: bool = True
    show_fps: bool = True
    show_state: bool = True
    show_metrics: bool = True
    show_audio_level: bool = True
    log_events: bool = True
    show_help: bool = True


@dataclass
class Config:
    display: DisplayConfig
    audio: AudioConfig
    wakeword: WakeWordConfig
    debug: DebugConfig

    @classmethod
    def default(cls) -> "Config":
        return cls(
            display=DisplayConfig(),
            audio=AudioConfig(),
            wakeword=WakeWordConfig(),
            debug=DebugConfig(),
        )
