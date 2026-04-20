from typing import List, Optional
from ..core.types import Rect


class DirtyRectTracker:
    def __init__(self):
        self.previous_rects: List[Rect] = []

    def update(self, current_rects: List[Rect]) -> List[Rect]:
        dirty: List[Rect] = []

        # Add all current rects
        for r in current_rects:
            dirty.append(r)

        # Add previous rects to clear old areas
        for r in self.previous_rects:
            dirty.append(r)

        self.previous_rects = current_rects.copy()

        if not dirty:
            return []

        # Merge overlapping rects
        merged = self._merge_rects(dirty)
        return merged

    def _merge_rects(self, rects: List[Rect]) -> List[Rect]:
        if len(rects) <= 1:
            return rects

        # Sort by x then y
        sorted_rects = sorted(rects, key=lambda r: (r.x, r.y))
        merged: List[Rect] = [sorted_rects[0]]

        for current in sorted_rects[1:]:
            last = merged[-1]

            # Check if rects overlap or touch
            if (
                current.x <= last.x + last.w
                and current.y <= last.y + last.h
                and current.x + current.w >= last.x
                and current.y + current.h >= last.y
            ):
                # Merge them
                new_x = min(last.x, current.x)
                new_y = min(last.y, current.y)
                new_w = max(last.x + last.w, current.x + current.w) - new_x
                new_h = max(last.y + last.h, current.y + current.h) - new_y
                merged[-1] = Rect(new_x, new_y, new_w, new_h)
            else:
                merged.append(current)

        return merged

    def reset(self) -> None:
        self.previous_rects = []
