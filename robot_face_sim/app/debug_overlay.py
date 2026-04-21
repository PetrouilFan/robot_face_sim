import pygame
from dataclasses import dataclass

from ..config import DebugConfig


HELP_SECTIONS = [
    ("Expressions", [
        ("B", "Blink"),
        ("N", "Double blink"),
        ("H", "Happy"),
        ("O", "Surprised"),
        ("A", "Angry"),
        ("J", "Sad"),
        ("C", "Confused"),
        ("X", "Thinking"),
    ]),
    ("Personality", [
        ("Y", "Yawn"),
        ("L", "Smile arc"),
        ("E", "Proud focus"),
        ("R", "Worried"),
        ("U", "Curious peek"),
        ("G", "Glitch split"),
        ("P", "Sleep peek"),
        ("F1", "Boot scan"),
    ]),
    ("Face Rig", [
        ("Q", "Whip look"),
        ("T", "Recoil bounce"),
        ("I", "Squash pop"),
        ("K", "Orbit search"),
        ("Z", "Panic ping-pong"),
        ("V", "Happy hop"),
        ("M", "Side freeze"),
    ]),
    ("States", [
        ("1", "IDLE"),
        ("2", "LISTENING"),
        ("3", "THINKING"),
        ("4", "SPEAKING"),
        ("5", "ANGRY"),
        ("6", "SAD"),
        ("7", "CONFUSED"),
        ("S", "Sleep toggle"),
    ]),
    ("System", [
        ("?", "Toggle this help"),
        ("D", "Toggle debug"),
        ("F", "Force full frame"),
        ("W", "Trigger wakeword"),
        (".", "Cycle warp (0→0.1→0.25→0.5→0.75→1.0→0)"),
        ("!", "Simulate loud noise"),
        ("ESC", "Quit"),
    ]),
]


@dataclass
class DebugOverlay:
    config: DebugConfig
    font: pygame.font.Font = None
    font_small: pygame.font.Font = None

    def __post_init__(self) -> None:
        try:
            self.font = pygame.font.SysFont("monospace", 12)
            self.font_small = pygame.font.SysFont("monospace", 10)
        except Exception:
            self.font = pygame.font.Font(None, 12)
            self.font_small = pygame.font.Font(None, 10)

    def draw(self, surface, simulator, metrics, delta, render_time) -> None:
        if not self.config.enabled:
            return

        # Debug metrics (top-left)
        y = 10
        color = (255, 255, 0)

        fps = 1.0 / delta if delta > 0 else 0.0
        lines = [
            f"FPS: {fps:.1f}",
            f"State: {simulator.state_machine.current_state.name}",
            f"Warp: {simulator.scheduler.base_state.rig.face_warp:.2f}",
            f"Frame time: {delta * 1000:.1f}ms",
            f"Render time: {render_time * 1000:.1f}ms",
            f"Dirty area: {metrics.dirty_area}px ({metrics.dirty_percent:.1f}%)",
            f"Transfer: {metrics.bytes_transferred} bytes",
            f"Transfer time: {metrics.estimated_transfer_us}us",
            f"Budget OK: {'Y' if metrics.frame_budget_ok else 'N'}",
        ]

        for line in lines:
            img = self.font_small.render(line, True, color)
            surface.blit(img, (10, y))
            y += 14

        # Help OSD (right side)
        if self.config.show_help:
            self._draw_help(surface)

    def _draw_help(self, surface) -> None:
        surface_w = surface.get_width()
        section_color = (180, 180, 255)
        key_color = (100, 255, 100)
        desc_color = (200, 200, 200)

        x = surface_w - 5
        y = 10

        for section_name, bindings in HELP_SECTIONS:
            # Measure section width to right-align
            max_width = 0
            rows = []
            for key, desc in bindings:
                row_text = f"[{key}] {desc}"
                img = self.font_small.render(row_text, True, desc_color)
                max_width = max(max_width, img.get_width())
                rows.append((key, desc, img))

            # Section header
            header_img = self.font_small.render(f"-- {section_name} --", True, section_color)
            header_w = header_img.get_width()
            header_x = surface_w - header_w - 5
            surface.blit(header_img, (header_x, y))
            y += 14

            # Bindings
            for key, desc, row_img in rows:
                rx = surface_w - row_img.get_width() - 10
                surface.blit(row_img, (rx, y))
                y += 13

            y += 6  # gap between sections