from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import bisect

from .easing import interpolate
from .types import KeyFrame


@dataclass
class Timeline:
    tracks: Dict[str, List[KeyFrame]] = field(default_factory=dict)
    duration: float = 0.0

    def add_track(self, name: str, keyframes: List[KeyFrame]) -> None:
        keyframes.sort(key=lambda kf: kf.time)
        self.tracks[name] = keyframes
        self.duration = max(self.duration, max(kf.time for kf in keyframes))

    def evaluate(self, time: float) -> Dict[str, float]:
        result = {}
        for name, kfs in self.tracks.items():
            result[name] = self._evaluate_track(kfs, time)
        return result

    def _evaluate_track(self, kfs: List[KeyFrame], t: float) -> float:
        if not kfs:
            return 0.0

        if t <= kfs[0].time:
            return kfs[0].value

        if t >= kfs[-1].time:
            return kfs[-1].value

        idx = bisect.bisect_left(kfs, t, key=lambda x: x.time)
        k0 = kfs[idx - 1]
        k1 = kfs[idx]

        dt = k1.time - k0.time
        if dt == 0:
            return k1.value

        factor = (t - k0.time) / dt
        return interpolate(k0.value, k1.value, factor, k1.easing)
