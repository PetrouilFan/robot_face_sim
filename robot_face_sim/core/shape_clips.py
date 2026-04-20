from ..core.types import KeyFrame, Clip

# Base neutral values (from PRESETS["neutral_soft"] used by simulator)
# top_cut=0.10, bottom_cut=0.05, scale_x=0.95, scale_y=0.85
# center_x=0.0, center_y=0.0, inner_corner_raise=0.0, outer_corner_raise=0.0
# rotation_deg=0.0


def clip_blink() -> Clip:
    """Natural blink: fast close, brief hold, slower open. 20ms right-eye delay."""
    return Clip(
        id="blink",
        duration=0.38,
        priority=10,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.09, 0.90, "ease_in_cubic"),
                KeyFrame(0.14, 0.90),
                KeyFrame(0.35, 0.10, "ease_out_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.09, 0.85, "ease_in_cubic"),
                KeyFrame(0.14, 0.85),
                KeyFrame(0.35, 0.05, "ease_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.09, 0.70, "ease_in_cubic"),
                KeyFrame(0.14, 0.70),
                KeyFrame(0.35, 0.85, "ease_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.02, 0.10),
                KeyFrame(0.11, 0.88, "ease_in_cubic"),
                KeyFrame(0.16, 0.88),
                KeyFrame(0.37, 0.10, "ease_out_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.02, 0.05),
                KeyFrame(0.11, 0.83, "ease_in_cubic"),
                KeyFrame(0.16, 0.83),
                KeyFrame(0.37, 0.05, "ease_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.02, 0.85),
                KeyFrame(0.11, 0.72, "ease_in_cubic"),
                KeyFrame(0.16, 0.72),
                KeyFrame(0.37, 0.85, "ease_out_sine"),
            ],
        },
    )


def clip_double_blink() -> Clip:
    """Two quick blinks, second one slightly smaller."""
    return Clip(
        id="double_blink",
        duration=0.65,
        priority=10,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.08, 0.88, "ease_in_cubic"),
                KeyFrame(0.12, 0.88),
                KeyFrame(0.25, 0.10, "ease_out_sine"),
                KeyFrame(0.33, 0.75, "ease_in_cubic"),
                KeyFrame(0.37, 0.75),
                KeyFrame(0.50, 0.10, "ease_out_sine"),
                KeyFrame(0.65, 0.10),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.08, 0.82, "ease_in_cubic"),
                KeyFrame(0.12, 0.82),
                KeyFrame(0.25, 0.05, "ease_out_sine"),
                KeyFrame(0.33, 0.70, "ease_in_cubic"),
                KeyFrame(0.37, 0.70),
                KeyFrame(0.50, 0.05, "ease_out_sine"),
                KeyFrame(0.65, 0.05),
            ],
            "right.top_cut": [
                KeyFrame(0.02, 0.10),
                KeyFrame(0.10, 0.86, "ease_in_cubic"),
                KeyFrame(0.14, 0.86),
                KeyFrame(0.27, 0.10, "ease_out_sine"),
                KeyFrame(0.35, 0.73, "ease_in_cubic"),
                KeyFrame(0.39, 0.73),
                KeyFrame(0.52, 0.10, "ease_out_sine"),
                KeyFrame(0.65, 0.10),
            ],
            "right.bottom_cut": [
                KeyFrame(0.02, 0.05),
                KeyFrame(0.10, 0.80, "ease_in_cubic"),
                KeyFrame(0.14, 0.80),
                KeyFrame(0.27, 0.05, "ease_out_sine"),
                KeyFrame(0.35, 0.68, "ease_in_cubic"),
                KeyFrame(0.39, 0.68),
                KeyFrame(0.52, 0.05, "ease_out_sine"),
                KeyFrame(0.65, 0.05),
            ],
        },
    )


