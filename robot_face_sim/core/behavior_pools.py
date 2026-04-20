from dataclasses import dataclass, field
from typing import Callable, Dict, List, Set

from .types import Clip, KeyFrame, State


@dataclass
class BehaviorDef:
    """Defines a behavior: a clip factory plus scheduling metadata."""
    name: str
    clip_factory: Callable[[], Clip]
    tier: str  # "common", "occasional", "rare"
    weight: float = 1.0
    cooldown: float = 0.0
    allowed_states: Set[State] = field(default_factory=lambda: {State.IDLE})


# ---------------------------------------------------------------------------
# Common micro-idle clips (1.5-8s intervals)
# ---------------------------------------------------------------------------

def clip_soft_squish() -> Clip:
    """Tiny vertical compression pulse, like a breathing accent."""
    return Clip(
        id="soft_squish",
        duration=0.6,
        priority=3,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.15, 0.82, "ease_in_out_sine"),
                KeyFrame(0.45, 0.85, "ease_in_out_sine"),
                KeyFrame(0.60, 0.85),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.17, 0.81, "ease_in_out_sine"),
                KeyFrame(0.47, 0.85, "ease_in_out_sine"),
                KeyFrame(0.60, 0.85),
            ],
        },
    )


def clip_micro_tilt_swap() -> Clip:
    """One eye rotates +2deg, the other -1deg, then swap back."""
    return Clip(
        id="micro_tilt_swap",
        duration=0.8,
        priority=3,
        interruptible=True,
        loop=False,
        tracks={
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 2.0, "ease_out_sine"),
                KeyFrame(0.40, 2.0),
                KeyFrame(0.60, -1.0, "ease_in_out_sine"),
                KeyFrame(0.80, 0.0, "ease_in_sine"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.22, -1.0, "ease_out_sine"),
                KeyFrame(0.42, -1.0),
                KeyFrame(0.62, 2.0, "ease_in_out_sine"),
                KeyFrame(0.80, 0.0, "ease_in_sine"),
            ],
        },
    )


def clip_tiny_focus_narrow() -> Clip:
    """Both eyes narrow briefly, like a moment of focus."""
    return Clip(
        id="tiny_focus_narrow",
        duration=0.35,
        priority=3,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.08, 0.22, "ease_out_sine"),
                KeyFrame(0.25, 0.22),
                KeyFrame(0.35, 0.10, "ease_in_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.10, 0.20, "ease_out_sine"),
                KeyFrame(0.27, 0.20),
                KeyFrame(0.35, 0.10, "ease_in_sine"),
            ],
        },
    )


def clip_lazy_half_blink() -> Clip:
    """Asymmetric partial blink: left side closes more than right."""
    return Clip(
        id="lazy_half_blink",
        duration=0.5,
        priority=10,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.12, 0.70, "ease_in_sine"),
                KeyFrame(0.30, 0.70),
                KeyFrame(0.50, 0.10, "ease_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.12, 0.75, "ease_in_sine"),
                KeyFrame(0.30, 0.75),
                KeyFrame(0.50, 0.85, "ease_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.14, 0.45, "ease_in_sine"),
                KeyFrame(0.32, 0.45),
                KeyFrame(0.50, 0.10, "ease_out_sine"),
            ],
        },
    )


def clip_sleepy_recover() -> Clip:
    """Eye droops then snaps back, like catching itself falling asleep."""
    return Clip(
        id="sleepy_recover",
        duration=1.0,
        priority=9,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.40, 0.55, "ease_in_sine"),
                KeyFrame(0.55, 0.55),
                KeyFrame(0.65, 0.05, "ease_out_cubic"),
                KeyFrame(0.75, 0.15),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.40, 0.70, "ease_in_sine"),
                KeyFrame(0.55, 0.70),
                KeyFrame(0.65, 0.88, "ease_out_cubic"),
                KeyFrame(1.00, 0.85, "ease_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.42, 0.50, "ease_in_sine"),
                KeyFrame(0.57, 0.50),
                KeyFrame(0.67, 0.07, "ease_out_cubic"),
                KeyFrame(0.77, 0.13),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.42, 0.72, "ease_in_sine"),
                KeyFrame(0.57, 0.72),
                KeyFrame(0.67, 0.87, "ease_out_cubic"),
                KeyFrame(1.00, 0.85, "ease_out_sine"),
            ],
        },
    )


def clip_inner_corner_twitch() -> Clip:
    """One eye adds a tiny inner-corner tension spike."""
    return Clip(
        id="inner_corner_twitch",
        duration=0.3,
        priority=3,
        interruptible=True,
        loop=False,
        tracks={
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.06, 0.18, "ease_out_sine"),
                KeyFrame(0.20, 0.18),
                KeyFrame(0.30, 0.0, "ease_in_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.06, 0.13, "ease_out_sine"),
                KeyFrame(0.20, 0.13),
                KeyFrame(0.30, 0.10, "ease_in_sine"),
            ],
        },
    )


# ---------------------------------------------------------------------------
# Occasional personality beats (8-40s intervals)
# ---------------------------------------------------------------------------

def clip_suspicious_side_eye() -> Clip:
    """One eye narrows more, slight horizontal shift, snap-to-pose hold, snap back."""
    return Clip(
        id="suspicious_side_eye",
        duration=1.4,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.12, 0.32, "ease_out_cubic"),
                KeyFrame(0.85, 0.30),
                KeyFrame(1.05, 0.10, "ease_in_cubic"),
                KeyFrame(1.40, 0.10),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.12, 0.72, "ease_out_cubic"),
                KeyFrame(0.85, 0.74),
                KeyFrame(1.05, 0.85, "ease_in_cubic"),
                KeyFrame(1.40, 0.85),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.35, "ease_out_cubic"),
                KeyFrame(0.85, 0.30),
                KeyFrame(1.05, 0.0, "ease_in_cubic"),
                KeyFrame(1.40, 0.0),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.15, 0.18, "ease_out_cubic"),
                KeyFrame(0.88, 0.16),
                KeyFrame(1.08, 0.10, "ease_in_cubic"),
                KeyFrame(1.40, 0.10),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, 0.30, "ease_out_cubic"),
                KeyFrame(0.88, 0.25),
                KeyFrame(1.08, 0.0, "ease_in_cubic"),
                KeyFrame(1.40, 0.0),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.15, "ease_out_cubic"),
                KeyFrame(0.85, 0.12),
                KeyFrame(1.05, 0.0, "ease_in_cubic"),
                KeyFrame(1.40, 0.0),
            ],
        },
    )


