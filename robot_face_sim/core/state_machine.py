from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Set
import time

from .types import State, Event, EventType


TransitionRule = Callable[[State, Event], Optional[State]]


@dataclass
class StateMachine:
    current_state: State = State.BOOTING
    last_transition_time: float = field(default_factory=time.time)
    allowed_transitions: Dict[State, Set[State]] = field(default_factory=dict)
    transition_handlers: Dict[tuple[State, State], Callable[[], None]] = field(
        default_factory=dict
    )
    global_rules: list[TransitionRule] = field(default_factory=list)

    def add_transition(self, from_state: State, to_state: State) -> None:
        if from_state not in self.allowed_transitions:
            self.allowed_transitions[from_state] = set()
        self.allowed_transitions[from_state].add(to_state)

    def can_transition(self, to_state: State) -> bool:
        return to_state in self.allowed_transitions.get(self.current_state, set())

    def transition(self, to_state: State) -> bool:
        if not self.can_transition(to_state):
            return False

        handler_key = (self.current_state, to_state)
        if handler_key in self.transition_handlers:
            self.transition_handlers[handler_key]()

        self.current_state = to_state
        self.last_transition_time = time.time()
        return True

    def handle_event(self, event: Event) -> bool:
        for rule in self.global_rules:
            target = rule(self.current_state, event)
            if target is not None and self.can_transition(target):
                return self.transition(target)
        return False

    def time_in_state(self) -> float:
        return time.time() - self.last_transition_time