def clip_happy() -> Clip:
    """Joyful squint: compressed vertically, widened horizontally (volume preservation)."""
    return Clip(
        id="happy",
        duration=1.2,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.18, 0.56, "ease_out_back"),
                KeyFrame(0.90, 0.52),
                KeyFrame(1.20, 0.10, "ease_in_out_sine"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.40, "ease_out_quad"),
                KeyFrame(0.90, 0.38),
                KeyFrame(1.20, 0.0, "ease_in_out_sine"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.18, "ease_out_quad"),
                KeyFrame(0.90, 0.16),
                KeyFrame(1.20, 0.0, "ease_in_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.18, 0.60, "ease_out_back"),
                KeyFrame(0.90, 0.62),
                KeyFrame(1.20, 0.85, "ease_in_out_sine"),
            ],
            "left.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.20, 1.15, "ease_out_quad"),
                KeyFrame(0.90, 1.12),
                KeyFrame(1.20, 0.95, "ease_in_out_sine"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.20, 0.12, "ease_out_back"),
                KeyFrame(0.90, 0.10),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.54, "ease_out_back"),
                KeyFrame(0.95, 0.50),
                KeyFrame(1.20, 0.10, "ease_in_out_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, 0.42, "ease_out_quad"),
                KeyFrame(0.95, 0.40),
                KeyFrame(1.20, 0.0, "ease_in_out_sine"),
            ],
            "right.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, 0.20, "ease_out_quad"),
                KeyFrame(0.95, 0.18),
                KeyFrame(1.20, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.25, 0.62, "ease_out_back"),
                KeyFrame(0.95, 0.64),
                KeyFrame(1.20, 0.85, "ease_in_out_sine"),
            ],
            "right.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.27, 1.17, "ease_out_quad"),
                KeyFrame(0.95, 1.14),
                KeyFrame(1.20, 0.95, "ease_in_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.27, -0.12, "ease_out_back"),
                KeyFrame(0.95, -0.10),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
        },
    )


def clip_surprised() -> Clip:
    """Wide eyes: taller AND narrower (volume preservation), spaced apart, sharp snap."""
    return Clip(
        id="surprised",
        duration=0.7,
        priority=12,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.12, 1.20, "ease_out_cubic"),
                KeyFrame(0.50, 1.15),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
            "left.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.12, 0.85, "ease_out_cubic"),
                KeyFrame(0.50, 0.87),
                KeyFrame(0.70, 0.95, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.10, 0.0, "ease_out_sine"),
                KeyFrame(0.50, 0.0),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.10, 0.0, "ease_out_sine"),
                KeyFrame(0.50, 0.0),
                KeyFrame(0.70, 0.05, "ease_in_out_sine"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.12, 0.22, "ease_out_cubic"),
                KeyFrame(0.50, 0.18),
                KeyFrame(0.70, 0.0, "ease_in_cubic"),
            ],
            "right.scale_y": [
                KeyFrame(0.02, 0.85),
                KeyFrame(0.14, 1.18, "ease_out_cubic"),
                KeyFrame(0.52, 1.13),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
            "right.scale_x": [
                KeyFrame(0.02, 0.95),
                KeyFrame(0.14, 0.83, "ease_out_cubic"),
                KeyFrame(0.52, 0.85),
                KeyFrame(0.70, 0.95, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.02, 0.10),
                KeyFrame(0.12, 0.0, "ease_out_sine"),
                KeyFrame(0.52, 0.0),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.02, 0.05),
                KeyFrame(0.12, 0.0, "ease_out_sine"),
                KeyFrame(0.52, 0.0),
                KeyFrame(0.70, 0.05, "ease_in_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.02, 0.0),
                KeyFrame(0.14, -0.22, "ease_out_cubic"),
                KeyFrame(0.52, -0.18),
                KeyFrame(0.70, 0.0, "ease_in_cubic"),
            ],
        },
    )