def clip_curious_peek() -> Clip:
    """Both eyes compress and shift upward, one side opens more."""
    return Clip(
        id="curious_peek",
        duration=1.0,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.92, "ease_out_sine"),
                KeyFrame(0.70, 0.90),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.20, 0.04, "ease_out_sine"),
                KeyFrame(0.70, 0.05),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "left.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, -0.30, "ease_out_sine"),
                KeyFrame(0.70, -0.22),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.22, 0.88, "ease_out_sine"),
                KeyFrame(0.72, 0.87),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "right.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.22, -0.22, "ease_out_sine"),
                KeyFrame(0.72, -0.16),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "face.face_offset_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, -0.12, "ease_out_cubic"),
                KeyFrame(0.70, -0.10),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
        },
    )


def clip_tiny_smile_arc() -> Clip:
    """Both eyes soften into a mild happy arc briefly."""
    return Clip(
        id="tiny_smile_arc",
        duration=0.8,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.15, 0.25, "ease_out_sine"),
                KeyFrame(0.55, 0.23),
                KeyFrame(0.80, 0.10, "ease_in_out_sine"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.18, 0.18, "ease_out_sine"),
                KeyFrame(0.55, 0.16),
                KeyFrame(0.80, 0.0, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.17, 0.23, "ease_out_sine"),
                KeyFrame(0.57, 0.21),
                KeyFrame(0.80, 0.10, "ease_in_out_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.20, "ease_out_sine"),
                KeyFrame(0.57, 0.18),
                KeyFrame(0.80, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_double_take_soft() -> Clip:
    """Look one way, return, then smaller second look. Funny and readable."""
    return Clip(
        id="double_take_soft",
        duration=1.8,
        priority=5,
        interruptible=True,
        loop=False,
        tracks={
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.45, "ease_out_cubic"),
                KeyFrame(0.65, 0.0, "ease_in_out_sine"),
                KeyFrame(0.90, 0.35, "ease_out_sine"),
                KeyFrame(1.30, 0.28),
                KeyFrame(1.80, 0.0, "ease_in_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, 0.42, "ease_out_cubic"),
                KeyFrame(0.67, 0.0, "ease_in_out_sine"),
                KeyFrame(0.92, 0.32, "ease_out_sine"),
                KeyFrame(1.32, 0.25),
                KeyFrame(1.80, 0.0, "ease_in_out_sine"),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.20, "ease_out_cubic"),
                KeyFrame(0.65, 0.0, "ease_in_cubic"),
                KeyFrame(0.90, 0.15, "ease_out_cubic"),
                KeyFrame(1.30, 0.12),
                KeyFrame(1.80, 0.0, "ease_in_cubic"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.08),
                KeyFrame(0.65, 0.10),
                KeyFrame(0.90, 0.08),
                KeyFrame(1.30, 0.08),
                KeyFrame(1.80, 0.10),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.27, 0.09),
                KeyFrame(0.67, 0.10),
                KeyFrame(0.92, 0.09),
                KeyFrame(1.32, 0.09),
                KeyFrame(1.80, 0.10),
            ],
        },
    )


def clip_thinking_wobble() -> Clip:
    """Mild alternating left/right asymmetry with pauses and timing offset. Contemplative."""
    return Clip(
        id="thinking_wobble",
        duration=2.0,
        priority=5,
        interruptible=True,
        loop=False,
        tracks={
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.30, 3.0, "ease_in_out_sine"),
                KeyFrame(0.80, 3.0),
                KeyFrame(1.10, -2.0, "ease_in_out_sine"),
                KeyFrame(1.60, -2.0),
                KeyFrame(2.00, 0.0, "ease_in_out_sine"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.38, -2.0, "ease_in_out_sine"),
                KeyFrame(0.88, -2.0),
                KeyFrame(1.18, 3.0, "ease_in_out_sine"),
                KeyFrame(1.68, 3.0),
                KeyFrame(2.00, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_sleepy_nod_face() -> Clip:
    """Eyes droop nearly shut, reopen halfway, then settle. Drowsy."""
    return Clip(
        id="sleepy_nod_face",
        duration=1.5,
        priority=7,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.50, 0.65, "ease_in_sine"),
                KeyFrame(0.75, 0.65),
                KeyFrame(0.90, 0.30, "ease_out_cubic"),
                KeyFrame(1.10, 0.30),
                KeyFrame(1.50, 0.10, "ease_in_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.50, 0.68, "ease_in_sine"),
                KeyFrame(0.75, 0.68),
                KeyFrame(0.90, 0.78, "ease_out_cubic"),
                KeyFrame(1.50, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.52, 0.62, "ease_in_sine"),
                KeyFrame(0.77, 0.62),
                KeyFrame(0.92, 0.28, "ease_out_cubic"),
                KeyFrame(1.12, 0.28),
                KeyFrame(1.50, 0.10, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.52, 0.70, "ease_in_sine"),
                KeyFrame(0.77, 0.70),
                KeyFrame(0.92, 0.80, "ease_out_cubic"),
                KeyFrame(1.50, 0.85, "ease_in_out_sine"),
            ],
        },
    )


