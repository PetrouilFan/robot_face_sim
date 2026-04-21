import math
import numpy as np
import pygame
from typing import Optional, Tuple

from ..core.types import FaceState, EyeParameters, Rect, DisplayMetrics
from ..core.dirty_rect import DirtyRectTracker
from ..config import DisplayConfig
from ..constants import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    BYTES_PER_PIXEL,
    DEFAULT_EYE_SEPARATION,
    DEFAULT_EYE_WIDTH,
    DEFAULT_EYE_HEIGHT,
    DEFAULT_EYE_Y,
    FACE_OFFSET_PX_PER_UNIT,
)


class PygameRenderer:
    def __init__(self, config: DisplayConfig):
        self.config = config
        self.width = config.width
        self.height = config.height
        self.scale = config.scale

        pygame.init()
        self.window = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale)
        )
        pygame.display.set_caption("Robot Face Simulator")
        pygame.time.delay(100)
        pygame.event.clear()

        self.framebuffer = pygame.Surface((self.width, self.height))
        self.dirty_tracker = DirtyRectTracker()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("monospace", 10)

        # Precompute barrel distortion coordinate grids
        cx = self.width / 2.0
        cy = self.height / 2.0
        max_r = math.sqrt(cx * cx + cy * cy)
        x_grid, y_grid = np.meshgrid(
            np.arange(self.width, dtype=np.float32),
            np.arange(self.height, dtype=np.float32),
            indexing='ij',
        )
        self._warp_dx = (x_grid - cx).astype(np.float32)
        self._warp_dy = (y_grid - cy).astype(np.float32)
        self._warp_norm_r = (np.sqrt(self._warp_dx**2 + self._warp_dy**2) / max_r).astype(np.float32)

    def render_eye(
        self,
        surface: pygame.Surface,
        eye: EyeParameters,
        cx: int,
        cy: int,
        base_width: int = DEFAULT_EYE_WIDTH,
        base_height: int = DEFAULT_EYE_HEIGHT,
    ) -> Rect:
        from .eye_shape import generate_eye_contour

        if not eye.visible:
            return Rect(cx - base_width // 2, cy - base_height // 2, 0, 0)

        points = generate_eye_contour(eye, base_width, base_height)
        hw = base_width // 2
        hh = base_height // 2
        offset_points = [(p[0] + cx - hw, p[1] + cy - hh) for p in points]

        brightness = int(200 * eye.brightness)
        pygame.draw.polygon(surface, (0, brightness, brightness), offset_points)

        xs = [p[0] for p in offset_points]
        ys = [p[1] for p in offset_points]

        return Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    def _apply_barrel_distortion(self, warp: float) -> None:
        """Apply barrel distortion to framebuffer. warp > 0 = bulge center (curved screen)."""
        cx = self.width / 2.0
        cy = self.height / 2.0

        # For each output pixel, the source is at a closer radius (center magnified, edges compressed)
        k = warp * 0.8
        factor = (1.0 - k * self._warp_norm_r ** 2).astype(np.float32)

        src_x = (cx + self._warp_dx * factor).astype(np.int32)
        src_y = (cy + self._warp_dy * factor).astype(np.int32)

        np.clip(src_x, 0, self.width - 1, out=src_x)
        np.clip(src_y, 0, self.height - 1, out=src_y)

        arr = pygame.surfarray.array3d(self.framebuffer)
        result = arr[src_x, src_y]
        pygame.surfarray.blit_array(self.framebuffer, result)

    def render(self, face: FaceState) -> Tuple[DisplayMetrics, float]:
        start_time = pygame.time.get_ticks()
        self.framebuffer.fill((0, 0, 0))

        rig = face.rig
        display_cx = self.width // 2
        display_cy = self.height // 2

        # Compute effective eye separation (gap + scale)
        separation = DEFAULT_EYE_SEPARATION * rig.eye_gap * rig.face_scale

        # Base eye center positions
        left_base_x = display_cx - separation / 2.0
        right_base_x = display_cx + separation / 2.0
        base_y = float(DEFAULT_EYE_Y)

        # Apply face offset (normalized units to pixels)
        offset_px = rig.face_offset_x * FACE_OFFSET_PX_PER_UNIT
        offset_py = rig.face_offset_y * FACE_OFFSET_PX_PER_UNIT
        left_cx = left_base_x + offset_px
        right_cx = right_base_x + offset_px
        cy = base_y + offset_py

        # Apply face tilt (rotate eye centers around display center)
        if rig.face_tilt != 0.0:
            tilt_rad = math.radians(rig.face_tilt)
            cos_t = math.cos(tilt_rad)
            sin_t = math.sin(tilt_rad)

            lx = left_cx - display_cx
            ly = cy - display_cy
            left_cx = display_cx + lx * cos_t - ly * sin_t
            left_cy = display_cy + lx * sin_t + ly * cos_t

            rx = right_cx - display_cx
            ry = cy - display_cy
            right_cx = display_cx + rx * cos_t - ry * sin_t
            right_cy = display_cy + rx * sin_t + ry * cos_t
        else:
            left_cy = cy
            right_cy = cy

        # Copy per-eye params and add face_tilt to rotation
        left_eye = EyeParameters(**face.left.__dict__)
        right_eye = EyeParameters(**face.right.__dict__)
        left_eye.rotation_deg += rig.face_tilt
        right_eye.rotation_deg += rig.face_tilt

        # Scale base dimensions
        scaled_w = round(DEFAULT_EYE_WIDTH * rig.face_scale)
        scaled_h = round(DEFAULT_EYE_HEIGHT * rig.face_scale)

        rect1 = self.render_eye(
            self.framebuffer, left_eye,
            int(left_cx), int(left_cy),
            scaled_w, scaled_h,
        )
        rect2 = self.render_eye(
            self.framebuffer, right_eye,
            int(right_cx), int(right_cy),
            scaled_w, scaled_h,
        )

        # Apply barrel distortion after rendering eyes
        if rig.face_warp != 0.0:
            self._apply_barrel_distortion(rig.face_warp)
            dirty_rects = [Rect(0, 0, self.width, self.height)]
        else:
            dirty_rects = self.dirty_tracker.update([rect1, rect2])

        if self.config.force_full_frame:
            dirty_rects = [Rect(0, 0, self.width, self.height)]

        dirty_area = sum(r.area for r in dirty_rects)
        dirty_percent = 100.0 * dirty_area / (self.width * self.height)
        bytes_transferred = dirty_area * BYTES_PER_PIXEL
        bytes_per_sec = self.config.spi_clock_hz // 8
        transfer_us = int((bytes_transferred / bytes_per_sec) * 1_000_000)
        frame_budget_ok = transfer_us < (1_000_000 // self.config.target_fps)

        metrics = DisplayMetrics(
            dirty_area=dirty_area,
            dirty_percent=dirty_percent,
            bytes_transferred=bytes_transferred,
            estimated_transfer_us=transfer_us,
            frame_budget_ok=frame_budget_ok,
        )

        pygame.transform.scale(self.framebuffer, self.window.get_size(), self.window)

        if self.config.show_dirty_rects:
            for r in dirty_rects:
                pygame.draw.rect(
                    self.window,
                    (255, 0, 0),
                    (
                        r.x * self.scale,
                        r.y * self.scale,
                        r.w * self.scale,
                        r.h * self.scale,
                    ),
                    1,
                )

        render_time = (pygame.time.get_ticks() - start_time) / 1000.0
        return metrics, render_time

    def flip(self) -> None:
        pygame.display.flip()

    def tick(self) -> float:
        return self.clock.tick(self.config.target_fps) / 1000.0

    def get_events(self):
        return pygame.event.get()