def clip_angry() -> Clip:
    """Inner corners down, narrow slit, converging tilt and spacing, volume preserved."""
    return Clip(
        id="angry",
        duration=1.0,
        priority=12,
        interruptible=True,
        loop=False,
        tracks={
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, -0.35, "ease_out_cubic"),
                KeyFrame(0.75, -0.33),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.15, "ease_out_cubic"),
                KeyFrame(0.75, 0.13),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.30, "ease_out_cubic"),
                KeyFrame(0.75, 0.28),
                KeyFrame(1.00, 0.10, "ease_in_cubic"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.25, 0.15, "ease_out_cubic"),
                KeyFrame(0.75, 0.13),
                KeyFrame(1.00, 0.05, "ease_in_cubic"),
            ],
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, -8.0, "ease_out_cubic"),
                KeyFrame(0.75, -7.0),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, -0.25, "ease_out_cubic"),
                KeyFrame(0.75, -0.22),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.25, 0.65, "ease_out_cubic"),
                KeyFrame(0.75, 0.67),
                KeyFrame(1.00, 0.85, "ease_in_cubic"),
            ],
            "left.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.25, 1.12, "ease_out_cubic"),
                KeyFrame(0.75, 1.10),
                KeyFrame(1.00, 0.95, "ease_in_cubic"),
            ],
            "right.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, -0.37, "ease_out_cubic"),
                KeyFrame(0.82, -0.35),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, 0.17, "ease_out_cubic"),
                KeyFrame(0.82, 0.15),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.32, 0.28, "ease_out_cubic"),
                KeyFrame(0.82, 0.26),
                KeyFrame(1.00, 0.10, "ease_in_cubic"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.32, 0.13, "ease_out_cubic"),
                KeyFrame(0.82, 0.11),
                KeyFrame(1.00, 0.05, "ease_in_cubic"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, 8.0, "ease_out_cubic"),
                KeyFrame(0.82, 7.0),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, 0.25, "ease_out_cubic"),
                KeyFrame(0.82, 0.22),
                KeyFrame(1.00, 0.0, "ease_in_cubic"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.32, 0.67, "ease_out_cubic"),
                KeyFrame(0.82, 0.69),
                KeyFrame(1.00, 0.85, "ease_in_cubic"),
            ],
            "right.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.32, 1.14, "ease_out_cubic"),
                KeyFrame(0.82, 1.12),
                KeyFrame(1.00, 0.95, "ease_in_cubic"),
            ],
        },
    )


def clip_sad() -> Clip:
    """Droopy outer corners, pleading inner corners, tilt inward-up, slow onset."""
    return Clip(
        id="sad",
        duration=1.5,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.50, -0.30, "ease_in_out_sine"),
                KeyFrame(1.10, -0.28),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.50, 0.15, "ease_in_out_sine"),
                KeyFrame(1.10, 0.13),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.50, 7.0, "ease_in_out_sine"),
                KeyFrame(1.10, 6.0),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.50, 0.15, "ease_in_out_sine"),
                KeyFrame(1.10, 0.12),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.50, 0.22, "ease_in_out_sine"),
                KeyFrame(1.10, 0.20),
                KeyFrame(1.50, 0.10, "ease_in_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.50, 0.70, "ease_in_out_sine"),
                KeyFrame(1.10, 0.72),
                KeyFrame(1.50, 0.85, "ease_in_out_sine"),
            ],
            "left.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.50, 1.08, "ease_in_out_sine"),
                KeyFrame(1.10, 1.06),
                KeyFrame(1.50, 0.95, "ease_in_out_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.57, -0.32, "ease_in_out_sine"),
                KeyFrame(1.17, -0.30),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "right.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.57, 0.17, "ease_in_out_sine"),
                KeyFrame(1.17, 0.15),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.57, -7.0, "ease_in_out_sine"),
                KeyFrame(1.17, -6.0),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.57, -0.15, "ease_in_out_sine"),
                KeyFrame(1.17, -0.12),
                KeyFrame(1.50, 0.0, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.57, 0.24, "ease_in_out_sine"),
                KeyFrame(1.17, 0.22),
                KeyFrame(1.50, 0.10, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.57, 0.72, "ease_in_out_sine"),
                KeyFrame(1.17, 0.74),
                KeyFrame(1.50, 0.85, "ease_in_out_sine"),
            ],
            "right.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.57, 1.10, "ease_in_out_sine"),
                KeyFrame(1.17, 1.08),
                KeyFrame(1.50, 0.95, "ease_in_out_sine"),
            ],
        },
    )


def clip_confused() -> Clip:
    """Asymmetric: left eye wider with tilt, right eye narrower. Timing offset + center_x."""
    return Clip(
        id="confused",
        duration=1.0,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.25, 0.95, "ease_out_back"),
                KeyFrame(0.75, 0.93),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.25, 0.03, "ease_out_quad"),
                KeyFrame(0.75, 0.05),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 10.0, "ease_out_back"),
                KeyFrame(0.75, 8.0),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.20, "ease_out_quad"),
                KeyFrame(0.75, 0.18),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.18, "ease_out_back"),
                KeyFrame(0.75, 0.15),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.33, 0.75, "ease_out_quad"),
                KeyFrame(0.83, 0.77),
                KeyFrame(1.00, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.33, 0.20, "ease_out_quad"),
                KeyFrame(0.83, 0.18),
                KeyFrame(1.00, 0.10, "ease_in_out_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.33, -0.10, "ease_out_quad"),
                KeyFrame(0.83, -0.08),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.33, -0.10, "ease_out_quad"),
                KeyFrame(0.83, -0.08),
                KeyFrame(1.00, 0.0, "ease_in_out_sine"),
            ],
        },
    )