def clip_annoyed_flatten() -> Clip:
    """Eyes flatten and angle inward briefly. Post-interruption annoyance."""
    return Clip(
        id="annoyed_flatten",
        duration=0.7,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.10, 0.28, "ease_out_cubic"),
                KeyFrame(0.45, 0.26),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.10, 0.70, "ease_out_cubic"),
                KeyFrame(0.45, 0.72),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, -0.15, "ease_out_cubic"),
                KeyFrame(0.45, -0.13),
                KeyFrame(0.70, 0.0, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.12, 0.25, "ease_out_cubic"),
                KeyFrame(0.47, 0.23),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.12, 0.72, "ease_out_cubic"),
                KeyFrame(0.47, 0.74),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
            "right.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.14, -0.12, "ease_out_cubic"),
                KeyFrame(0.47, -0.10),
                KeyFrame(0.70, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_confused_one_up() -> Clip:
    """One eye slightly taller and more open, the other skeptical."""
    return Clip(
        id="confused_one_up",
        duration=1.0,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.92, "ease_out_sine"),
                KeyFrame(0.70, 0.90),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.20, 0.03, "ease_out_sine"),
                KeyFrame(0.70, 0.05),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.15, "ease_out_sine"),
                KeyFrame(0.70, 0.13),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.22, 0.72, "ease_out_sine"),
                KeyFrame(0.72, 0.74),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.22, 0.22, "ease_out_sine"),
                KeyFrame(0.72, 0.20),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
        },
    )


def clip_shy_soften() -> Clip:
    """Both eyes shrink slightly and drop lower. Timid moment."""
    return Clip(
        id="shy_soften",
        duration=1.0,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.25, 0.72, "ease_in_out_sine"),
                KeyFrame(0.70, 0.74),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.22, "ease_in_out_sine"),
                KeyFrame(0.70, 0.20),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "left.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.10, "ease_in_out_sine"),
                KeyFrame(0.70, 0.08),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.27, 0.74, "ease_in_out_sine"),
                KeyFrame(0.72, 0.76),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.27, 0.20, "ease_in_out_sine"),
                KeyFrame(0.72, 0.18),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "right.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, 0.08, "ease_in_out_sine"),
                KeyFrame(0.72, 0.06),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_proud_focus() -> Clip:
    """Eyes widen just a little, then become clean and stable. Confident."""
    return Clip(
        id="proud_focus",
        duration=1.2,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.92, "ease_out_sine"),
                KeyFrame(0.80, 0.90),
                KeyFrame(1.20, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.20, 0.04, "ease_out_sine"),
                KeyFrame(0.80, 0.06),
                KeyFrame(1.20, 0.10, "ease_in_out_sine"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.10, "ease_out_sine"),
                KeyFrame(0.80, 0.08),
                KeyFrame(1.20, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.22, 0.90, "ease_out_sine"),
                KeyFrame(0.82, 0.88),
                KeyFrame(1.20, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.22, 0.05, "ease_out_sine"),
                KeyFrame(0.82, 0.07),
                KeyFrame(1.20, 0.10, "ease_in_out_sine"),
            ],
        },
    )


# ---------------------------------------------------------------------------
# Rare "wow" moments (45-300s or event-triggered)
# ---------------------------------------------------------------------------

def clip_sleep_peek() -> Clip:
    """One eye opens slightly, glances, closes. During sleep."""
    return Clip(
        id="sleep_peek",
        duration=1.8,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.88),
                KeyFrame(0.30, 0.80, "ease_out_sine"),
                KeyFrame(1.30, 0.82),
                KeyFrame(1.80, 0.88, "ease_in_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.86),
                KeyFrame(0.25, 0.38, "ease_out_sine"),
                KeyFrame(0.40, 0.35),
                KeyFrame(0.90, 0.38),
                KeyFrame(1.40, 0.82, "ease_in_sine"),
                KeyFrame(1.80, 0.86, "ease_in_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.42),
                KeyFrame(0.25, 0.68, "ease_out_sine"),
                KeyFrame(0.40, 0.70),
                KeyFrame(0.90, 0.68),
                KeyFrame(1.40, 0.50, "ease_in_sine"),
                KeyFrame(1.80, 0.42, "ease_in_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.35, 0.15, "ease_out_sine"),
                KeyFrame(0.80, 0.10),
                KeyFrame(1.40, 0.0, "ease_in_sine"),
            ],
        },
    )


def clip_startled_wake() -> Clip:
    """Loud noise while sleeping: eyes snap wide open, rapid blinks, settle."""
    return Clip(
        id="startled_wake",
        duration=1.8,
        priority=15,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.88),
                KeyFrame(0.08, 0.0, "ease_out_cubic"),
                KeyFrame(0.20, 0.0),
                KeyFrame(0.28, 0.80, "ease_in_cubic"),
                KeyFrame(0.35, 0.80),
                KeyFrame(0.45, 0.05, "ease_out_sine"),
                KeyFrame(0.70, 0.05),
                KeyFrame(0.80, 0.50, "ease_in_cubic"),
                KeyFrame(0.88, 0.50),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
                KeyFrame(1.80, 0.10),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.40),
                KeyFrame(0.08, 1.10, "ease_out_cubic"),
                KeyFrame(0.20, 1.05),
                KeyFrame(0.35, 0.72),
                KeyFrame(0.45, 0.95),
                KeyFrame(0.70, 0.90),
                KeyFrame(0.88, 0.78),
                KeyFrame(1.00, 0.85, "ease_out_sine"),
                KeyFrame(1.80, 0.85),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, -0.10),
                KeyFrame(0.15, 0.0, "ease_out_sine"),
                KeyFrame(1.80, 0.0),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.86),
                KeyFrame(0.10, 0.0, "ease_out_cubic"),
                KeyFrame(0.22, 0.0),
                KeyFrame(0.30, 0.78, "ease_in_cubic"),
                KeyFrame(0.37, 0.78),
                KeyFrame(0.47, 0.05, "ease_out_sine"),
                KeyFrame(0.72, 0.05),
                KeyFrame(0.82, 0.48, "ease_in_cubic"),
                KeyFrame(0.90, 0.48),
                KeyFrame(1.02, 0.10, "ease_out_sine"),
                KeyFrame(1.80, 0.10),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.42),
                KeyFrame(0.10, 1.08, "ease_out_cubic"),
                KeyFrame(0.22, 1.03),
                KeyFrame(0.37, 0.74),
                KeyFrame(0.47, 0.93),
                KeyFrame(0.72, 0.88),
                KeyFrame(0.90, 0.80),
                KeyFrame(1.02, 0.85, "ease_out_sine"),
                KeyFrame(1.80, 0.85),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, -0.08),
                KeyFrame(0.17, 0.0, "ease_out_sine"),
                KeyFrame(1.80, 0.0),
            ],
        },
    )


