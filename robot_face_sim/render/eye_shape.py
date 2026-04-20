import math
from typing import List, Tuple

from ..core.types import EyeParameters

Point = Tuple[float, float]


def generate_eye_contour(
    eye: EyeParameters, base_width: int = 48, base_height: int = 64
) -> List[Tuple[int, int]]:
    """Generate polygon contour for eye shape from parameters"""
    points: List[Point] = []
    steps = 16

    # Base capsule shape
    for i in range(steps):
        angle = (i / steps) * math.pi * 2
        rx = base_width * 0.5 * eye.scale_x * eye.squash
        ry = base_height * 0.5 * eye.scale_y * eye.stretch

        x = math.cos(angle) * rx
        y = math.sin(angle) * ry

        # Apply corner shaping
        if angle < math.pi * 0.5 or angle > math.pi * 1.5:
            # Inner corner
            y += eye.inner_corner_raise * 6.0
        else:
            # Outer corner
            y += eye.outer_corner_raise * 6.0

        # Apply top cut
        top_cut_line = ry * (1.0 - eye.top_cut)
        if y < -top_cut_line:
            y = -top_cut_line

        # Apply bottom cut
        bottom_cut_line = ry * (1.0 - eye.bottom_cut)
        if y > bottom_cut_line:
            y = bottom_cut_line

        points.append((x, y))

    # Rotate
    rad = math.radians(eye.rotation_deg)
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)
    points = [(x * cos_r - y * sin_r, x * sin_r + y * cos_r) for x, y in points]

    # Translate to center
    cx = base_width // 2 + eye.center_x * 8
    cy = base_height // 2 + eye.center_y * 8

    return [(int(cx + x), int(cy + y)) for x, y in points]


# Canonical shape presets
PRESETS = {
    "neutral_soft": EyeParameters(
        scale_x=0.95,
        scale_y=0.85,
        inner_corner_raise=0.0,
        outer_corner_raise=0.0,
        top_cut=0.1,
        bottom_cut=0.05,
        roundness=0.7,
    ),
    "sleepy_droop": EyeParameters(
        scale_x=0.9,
        scale_y=0.6,
        inner_corner_raise=0.1,
        outer_corner_raise=-0.3,
        top_cut=0.25,
        bottom_cut=0.2,
        roundness=0.9,
    ),
    "angry_slant": EyeParameters(
        scale_x=0.8,
        scale_y=0.7,
        inner_corner_raise=-0.4,
        outer_corner_raise=0.2,
        rotation_deg=-6.0,
        top_cut=0.0,
        bottom_cut=0.3,
        roundness=0.3,
    ),
    "happy_arc": EyeParameters(
        scale_x=1.0,
        scale_y=0.55,
        inner_corner_raise=0.25,
        outer_corner_raise=0.35,
        top_cut=0.5,
        bottom_cut=0.0,
        roundness=0.8,
    ),
    "focused_narrow": EyeParameters(
        scale_x=0.95,
        scale_y=0.5,
        inner_corner_raise=0.0,
        outer_corner_raise=0.0,
        top_cut=0.35,
        bottom_cut=0.35,
        roundness=0.2,
    ),
    "closed_soft": EyeParameters(
        scale_x=0.9, scale_y=0.15, top_cut=0.85, bottom_cut=0.85, roundness=0.9
    ),
    "surprised_open": EyeParameters(
        scale_x=1.1,
        scale_y=1.1,
        inner_corner_raise=0.0,
        outer_corner_raise=0.0,
        top_cut=0.0,
        bottom_cut=0.0,
        roundness=0.85,
    ),
    "curious_tilt": EyeParameters(
        scale_x=0.9,
        scale_y=0.85,
        rotation_deg=5.0,
        inner_corner_raise=-0.15,
        outer_corner_raise=0.2,
        top_cut=0.1,
        bottom_cut=0.1,
        roundness=0.65,
    ),
}