def clip_thinking() -> Clip:
    """Eyes glance upward, slight narrow, converging center_x for focus."""
    return Clip(
        id="thinking",
        duration=1.8,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.35, -0.45, "ease_out_cubic"),
                KeyFrame(1.30, -0.40),
                KeyFrame(1.80, 0.0, "ease_in_cubic"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.35, -0.15, "ease_out_cubic"),
                KeyFrame(1.30, -0.12),
                KeyFrame(1.80, 0.0, "ease_in_cubic"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.35, 0.22, "ease_out_cubic"),
                KeyFrame(1.30, 0.20),
                KeyFrame(1.80, 0.10, "ease_in_cubic"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.35, 0.75, "ease_out_cubic"),
                KeyFrame(1.30, 0.77),
                KeyFrame(1.80, 0.85, "ease_in_cubic"),
            ],
            "right.center_y": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, -0.38, "ease_out_cubic"),
                KeyFrame(1.35, -0.34),
                KeyFrame(1.80, 0.0, "ease_in_cubic"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.40, 0.15, "ease_out_cubic"),
                KeyFrame(1.35, 0.12),
                KeyFrame(1.80, 0.0, "ease_in_cubic"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.40, 0.24, "ease_out_cubic"),
                KeyFrame(1.35, 0.22),
                KeyFrame(1.80, 0.10, "ease_in_cubic"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.40, 0.77, "ease_out_cubic"),
                KeyFrame(1.35, 0.79),
                KeyFrame(1.80, 0.85, "ease_in_cubic"),
            ],
        },
    )