def clip_flinch() -> Clip:
    """Quick squint reaction to loud noise while awake."""
    return Clip(
        id="flinch",
        duration=0.35,
        priority=14,
        interruptible=False,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.06, 0.55, "ease_in_cubic"),
                KeyFrame(0.15, 0.55),
                KeyFrame(0.35, 0.85, "ease_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.06, 0.40, "ease_in_cubic"),
                KeyFrame(0.15, 0.40),
                KeyFrame(0.35, 0.10, "ease_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.08, 0.58, "ease_in_cubic"),
                KeyFrame(0.17, 0.58),
                KeyFrame(0.35, 0.85, "ease_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.08, 0.38, "ease_in_cubic"),
                KeyFrame(0.17, 0.38),
                KeyFrame(0.35, 0.10, "ease_out_sine"),
            ],
        },
    )


def clip_yawn() -> Clip:
    """Slow wide open, hold, slow close. Rare idle behavior."""
    return Clip(
        id="yawn",
        duration=2.2,
        priority=9,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.60, 0.0, "ease_in_out_sine"),
                KeyFrame(1.20, 0.0),
                KeyFrame(1.80, 0.10, "ease_in_out_sine"),
                KeyFrame(2.20, 0.10),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.60, 0.0, "ease_in_out_sine"),
                KeyFrame(1.20, 0.0),
                KeyFrame(1.80, 0.05, "ease_in_out_sine"),
                KeyFrame(2.20, 0.05),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.60, 1.05, "ease_in_out_sine"),
                KeyFrame(1.20, 1.05),
                KeyFrame(1.80, 0.85, "ease_in_out_sine"),
                KeyFrame(2.20, 0.85),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.80, -0.08, "ease_in_out_sine"),
                KeyFrame(1.20, -0.08),
                KeyFrame(1.80, 0.0, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.62, 0.0, "ease_in_out_sine"),
                KeyFrame(1.22, 0.0),
                KeyFrame(1.82, 0.10, "ease_in_out_sine"),
                KeyFrame(2.20, 0.10),
            ],
            "right.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.62, 0.0, "ease_in_out_sine"),
                KeyFrame(1.22, 0.0),
                KeyFrame(1.82, 0.05, "ease_in_out_sine"),
                KeyFrame(2.20, 0.05),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.62, 1.03, "ease_in_out_sine"),
                KeyFrame(1.22, 1.03),
                KeyFrame(1.82, 0.85, "ease_in_out_sine"),
                KeyFrame(2.20, 0.85),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.82, -0.06, "ease_in_out_sine"),
                KeyFrame(1.22, -0.06),
                KeyFrame(1.82, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_boot_scan() -> Clip:
    """Eyes appear as thin lines, widen, shift, stabilize. Boot signature."""
    return Clip(
        id="boot_scan",
        duration=1.8,
        priority=15,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.70),
                KeyFrame(0.40, 0.70),
                KeyFrame(0.80, 0.05, "ease_out_sine"),
                KeyFrame(1.00, 0.05),
                KeyFrame(1.20, 0.10, "ease_in_out_sine"),
                KeyFrame(1.80, 0.10),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.30),
                KeyFrame(0.40, 0.30),
                KeyFrame(0.80, 0.90, "ease_out_sine"),
                KeyFrame(1.00, 0.90),
                KeyFrame(1.20, 0.85, "ease_in_out_sine"),
                KeyFrame(1.80, 0.85),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.60, -0.35, "ease_out_sine"),
                KeyFrame(1.00, 0.25, "ease_in_out_sine"),
                KeyFrame(1.40, 0.0, "ease_in_out_sine"),
                KeyFrame(1.80, 0.0),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.68),
                KeyFrame(0.42, 0.68),
                KeyFrame(0.82, 0.06, "ease_out_sine"),
                KeyFrame(1.02, 0.06),
                KeyFrame(1.22, 0.10, "ease_in_out_sine"),
                KeyFrame(1.80, 0.10),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.32),
                KeyFrame(0.42, 0.32),
                KeyFrame(0.82, 0.88, "ease_out_sine"),
                KeyFrame(1.02, 0.88),
                KeyFrame(1.22, 0.85, "ease_in_out_sine"),
                KeyFrame(1.80, 0.85),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.62, -0.32, "ease_out_sine"),
                KeyFrame(1.02, 0.22, "ease_in_out_sine"),
                KeyFrame(1.42, 0.0, "ease_in_out_sine"),
                KeyFrame(1.80, 0.0),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.60, -0.12, "ease_out_sine"),
                KeyFrame(1.00, 0.08, "ease_in_out_sine"),
                KeyFrame(1.40, 0.0, "ease_in_out_sine"),
                KeyFrame(1.80, 0.0),
            ],
        },
    )


