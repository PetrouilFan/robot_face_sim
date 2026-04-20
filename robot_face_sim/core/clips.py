from dataclasses import dataclass, field
from typing import Dict, List

from ..core.types import Clip
from ..core.shape_clips import CLIP_FACTORIES
from ..core.behavior_pools import ALL_CLIP_FACTORIES


@dataclass
class AnimationLibrary:
    clips: Dict[str, Clip] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, factory in CLIP_FACTORIES.items():
            self.clips[name] = factory()
        for name, factory in ALL_CLIP_FACTORIES.items():
            self.clips[name] = factory()

    def get(self, name: str) -> Clip:
        return self.clips[name]

    def all_names(self) -> List[str]:
        return list(self.clips.keys())