def clip_sleep_enter() -> Clip:
    """Gradual close over 2.5s with drooping outer corners."""
    return Clip(
        id="sleep_enter",
        duration=2.5,
        priority=15,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.80, 0.35, "ease_in_out_sine"),
                KeyFrame(1.40, 0.55, "ease_in_out_sine"),
                KeyFrame(2.00, 0.78, "ease_in_out_sine"),
                KeyFrame(2.50, 0.88, "ease_in_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.80, 0.20, "ease_in_out_sine"),
                KeyFrame(1.40, 0.35, "ease_in_out_sine"),
                KeyFrame(2.00, 0.65, "ease_in_out_sine"),
                KeyFrame(2.50, 0.82, "ease_in_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.80, 0.75, "ease_in_out_sine"),
                KeyFrame(1.40, 0.65, "ease_in_out_sine"),
                KeyFrame(2.00, 0.55, "ease_in_out_sine"),
                KeyFrame(2.50, 0.40, "ease_in_sine"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(1.50, -0.05, "ease_in_out_sine"),
                KeyFrame(2.50, -0.10, "ease_in_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.05, 0.10),
                KeyFrame(0.85, 0.33, "ease_in_out_sine"),
                KeyFrame(1.45, 0.53, "ease_in_out_sine"),
                KeyFrame(2.05, 0.76, "ease_in_out_sine"),
                KeyFrame(2.50, 0.86, "ease_in_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.05, 0.05),
                KeyFrame(0.85, 0.18, "ease_in_out_sine"),
                KeyFrame(1.45, 0.33, "ease_in_out_sine"),
                KeyFrame(2.05, 0.63, "ease_in_out_sine"),
                KeyFrame(2.50, 0.80, "ease_in_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.05, 0.85),
                KeyFrame(0.85, 0.77, "ease_in_out_sine"),
                KeyFrame(1.45, 0.67, "ease_in_out_sine"),
                KeyFrame(2.05, 0.57, "ease_in_out_sine"),
                KeyFrame(2.50, 0.42, "ease_in_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.05, 0.0),
                KeyFrame(1.55, -0.03, "ease_in_out_sine"),
                KeyFrame(2.50, -0.08, "ease_in_sine"),
            ],
        },
    )


def clip_sleep_idle() -> Clip:
    """Looping breathing cycle while asleep. Subtle scale_y and cut oscillation."""
    return Clip(
        id="sleep_idle",
        duration=4.0,
        priority=2,
        interruptible=False,
        loop=True,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.40),
                KeyFrame(1.00, 0.46, "ease_in_out_sine"),
                KeyFrame(2.00, 0.40, "ease_in_out_sine"),
                KeyFrame(3.00, 0.46, "ease_in_out_sine"),
                KeyFrame(4.00, 0.40, "ease_in_out_sine"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.88),
                KeyFrame(1.00, 0.84, "ease_in_out_sine"),
                KeyFrame(2.00, 0.88, "ease_in_out_sine"),
                KeyFrame(3.00, 0.84, "ease_in_out_sine"),
                KeyFrame(4.00, 0.88, "ease_in_out_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.82),
                KeyFrame(1.00, 0.78, "ease_in_out_sine"),
                KeyFrame(2.00, 0.82, "ease_in_out_sine"),
                KeyFrame(3.00, 0.78, "ease_in_out_sine"),
                KeyFrame(4.00, 0.82, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.42),
                KeyFrame(1.00, 0.48, "ease_in_out_sine"),
                KeyFrame(2.00, 0.42, "ease_in_out_sine"),
                KeyFrame(3.00, 0.48, "ease_in_out_sine"),
                KeyFrame(4.00, 0.42, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.86),
                KeyFrame(1.00, 0.82, "ease_in_out_sine"),
                KeyFrame(2.00, 0.86, "ease_in_out_sine"),
                KeyFrame(3.00, 0.82, "ease_in_out_sine"),
                KeyFrame(4.00, 0.86, "ease_in_out_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.00, 0.80),
                KeyFrame(1.00, 0.76, "ease_in_out_sine"),
                KeyFrame(2.00, 0.80, "ease_in_out_sine"),
                KeyFrame(3.00, 0.76, "ease_in_out_sine"),
                KeyFrame(4.00, 0.80, "ease_in_out_sine"),
            ],
        },
    )


def clip_wake_enter() -> Clip:
    """Eyes gradually open from sleeping state."""
    return Clip(
        id="wake_enter",
        duration=1.0,
        priority=15,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.88),
                KeyFrame(0.50, 0.40, "ease_out_sine"),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.82),
                KeyFrame(0.50, 0.25, "ease_out_sine"),
                KeyFrame(1.00, 0.05, "ease_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.40),
                KeyFrame(0.50, 0.65, "ease_out_sine"),
                KeyFrame(1.00, 0.85, "ease_out_sine"),
            ],
            "left.outer_corner_raise": [
                KeyFrame(0.00, -0.10),
                KeyFrame(0.70, -0.03, "ease_out_sine"),
                KeyFrame(1.00, 0.0, "ease_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.86),
                KeyFrame(0.52, 0.38, "ease_out_sine"),
                KeyFrame(1.00, 0.10, "ease_out_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.00, 0.80),
                KeyFrame(0.52, 0.23, "ease_out_sine"),
                KeyFrame(1.00, 0.05, "ease_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.42),
                KeyFrame(0.52, 0.67, "ease_out_sine"),
                KeyFrame(1.00, 0.85, "ease_out_sine"),
            ],
            "right.outer_corner_raise": [
                KeyFrame(0.00, -0.08),
                KeyFrame(0.72, -0.02, "ease_out_sine"),
                KeyFrame(1.00, 0.0, "ease_out_sine"),
            ],
        },
    )


def clip_breathing() -> Clip:
    """Always-on subtle scale_y oscillation. Priority 1 so expressions override it."""
    return Clip(
        id="breathing",
        duration=3.5,
        priority=1,
        interruptible=False,
        loop=True,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.84),
                KeyFrame(0.88, 0.86, "ease_in_out_sine"),
                KeyFrame(1.75, 0.84, "ease_in_out_sine"),
                KeyFrame(2.63, 0.86, "ease_in_out_sine"),
                KeyFrame(3.50, 0.84, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.84),
                KeyFrame(0.90, 0.86, "ease_in_out_sine"),
                KeyFrame(1.80, 0.84, "ease_in_out_sine"),
                KeyFrame(2.70, 0.86, "ease_in_out_sine"),
                KeyFrame(3.50, 0.84, "ease_in_out_sine"),
            ],
        },
    )