def clip_glitch_split() -> Clip:
    """One-frame left/right mismatch, then recover. Very short, surprising."""
    return Clip(
        id="glitch_split",
        duration=0.25,
        priority=14,
        interruptible=False,
        loop=False,
        tracks={
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.04, -0.30),
                KeyFrame(0.08, 0.225),
                KeyFrame(0.12, -0.15),
                KeyFrame(0.18, 0.075),
                KeyFrame(0.25, 0.0, "ease_in_sine"),
            ],
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.04, -7.5),
                KeyFrame(0.08, 4.5),
                KeyFrame(0.12, -3.0),
                KeyFrame(0.18, 0.0),
                KeyFrame(0.25, 0.0),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.04, 0.27),
                KeyFrame(0.08, -0.18),
                KeyFrame(0.12, 0.12),
                KeyFrame(0.18, -0.045),
                KeyFrame(0.25, 0.0, "ease_in_sine"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.04, 6.0),
                KeyFrame(0.08, -4.5),
                KeyFrame(0.12, 1.5),
                KeyFrame(0.18, 0.0),
                KeyFrame(0.25, 0.0),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.04, -0.10),
                KeyFrame(0.08, 0.08),
                KeyFrame(0.12, -0.05),
                KeyFrame(0.18, 0.02),
                KeyFrame(0.25, 0.0, "ease_in_sine"),
            ],
        },
    )


def clip_prank_side_glance() -> Clip:
    """Both eyes snap to one side and flatten, hold, then blink out."""
    return Clip(
        id="prank_side_glance",
        duration=1.5,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.50, "ease_out_cubic"),
                KeyFrame(0.85, 0.45),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
                KeyFrame(1.50, 0.0),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.12, 0.20, "ease_out_cubic"),
                KeyFrame(0.85, 0.18),
                KeyFrame(1.00, 0.70, "ease_in_cubic"),
                KeyFrame(1.15, 0.70),
                KeyFrame(1.50, 0.10, "ease_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, 0.45, "ease_out_cubic"),
                KeyFrame(0.88, 0.40),
                KeyFrame(1.03, 0.0, "ease_in_cubic"),
                KeyFrame(1.50, 0.0),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.15, 0.18, "ease_out_cubic"),
                KeyFrame(0.88, 0.16),
                KeyFrame(1.03, 0.68, "ease_in_cubic"),
                KeyFrame(1.18, 0.68),
                KeyFrame(1.50, 0.10, "ease_out_sine"),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.25, "ease_out_cubic"),
                KeyFrame(0.85, 0.22),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
                KeyFrame(1.50, 0.0),
            ],
        },
    )


def clip_social_freeze_soften() -> Clip:
    """Eyes lock in focused stare, then soften. After wake-word detect."""
    return Clip(
        id="social_freeze_soften",
        duration=1.0,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.08, 0.92, "ease_out_sine"),
                KeyFrame(0.40, 0.92),
                KeyFrame(0.70, 0.87, "ease_in_out_sine"),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.08, 0.03, "ease_out_sine"),
                KeyFrame(0.40, 0.03),
                KeyFrame(0.70, 0.08, "ease_in_out_sine"),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.10, 0.90, "ease_out_sine"),
                KeyFrame(0.42, 0.90),
                KeyFrame(0.72, 0.86, "ease_in_out_sine"),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.10, 0.05, "ease_out_sine"),
                KeyFrame(0.42, 0.05),
                KeyFrame(0.72, 0.09, "ease_in_out_sine"),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
        },
    )


def clip_dream_flutter() -> Clip:
    """REM-like rapid tiny eyelid quivers during sleep. Looping."""
    return Clip(
        id="dream_flutter",
        duration=2.0,
        priority=2,
        interruptible=False,
        loop=True,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.88),
                KeyFrame(0.20, 0.82, "ease_out_sine"),
                KeyFrame(0.40, 0.88, "ease_in_sine"),
                KeyFrame(0.60, 0.84, "ease_out_sine"),
                KeyFrame(0.80, 0.88, "ease_in_sine"),
                KeyFrame(1.20, 0.88),
                KeyFrame(1.40, 0.83, "ease_out_sine"),
                KeyFrame(1.60, 0.88, "ease_in_sine"),
                KeyFrame(2.00, 0.88),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.86),
                KeyFrame(0.22, 0.84, "ease_out_sine"),
                KeyFrame(0.42, 0.86, "ease_in_sine"),
                KeyFrame(0.62, 0.80, "ease_out_sine"),
                KeyFrame(0.82, 0.86, "ease_in_sine"),
                KeyFrame(1.22, 0.86),
                KeyFrame(1.42, 0.81, "ease_out_sine"),
                KeyFrame(1.62, 0.86, "ease_in_sine"),
                KeyFrame(2.00, 0.86),
            ],
        },
    )


def clip_whip_look() -> Clip:
    """Face rig slams right, overshoots, snaps back."""
    return Clip(
        id="whip_look",
        duration=0.7,
        priority=10,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, 0.80, "ease_out_cubic"),
                KeyFrame(0.25, 0.65, "ease_out_back"),
                KeyFrame(0.35, 0.60),
                KeyFrame(0.50, -0.08, "ease_out_back"),
                KeyFrame(0.70, 0.0),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, 0.30, "ease_out_cubic"),
                KeyFrame(0.35, 0.30),
                KeyFrame(0.50, 0.0),
                KeyFrame(0.70, 0.0),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.17, 0.28, "ease_out_cubic"),
                KeyFrame(0.37, 0.28),
                KeyFrame(0.52, 0.0),
                KeyFrame(0.70, 0.0),
            ],
            "face.face_tilt": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, -4.0, "ease_out_cubic"),
                KeyFrame(0.25, -2.0),
                KeyFrame(0.50, 1.5, "ease_out_back"),
                KeyFrame(0.70, 0.0),
            ],
        },
    )


def clip_recoil_bounce() -> Clip:
    """Rig throws backward/up, bounces, settles."""
    return Clip(
        id="recoil_bounce",
        duration=0.9,
        priority=12,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, -0.55, "ease_out_cubic"),
                KeyFrame(0.40, 0.12, "ease_out_back"),
                KeyFrame(0.55, -0.08, "ease_out_back"),
                KeyFrame(0.70, 0.03),
                KeyFrame(0.90, 0.0),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.15, -0.15, "ease_out_cubic"),
                KeyFrame(0.45, 0.0),
                KeyFrame(0.90, 0.0),
            ],
            "face.face_scale": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.15, 1.15, "ease_out_cubic"),
                KeyFrame(0.40, 0.92, "ease_out_back"),
                KeyFrame(0.55, 1.03),
                KeyFrame(0.90, 1.0),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.15, 1.15, "ease_out_cubic"),
                KeyFrame(0.40, 0.80, "ease_out_back"),
                KeyFrame(0.55, 0.88),
                KeyFrame(0.90, 0.85),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.17, 1.15, "ease_out_cubic"),
                KeyFrame(0.42, 0.80, "ease_out_back"),
                KeyFrame(0.57, 0.88),
                KeyFrame(0.90, 0.85),
            ],
        },
    )


