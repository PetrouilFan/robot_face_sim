from dataclasses import dataclass, field
from typing import Optional, List
import time

from .types import Clip, EyeParameters, FaceRigTransform, FaceState
from .timeline import Timeline


@dataclass
class ActiveClip:
    clip: Clip
    timeline: Timeline
    start_time: float
    paused: bool = False


@dataclass
class Scheduler:
    base_state: FaceState = field(
        default_factory=lambda: FaceState(left=EyeParameters(), right=EyeParameters())
    )
    active_clips: List[ActiveClip] = field(default_factory=list)

    def play(self, clip: Clip) -> None:
        # Stop lower priority clips
        self.active_clips = [
            ac
            for ac in self.active_clips
            if not ac.clip.interruptible or ac.clip.priority >= clip.priority
        ]

        timeline = Timeline()
        if clip.tracks:
            for track_name, kfs in clip.tracks.items():
                timeline.add_track(track_name, kfs)

        self.active_clips.append(
            ActiveClip(clip=clip, timeline=timeline, start_time=time.time())
        )

    def update(self, current_time: Optional[float] = None) -> FaceState:
        t = current_time if current_time is not None else time.time()
        state = FaceState(
            left=EyeParameters(**self.base_state.left.__dict__),
            right=EyeParameters(**self.base_state.right.__dict__),
            rig=FaceRigTransform(**self.base_state.rig.__dict__),
        )

        # Sort clips by priority ascending
        sorted_clips = sorted(self.active_clips, key=lambda ac: ac.clip.priority)

        # Remove completed clips
        self.active_clips = [
            ac
            for ac in sorted_clips
            if ac.clip.loop or (t - ac.start_time) < ac.clip.duration
        ]

        # Apply clips in priority order
        for active in self.active_clips:
            clip_time = t - active.start_time
            if active.clip.loop:
                clip_time %= active.clip.duration

            values = active.timeline.evaluate(clip_time)
            self._apply_values(state, values)

        return state

    def _apply_values(self, state: FaceState, values: dict) -> None:
        for key, value in values.items():
            if key.startswith("left."):
                attr = key[5:]
                if hasattr(state.left, attr):
                    setattr(state.left, attr, value)
            elif key.startswith("right."):
                attr = key[6:]
                if hasattr(state.right, attr):
                    setattr(state.right, attr, value)
            elif key.startswith("face."):
                attr = key[5:]
                if hasattr(state.rig, attr):
                    setattr(state.rig, attr, value)
            elif key == "brightness":
                state.overall_brightness = value