def clip_slow_blink() -> Clip:
    """Heavier, lazier blink. Same pattern as blink but 2x slower."""
    return Clip(
        id="slow_blink",
        duration=0.7,
        priority=10,
        interruptible=False,
        loop=False,
        tracks={
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.20, 0.88, "ease_in_out_sine"),
                KeyFrame(0.30, 0.88),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "left.bottom_cut": [
                KeyFrame(0.00, 0.05),
                KeyFrame(0.20, 0.82, "ease_in_out_sine"),
                KeyFrame(0.30, 0.82),
                KeyFrame(0.70, 0.05, "ease_in_out_sine"),
            ],
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.72, "ease_in_out_sine"),
                KeyFrame(0.30, 0.72),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
            "right.top_cut": [
                KeyFrame(0.02, 0.10),
                KeyFrame(0.22, 0.86, "ease_in_out_sine"),
                KeyFrame(0.32, 0.86),
                KeyFrame(0.70, 0.10, "ease_in_out_sine"),
            ],
            "right.bottom_cut": [
                KeyFrame(0.02, 0.05),
                KeyFrame(0.22, 0.80, "ease_in_out_sine"),
                KeyFrame(0.32, 0.80),
                KeyFrame(0.70, 0.05, "ease_in_out_sine"),
            ],
            "right.scale_y": [
                KeyFrame(0.02, 0.85),
                KeyFrame(0.22, 0.74, "ease_in_out_sine"),
                KeyFrame(0.32, 0.74),
                KeyFrame(0.70, 0.85, "ease_in_out_sine"),
            ],
        },
    )


def clip_worried() -> Clip:
    """Slight widen, inner corners raised and tilted up, mild concern."""
    return Clip(
        id="worried",
        duration=1.2,
        priority=8,
        interruptible=True,
        loop=False,
        tracks={
            "left.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.20, 0.92, "ease_out_cubic"),
                KeyFrame(0.80, 0.90),
                KeyFrame(1.20, 0.85, "ease_in_cubic"),
            ],
            "left.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.20, 0.88, "ease_out_cubic"),
                KeyFrame(0.80, 0.90),
                KeyFrame(1.20, 0.95, "ease_in_cubic"),
            ],
            "left.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.20, 0.05, "ease_out_cubic"),
                KeyFrame(0.80, 0.06),
                KeyFrame(1.20, 0.10, "ease_in_cubic"),
            ],
            "left.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.25, "ease_out_cubic"),
                KeyFrame(0.80, 0.22),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "left.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 7.0, "ease_out_cubic"),
                KeyFrame(0.80, 6.0),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "left.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.25, 0.18, "ease_out_cubic"),
                KeyFrame(0.80, 0.15),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "right.scale_y": [
                KeyFrame(0.00, 0.85),
                KeyFrame(0.27, 0.90, "ease_out_cubic"),
                KeyFrame(0.87, 0.88),
                KeyFrame(1.20, 0.85, "ease_in_cubic"),
            ],
            "right.scale_x": [
                KeyFrame(0.00, 0.95),
                KeyFrame(0.27, 0.86, "ease_out_cubic"),
                KeyFrame(0.87, 0.88),
                KeyFrame(1.20, 0.95, "ease_in_cubic"),
            ],
            "right.top_cut": [
                KeyFrame(0.00, 0.10),
                KeyFrame(0.27, 0.06, "ease_out_cubic"),
                KeyFrame(0.87, 0.07),
                KeyFrame(1.20, 0.10, "ease_in_cubic"),
            ],
            "right.inner_corner_raise": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, 0.22, "ease_out_cubic"),
                KeyFrame(0.87, 0.20),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "right.rotation_deg": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, -7.0, "ease_out_cubic"),
                KeyFrame(0.87, -6.0),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
            "right.center_x": [
                KeyFrame(0.00, 0.0),
                KeyFrame(0.32, -0.18, "ease_out_cubic"),
                KeyFrame(0.87, -0.15),
                KeyFrame(1.20, 0.0, "ease_in_cubic"),
            ],
        },
    )


CLIP_FACTORIES = {
    "blink": clip_blink,
    "double_blink": clip_double_blink,
    "slow_blink": clip_slow_blink,
    "happy": clip_happy,
    "surprised": clip_surprised,
    "angry": clip_angry,
    "sad": clip_sad,
    "confused": clip_confused,
    "thinking": clip_thinking,
    "worried": clip_worried,
    "sleep_enter": clip_sleep_enter,
    "sleep_idle": clip_sleep_idle,
    "wake_enter": clip_wake_enter,
    "breathing": clip_breathing,
}