def clip_peek_from_edge() -> Clip:
    """Face starts off-screen, slides in with tilt."""
    return Clip(
        id="peek_from_edge",
        duration=1.6,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_x": [
                KeyFrame(0.00, 2.5),
                KeyFrame(0.50, 2.5),
                KeyFrame(0.85, 0.35, "ease_out_cubic"),
                KeyFrame(1.05, 0.15, "ease_out_back"),
                KeyFrame(1.20, 0.15),
                KeyFrame(1.60, 0.0, "ease_in_cubic"),
            ],
            "face.face_tilt": [
                KeyFrame(0.00, 8.0),
                KeyFrame(0.50, 8.0),
                KeyFrame(0.85, -2.0, "ease_out_back"),
                KeyFrame(1.05, 0.0),
                KeyFrame(1.60, 0.0),
            ],
            "face.eye_gap": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.50, 0.85),
                KeyFrame(1.05, 1.05, "ease_out_back"),
                KeyFrame(1.60, 1.0),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.50, 0.85),
                KeyFrame(0.87, 0.90, "ease_out_back"),
                KeyFrame(1.60, 0.85),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.50, 0.85),
                KeyFrame(0.89, 0.88, "ease_out_back"),
                KeyFrame(1.60, 0.85),
            ],
        },
    )


def clip_squash_pop() -> Clip:
    """Compress down, spring tall with widened gap."""
    return Clip(
        id="squash_pop",
        duration=0.8,
        priority=10,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_scale": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.20, 0.80, "ease_in_cubic"),
                KeyFrame(0.30, 0.80),
                KeyFrame(0.45, 1.25, "ease_out_back"),
                KeyFrame(0.60, 1.08),
                KeyFrame(0.80, 1.0),
            ],
            "face.eye_gap": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.20, 0.80, "ease_in_cubic"),
                KeyFrame(0.30, 0.80),
                KeyFrame(0.45, 1.35, "ease_out_back"),
                KeyFrame(0.60, 1.10),
                KeyFrame(0.80, 1.0),
            ],
            "face.face_offset_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.15, "ease_in_cubic"),
                KeyFrame(0.45, -0.20, "ease_out_back"),
                KeyFrame(0.60, -0.05),
                KeyFrame(0.80, 0.0),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.60, "ease_in_cubic"),
                KeyFrame(0.45, 1.10, "ease_out_back"),
                KeyFrame(0.60, 0.87),
                KeyFrame(0.80, 0.85),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.22, 0.60, "ease_in_cubic"),
                KeyFrame(0.47, 1.10, "ease_out_back"),
                KeyFrame(0.62, 0.87),
                KeyFrame(0.80, 0.85),
            ],
        },
    )


def clip_orbit_search() -> Clip:
    """Eyes trace arc path with face_tilt."""
    return Clip(
        id="orbit_search",
        duration=2.0,
        priority=6,
        interruptible=True,
        loop=False,
        tracks={
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, 0.25, "ease_out_cubic"),
                KeyFrame(0.80, 0.20),
                KeyFrame(1.20, -0.15),
                KeyFrame(1.50, -0.10),
                KeyFrame(1.80, 0.05),
                KeyFrame(2.00, 0.0),
            ],
            "left.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, -0.25, "ease_out_cubic"),
                KeyFrame(0.80, -0.15),
                KeyFrame(1.20, -0.10),
                KeyFrame(1.50, -0.05),
                KeyFrame(1.80, 0.0),
                KeyFrame(2.00, 0.0),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.42, 0.22, "ease_out_cubic"),
                KeyFrame(0.82, 0.18),
                KeyFrame(1.22, -0.13),
                KeyFrame(1.52, -0.08),
                KeyFrame(1.82, 0.04),
                KeyFrame(2.00, 0.0),
            ],
            "right.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.42, -0.22, "ease_out_cubic"),
                KeyFrame(0.82, -0.13),
                KeyFrame(1.22, -0.08),
                KeyFrame(1.52, -0.04),
                KeyFrame(1.82, 0.0),
                KeyFrame(2.00, 0.0),
            ],
            "face.face_tilt": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, 5.0, "ease_out_cubic"),
                KeyFrame(0.80, 3.0),
                KeyFrame(1.20, -4.0),
                KeyFrame(1.60, -2.0),
                KeyFrame(2.00, 0.0),
            ],
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, 0.12, "ease_out_cubic"),
                KeyFrame(0.80, 0.10),
                KeyFrame(1.20, -0.08),
                KeyFrame(1.60, -0.05),
                KeyFrame(2.00, 0.0),
            ],
        },
    )


