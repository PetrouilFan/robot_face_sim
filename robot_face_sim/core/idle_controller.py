import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .types import Clip, KeyFrame, State
from .scheduler import Scheduler
from .behavior_pools import BehaviorDef, build_state_pools, clip_startled_wake, clip_flinch


# Tier timing intervals (seconds)
TIER_INTERVALS = {
    "common": (1.8, 4.5),
    "occasional": (8.0, 35.0),
    "rare": (45.0, 240.0),
}

# State-specific interval multipliers for common tier
STATE_COMMON_MODIFIERS = {
    State.IDLE: 1.0,
    State.LISTENING: 0.5,  # faster micro-idles when attentive
    State.THINKING: 1.4,   # slower when focused
    State.SPEAKING: 1.5,
    State.HAPPY: 1.0,
    State.SAD: 1.2,
    State.CONFUSED: 1.0,
    State.ANGRY: 1.0,
    State.ERROR: 1.0,
    State.WAKING: 0.8,
    State.SLEEPING: 0.0,   # no common behaviors in sleep
    State.BOOTING: 0.0,
}


@dataclass
class IdleController:
    scheduler: Scheduler
    # Per-clip cooldown tracking: clip_id -> last play time
    _cooldowns: Dict[str, float] = field(default_factory=dict)
    # Per-tier next trigger times
    _next_common: float = 0.0
    _next_occasional: float = 0.0
    _next_rare: float = 0.0
    # Pre-built state pools
    _pools: Dict[State, Dict[str, List[BehaviorDef]]] = field(default_factory=build_state_pools)
    # Track active looping clips
    _breathing_active: bool = False
    _sleep_idle_active: bool = False
    _dream_flutter_active: bool = False
    # Last state for detecting transitions
    _last_state: State = State.BOOTING

    def __post_init__(self) -> None:
        now = time.time()
        self._next_common = now + random.uniform(1.5, 3.0)
        self._next_occasional = now + random.uniform(8.0, 20.0)
        self._next_rare = now + random.uniform(45.0, 120.0)

    def update(self, current_time: float, current_state: State) -> None:
        # Detect state transitions
        if current_state != self._last_state:
            self._on_state_change(current_state, current_time)
            self._last_state = current_state

        self._ensure_breathing(current_state)
        self._check_common(current_time, current_state)
        self._check_occasional(current_time, current_state)
        self._check_rare(current_time, current_state)
        self._check_blink(current_time, current_state)
        self._check_micro_pose_shift(current_time, current_state)
        self._manage_sleep(current_state)

    def handle_loud_noise(self, current_time: float, current_state: State) -> None:
        """Called when a loud noise is detected. Routes to appropriate response."""
        if current_state == State.SLEEPING:
            # Startled wake
            self._stop_sleep_idle()
            self._sleep_idle_active = False
            self._stop_dream_flutter()
            self.scheduler.play(clip_startled_wake())
            # Transition will be handled by state machine global rules
        elif current_state not in (State.BOOTING,):
            # Flinch
            self.scheduler.play(clip_flinch())

    def trigger_boot_sequence(self) -> None:
        """Play boot scan animation. Call once at startup."""
        from .behavior_pools import clip_boot_scan
        self.scheduler.play(clip_boot_scan())

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _on_state_change(self, new_state: State, current_time: float) -> None:
        """Reset timing when state changes to avoid stale behaviors."""
        # Reset common tier to trigger soon in new state
        self._next_common = current_time + random.uniform(1.0, 2.5)

    def _ensure_breathing(self, state: State) -> None:
        if not self._breathing_active and state != State.SLEEPING:
            from .shape_clips import clip_breathing
            self.scheduler.play(clip_breathing())
            self._breathing_active = True

    def _check_blink(self, current_time: float, state: State) -> None:
        """Auto-blink with varying speed based on state."""
        if not hasattr(self, '_next_blink_time'):
            self._next_blink_time = current_time + random.uniform(2.0, 4.0)

        if state == State.SLEEPING:
            return
        if current_time < self._next_blink_time:
            return

        from .shape_clips import clip_blink, clip_double_blink, clip_slow_blink

        # 10% chance of slow blink, 12% double blink, rest normal
        roll = random.random()
        if roll < 0.10:
            self.scheduler.play(clip_slow_blink())
        elif roll < 0.22:
            self.scheduler.play(clip_double_blink())
        else:
            self.scheduler.play(clip_blink())

        # Blink interval varies by state
        if state == State.LISTENING:
            interval = random.uniform(1.5, 3.0)
        elif state == State.THINKING:
            interval = random.uniform(3.0, 6.0)
        else:
            interval = random.uniform(2.5, 5.0)
        self._next_blink_time = current_time + interval

    def _check_micro_pose_shift(self, current_time: float, state: State) -> None:
        """Tiny random center_x/y shifts. Renamed from 'saccade' since no pupils."""
        if not hasattr(self, '_next_pose_time'):
            self._next_pose_time = current_time + random.uniform(0.5, 2.0)

        if state in (State.SLEEPING, State.BOOTING):
            return
        if current_time < self._next_pose_time:
            return

        dx_l = random.uniform(-0.10, 0.10)
        dy_l = random.uniform(-0.10, 0.10)
        dx_r = dx_l * 0.85 + random.uniform(-0.02, 0.02)
        dy_r = dy_l * 0.85 + random.uniform(-0.02, 0.02)

        clip = Clip(
            id="micro_pose_shift",
            duration=0.35,
            priority=3,
            interruptible=True,
            loop=False,
            tracks={
                "left.center_x": [
                    KeyFrame(0.00, 0.0), KeyFrame(0.08, dx_l, "ease_out_sine"),
                    KeyFrame(0.25, dx_l), KeyFrame(0.35, 0.0, "ease_in_sine"),
                ],
                "left.center_y": [
                    KeyFrame(0.00, 0.0), KeyFrame(0.08, dy_l, "ease_out_sine"),
                    KeyFrame(0.25, dy_l), KeyFrame(0.35, 0.0, "ease_in_sine"),
                ],
                "right.center_x": [
                    KeyFrame(0.00, 0.0), KeyFrame(0.10, dx_r, "ease_out_sine"),
                    KeyFrame(0.27, dx_r), KeyFrame(0.35, 0.0, "ease_in_sine"),
                ],
                "right.center_y": [
                    KeyFrame(0.00, 0.0), KeyFrame(0.10, dy_r, "ease_out_sine"),
                    KeyFrame(0.27, dy_r), KeyFrame(0.35, 0.0, "ease_in_sine"),
                ],
            },
        )
        self.scheduler.play(clip)

        if state == State.LISTENING:
            interval = random.uniform(0.3, 1.0)
        elif state == State.THINKING:
            interval = random.uniform(1.0, 3.0)
        else:
            interval = random.uniform(0.5, 2.0)
        self._next_pose_time = current_time + interval

    def _check_common(self, current_time: float, state: State) -> None:
        if current_time < self._next_common:
            return
        self._pick_and_play(current_time, state, "common")
        lo, hi = TIER_INTERVALS["common"]
        mult = STATE_COMMON_MODIFIERS.get(state, 1.0)
        self._next_common = current_time + random.uniform(lo, hi) * mult

    def _check_occasional(self, current_time: float, state: State) -> None:
        if current_time < self._next_occasional:
            return
        self._pick_and_play(current_time, state, "occasional")
        lo, hi = TIER_INTERVALS["occasional"]
        self._next_occasional = current_time + random.uniform(lo, hi)

    def _check_rare(self, current_time: float, state: State) -> None:
        if current_time < self._next_rare:
            return
        self._pick_and_play(current_time, state, "rare")
        lo, hi = TIER_INTERVALS["rare"]
        self._next_rare = current_time + random.uniform(lo, hi)

    def _pick_and_play(self, current_time: float, state: State, tier: str) -> None:
        """Pick a weighted random behavior from the state's pool for this tier."""
        pool = self._pools.get(state, {}).get(tier, [])
        if not pool:
            return

        # Filter out behaviors on cooldown
        available = []
        for bdef in pool:
            last_played = self._cooldowns.get(bdef.name, 0.0)
            if current_time - last_played >= bdef.cooldown:
                available.append(bdef)

        if not available:
            return

        # Weighted random selection
        total_weight = sum(b.weight for b in available)
        roll = random.uniform(0, total_weight)
        cumulative = 0.0
        chosen = available[0]
        for bdef in available:
            cumulative += bdef.weight
            if roll <= cumulative:
                chosen = bdef
                break

        # Play the clip and record cooldown
        clip = chosen.clip_factory()
        self.scheduler.play(clip)
        self._cooldowns[chosen.name] = current_time

    def _manage_sleep(self, state: State) -> None:
        if state == State.SLEEPING and not self._sleep_idle_active:
            self._start_sleep()
        elif state != State.SLEEPING and self._sleep_idle_active:
            self._stop_sleep()

    def _start_sleep(self) -> None:
        from .shape_clips import clip_sleep_idle
        from .behavior_pools import clip_dream_flutter

        # Stop breathing, start sleep idle
        self.scheduler.active_clips = [
            ac for ac in self.scheduler.active_clips if ac.clip.id != "breathing"
        ]
        self._breathing_active = False
        self.scheduler.play(clip_sleep_idle())
        self._sleep_idle_active = True

        # Start dream flutter after a short delay
        self.scheduler.play(clip_dream_flutter())
        self._dream_flutter_active = True

    def _stop_sleep(self) -> None:
        self._stop_sleep_idle()
        self._stop_dream_flutter()
        self._sleep_idle_active = False
        self._dream_flutter_active = False

    def _stop_sleep_idle(self) -> None:
        self.scheduler.active_clips = [
            ac for ac in self.scheduler.active_clips if ac.clip.id != "sleep_idle"
        ]

    def _stop_dream_flutter(self) -> None:
        self.scheduler.active_clips = [
            ac for ac in self.scheduler.active_clips if ac.clip.id != "dream_flutter"
        ]

    def notify_sleep_enter(self) -> None:
        """Called when transitioning to SLEEPING state."""
        # Handled by _manage_sleep on next update
        pass

    def notify_wake(self) -> None:
        """Called when transitioning out of SLEEPING state."""
        self._stop_sleep_idle()
        self._stop_dream_flutter()
        self._sleep_idle_active = False
        self._dream_flutter_active = False