def clip_panic_pingpong() -> Clip:
    """Fast screen-crossing looks, shrinking amplitude."""
    return Clip(
        id="panic_pingpong",
        duration=1.2,
        priority=12,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.60, "ease_out_cubic"),
                KeyFrame(0.20, 0.60),
                KeyFrame(0.30, -0.45, "ease_out_cubic"),
                KeyFrame(0.38, -0.45),
                KeyFrame(0.48, 0.30),
                KeyFrame(0.54, 0.30),
                KeyFrame(0.64, -0.20),
                KeyFrame(0.70, -0.20),
                KeyFrame(0.80, 0.10),
                KeyFrame(1.20, 0.0),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.35, "ease_out_cubic"),
                KeyFrame(0.20, 0.35),
                KeyFrame(0.30, -0.28, "ease_out_cubic"),
                KeyFrame(0.38, -0.28),
                KeyFrame(0.48, 0.20),
                KeyFrame(0.54, 0.20),
                KeyFrame(0.64, -0.12),
                KeyFrame(0.70, -0.12),
                KeyFrame(0.80, 0.06),
                KeyFrame(1.20, 0.0),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.14, 0.35, "ease_out_cubic"),
                KeyFrame(0.22, 0.35),
                KeyFrame(0.32, -0.28, "ease_out_cubic"),
                KeyFrame(0.40, -0.28),
                KeyFrame(0.50, 0.20),
                KeyFrame(0.56, 0.20),
                KeyFrame(0.66, -0.12),
                KeyFrame(0.72, -0.12),
                KeyFrame(0.82, 0.06),
                KeyFrame(1.20, 0.0),
            ],
            "face.face_scale": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.12, 1.08, "ease_out_cubic"),
                KeyFrame(0.60, 1.06),
                KeyFrame(1.20, 1.0),
            ],
        },
    )


def clip_happy_hop() -> Clip:
    """Rig jumps up with squashed landing."""
    return Clip(
        id="happy_hop",
        duration=0.9,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.10, 0.10, "ease_in_cubic"),
                KeyFrame(0.20, -0.50, "ease_out_cubic"),
                KeyFrame(0.45, -0.50),
                KeyFrame(0.55, 0.18, "ease_in_cubic"),
                KeyFrame(0.60, 0.18),
                KeyFrame(0.70, -0.05, "ease_out_back"),
                KeyFrame(0.90, 0.0),
            ],
            "face.face_scale": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.10, 0.88),
                KeyFrame(0.20, 1.10),
                KeyFrame(0.45, 1.10),
                KeyFrame(0.55, 0.85),
                KeyFrame(0.70, 1.04),
                KeyFrame(0.90, 1.0),
            ],
            "face.eye_gap": [
                KeyFrame(0.00, 1.0),
                KeyFrame(0.55, 0.85),
                KeyFrame(0.70, 1.08, "ease_out_back"),
                KeyFrame(0.90, 1.0),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.35, "ease_out_cubic"),
                KeyFrame(0.55, 0.30),
                KeyFrame(0.90, 0.0),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, 0.35, "ease_out_cubic"),
                KeyFrame(0.57, 0.30),
                KeyFrame(0.90, 0.0),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.40, "ease_out_cubic"),
                KeyFrame(0.55, 0.35),
                KeyFrame(0.90, 0.10),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.27, 0.40, "ease_out_cubic"),
                KeyFrame(0.57, 0.35),
                KeyFrame(0.90, 0.10),
            ],
        },
    )


def clip_dramatic_side_freeze() -> Clip:
    """Hard offset, freeze, tiny blink, release."""
    return Clip(
        id="dramatic_side_freeze",
        duration=2.0,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "face.face_offset_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 1.20, "ease_out_cubic"),
                KeyFrame(1.35, 1.20),
                KeyFrame(1.50, 1.10),
                KeyFrame(2.00, 0.0, "ease_in_cubic"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.25, "ease_out_cubic"),
                KeyFrame(1.35, 0.25),
                KeyFrame(1.50, 0.0),
                KeyFrame(2.00, 0.0),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.22, 0.22, "ease_out_cubic"),
                KeyFrame(1.37, 0.22),
                KeyFrame(1.52, 0.0),
                KeyFrame(2.00, 0.0),
            ],
            "face.face_tilt": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, -3.0, "ease_out_cubic"),
                KeyFrame(1.35, -3.0),
                KeyFrame(2.00, 0.0),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.70, 0.10),
                KeyFrame(0.75, 0.60, "ease_in_cubic"),
                KeyFrame(0.85, 0.60),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
                KeyFrame(2.00, 0.10),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.72, 0.10),
                KeyFrame(0.77, 0.60, "ease_in_cubic"),
                KeyFrame(0.87, 0.60),
                KeyFrame(1.02, 0.10, "ease_out_sine"),
                KeyFrame(2.00, 0.10),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.78, "ease_out_cubic"),
                KeyFrame(1.35, 0.78),
                KeyFrame(2.00, 0.85),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.22, 0.78, "ease_out_cubic"),
                KeyFrame(1.37, 0.78),
                KeyFrame(2.00, 0.85),
            ],
        },
    )


# ---------------------------------------------------------------------------
# Per-state behavior pools
# ---------------------------------------------------------------------------

IDLE_STATES = {State.IDLE, State.HAPPY, State.SAD, State.CONFUSED, State.ANGRY, State.ERROR}
AWAKE_STATES = IDLE_STATES | {State.LISTENING, State.THINKING, State.SPEAKING, State.WAKING}
ALL_STATES = AWAKE_STATES | {State.SLEEPING, State.BOOTING}


BEHAVIOR_DEFS: List[BehaviorDef] = [
    # --- Common micro-idles ---
    BehaviorDef("soft_squish", clip_soft_squish, "common", 1.0, 1.0, AWAKE_STATES),
    BehaviorDef("micro_tilt_swap", clip_micro_tilt_swap, "common", 0.8, 2.0, AWAKE_STATES),
    BehaviorDef("tiny_focus_narrow", clip_tiny_focus_narrow, "common", 0.6, 1.5, {State.IDLE, State.LISTENING, State.THINKING}),
    BehaviorDef("lazy_half_blink", clip_lazy_half_blink, "common", 0.3, 3.0, {State.IDLE, State.LISTENING}),
    BehaviorDef("sleepy_recover", clip_sleepy_recover, "common", 0.4, 8.0, {State.IDLE}),
    BehaviorDef("inner_corner_twitch", clip_inner_corner_twitch, "common", 0.5, 2.0, {State.IDLE, State.LISTENING, State.THINKING}),
    # --- Occasional personality beats ---
    BehaviorDef("suspicious_side_eye", clip_suspicious_side_eye, "occasional", 1.0, 15.0, {State.IDLE, State.THINKING}),
    BehaviorDef("curious_peek", clip_curious_peek, "occasional", 0.8, 12.0, {State.IDLE, State.LISTENING}),
    BehaviorDef("tiny_smile_arc", clip_tiny_smile_arc, "occasional", 0.6, 20.0, {State.IDLE, State.HAPPY}),
    BehaviorDef("double_take_soft", clip_double_take_soft, "occasional", 1.0, 25.0, {State.IDLE}),
    BehaviorDef("thinking_wobble", clip_thinking_wobble, "occasional", 0.8, 15.0, {State.THINKING}),
    BehaviorDef("sleepy_nod_face", clip_sleepy_nod_face, "occasional", 0.5, 30.0, {State.IDLE}),
    BehaviorDef("annoyed_flatten", clip_annoyed_flatten, "occasional", 0.6, 20.0, {State.IDLE, State.THINKING, State.CONFUSED}),
    BehaviorDef("confused_one_up", clip_confused_one_up, "occasional", 0.7, 15.0, {State.CONFUSED, State.IDLE}),
    BehaviorDef("shy_soften", clip_shy_soften, "occasional", 0.5, 25.0, {State.IDLE, State.LISTENING}),
    BehaviorDef("proud_focus", clip_proud_focus, "occasional", 0.4, 20.0, {State.IDLE, State.LISTENING}),
    # --- Rare "wow" moments ---
    BehaviorDef("sleep_peek", clip_sleep_peek, "rare", 1.0, 120.0, {State.SLEEPING}),
    BehaviorDef("startled_wake", clip_startled_wake, "rare", 1.0, 60.0, {State.SLEEPING}),
    BehaviorDef("flinch", clip_flinch, "rare", 1.0, 10.0, AWAKE_STATES),
    BehaviorDef("yawn", clip_yawn, "rare", 1.0, 180.0, {State.IDLE}),
    BehaviorDef("boot_scan", clip_boot_scan, "rare", 1.0, 300.0, {State.BOOTING}),
    BehaviorDef("glitch_split", clip_glitch_split, "rare", 0.5, 120.0, {State.IDLE, State.ERROR}),
    BehaviorDef("prank_side_glance", clip_prank_side_glance, "rare", 0.6, 150.0, {State.IDLE}),
    BehaviorDef("social_freeze_soften", clip_social_freeze_soften, "rare", 0.8, 30.0, {State.IDLE, State.LISTENING}),
    BehaviorDef("dream_flutter", clip_dream_flutter, "rare", 1.0, 60.0, {State.SLEEPING}),
    # --- New travel clips ---
    BehaviorDef("whip_look", clip_whip_look, "rare", 0.6, 60.0, {State.IDLE, State.LISTENING}),
    BehaviorDef("recoil_bounce", clip_recoil_bounce, "rare", 0.8, 30.0, AWAKE_STATES),
    BehaviorDef("peek_from_edge", clip_peek_from_edge, "rare", 0.5, 180.0, {State.IDLE}),
    BehaviorDef("squash_pop", clip_squash_pop, "rare", 0.7, 90.0, {State.IDLE, State.HAPPY}),
    BehaviorDef("orbit_search", clip_orbit_search, "occasional", 0.6, 25.0, {State.THINKING, State.IDLE}),
    BehaviorDef("panic_pingpong", clip_panic_pingpong, "rare", 0.4, 120.0, {State.CONFUSED, State.ERROR}),
    BehaviorDef("happy_hop", clip_happy_hop, "occasional", 0.7, 20.0, {State.IDLE, State.HAPPY}),
    BehaviorDef("dramatic_side_freeze", clip_dramatic_side_freeze, "rare", 0.3, 240.0, {State.IDLE}),
]


def build_state_pools() -> Dict[State, Dict[str, List[BehaviorDef]]]:
    """Build per-state pools indexed by tier."""
    pools: Dict[State, Dict[str, List[BehaviorDef]]] = {}
    for state in State:
        pools[state] = {"common": [], "occasional": [], "rare": []}

    for bdef in BEHAVIOR_DEFS:
        for state in bdef.allowed_states:
            pools[state][bdef.tier].append(bdef)

    return pools


# All clip factories for AnimationLibrary registration
ALL_CLIP_FACTORIES = {
    "soft_squish": clip_soft_squish,
    "micro_tilt_swap": clip_micro_tilt_swap,
    "tiny_focus_narrow": clip_tiny_focus_narrow,
    "lazy_half_blink": clip_lazy_half_blink,
    "sleepy_recover": clip_sleepy_recover,
    "inner_corner_twitch": clip_inner_corner_twitch,
    "suspicious_side_eye": clip_suspicious_side_eye,
    "curious_peek": clip_curious_peek,
    "tiny_smile_arc": clip_tiny_smile_arc,
    "double_take_soft": clip_double_take_soft,
    "thinking_wobble": clip_thinking_wobble,
    "sleepy_nod_face": clip_sleepy_nod_face,
    "annoyed_flatten": clip_annoyed_flatten,
    "confused_one_up": clip_confused_one_up,
    "shy_soften": clip_shy_soften,
    "proud_focus": clip_proud_focus,
    "sleep_peek": clip_sleep_peek,
    "startled_wake": clip_startled_wake,
    "flinch": clip_flinch,
    "yawn": clip_yawn,
    "boot_scan": clip_boot_scan,
    "glitch_split": clip_glitch_split,
    "prank_side_glance": clip_prank_side_glance,
    "social_freeze_soften": clip_social_freeze_soften,
    "dream_flutter": clip_dream_flutter,
    "whip_look": clip_whip_look,
    "recoil_bounce": clip_recoil_bounce,
    "peek_from_edge": clip_peek_from_edge,
    "squash_pop": clip_squash_pop,
    "orbit_search": clip_orbit_search,
    "panic_pingpong": clip_panic_pingpong,
    "happy_hop": clip_happy_hop,
    "dramatic_side_freeze": clip_dramatic_side_freeze,
}