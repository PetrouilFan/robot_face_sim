import pygame
import time
import logging
from dataclasses import replace
from typing import Optional

from ..config import Config
from ..core import StateMachine, Scheduler, State, Event, EventType, FaceRigTransform, FaceState
from ..core.clips import AnimationLibrary
from ..core.idle_controller import IdleController
from ..render.pygame_renderer import PygameRenderer
from ..render.eye_shape import PRESETS
from ..audio.fake_audio import FakeAudioBackend
from ..wakeword.fake_detector import FakeWakeWordDetector
from .debug_overlay import DebugOverlay
from .controls import Controls


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Simulator:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.default()
        self.running = False

        # Core subsystems
        self.state_machine = StateMachine()
        self.scheduler = Scheduler()
        self.animations = AnimationLibrary()
        self.idle_controller = IdleController(self.scheduler)
        self.renderer = PygameRenderer(self.config.display)
        self.audio = FakeAudioBackend(self.config.audio)
        self.wakeword = FakeWakeWordDetector(self.config.wakeword)
        self.debug = DebugOverlay(self.config.debug)
        self.controls = Controls(self)

        # Set neutral base eye shape with subtle curved-screen warp
        neutral = PRESETS["neutral_soft"]
        self.scheduler.base_state = FaceState(
            left=replace(neutral),
            right=replace(neutral),
            rig=FaceRigTransform(face_warp=0.10),
        )

        self._setup_transitions()
        self._setup_global_rules()

        # Play boot sequence animation
        self.idle_controller.trigger_boot_sequence()

    def _setup_transitions(self) -> None:
        sched = self.scheduler
        anim = self.animations
        idle = self.idle_controller

        # Basic allowed state transitions
        self.state_machine.add_transition(State.BOOTING, State.IDLE)
        self.state_machine.add_transition(State.IDLE, State.LISTENING)
        self.state_machine.add_transition(State.IDLE, State.SLEEPING)
        self.state_machine.add_transition(State.SLEEPING, State.WAKING)
        self.state_machine.add_transition(State.WAKING, State.IDLE)
        self.state_machine.add_transition(State.LISTENING, State.THINKING)
        self.state_machine.add_transition(State.THINKING, State.SPEAKING)
        self.state_machine.add_transition(State.SPEAKING, State.IDLE)
        self.state_machine.add_transition(State.IDLE, State.HAPPY)
        self.state_machine.add_transition(State.IDLE, State.SAD)
        self.state_machine.add_transition(State.IDLE, State.CONFUSED)
        self.state_machine.add_transition(State.IDLE, State.ERROR)
        self.state_machine.add_transition(State.IDLE, State.ANGRY)
        self.state_machine.add_transition(State.ERROR, State.IDLE)
        self.state_machine.add_transition(State.HAPPY, State.IDLE)
        self.state_machine.add_transition(State.SAD, State.IDLE)
        self.state_machine.add_transition(State.CONFUSED, State.IDLE)
        self.state_machine.add_transition(State.ANGRY, State.IDLE)
        self.state_machine.add_transition(State.LISTENING, State.IDLE)
        self.state_machine.add_transition(State.THINKING, State.IDLE)
        self.state_machine.add_transition(State.SLEEPING, State.IDLE)

        # Expression transitions trigger animation clips
        self.state_machine.transition_handlers[(State.IDLE, State.HAPPY)] = lambda: sched.play(anim.get("happy"))
        self.state_machine.transition_handlers[(State.IDLE, State.SAD)] = lambda: sched.play(anim.get("sad"))
        self.state_machine.transition_handlers[(State.IDLE, State.CONFUSED)] = lambda: sched.play(anim.get("confused"))
        self.state_machine.transition_handlers[(State.IDLE, State.ANGRY)] = lambda: sched.play(anim.get("angry"))
        self.state_machine.transition_handlers[(State.LISTENING, State.THINKING)] = lambda: sched.play(anim.get("thinking"))
        self.state_machine.transition_handlers[(State.IDLE, State.ERROR)] = lambda: sched.play(anim.get("surprised"))

        # Sleep/wake transitions
        self.state_machine.transition_handlers[(State.IDLE, State.SLEEPING)] = lambda: (
            idle.notify_sleep_enter(),
            sched.play(anim.get("sleep_enter")),
        )
        self.state_machine.transition_handlers[(State.SLEEPING, State.WAKING)] = lambda: (
            idle.notify_wake(),
            sched.play(anim.get("wake_enter")),
        )
        self.state_machine.transition_handlers[(State.SLEEPING, State.IDLE)] = lambda: (
            idle.notify_wake(),
            sched.play(anim.get("wake_enter")),
        )

        # Return to idle: blink to reset the face
        for from_state in (State.HAPPY, State.SAD, State.CONFUSED, State.ANGRY, State.ERROR):
            self.state_machine.transition_handlers[(from_state, State.IDLE)] = lambda: sched.play(anim.get("blink"))

        self.state_machine.transition(State.IDLE)

    def _setup_global_rules(self) -> None:
        """Register event-driven state transition rules."""

        # Loud noise while sleeping → wake up
        def on_loud_noise_sleeping(state: State, event: Event) -> Optional[State]:
            if event.type == EventType.LOUD_NOISE_DETECTED and state == State.SLEEPING:
                return State.WAKING
            return None

        self.state_machine.global_rules.append(on_loud_noise_sleeping)

    def run(self) -> None:
        self.running = True
        logger.info("Simulator started")

        try:
            while self.running:
                dt = self.renderer.tick()

                # Handle input events
                events = self.renderer.get_events()
                for event in events:
                    if event.type == pygame.QUIT:
                        print("QUIT event received")
                        self.running = False
                        break
                    self.controls.handle_event(event)

                # Update subsystems
                self.wakeword.update()
                self.audio.update()

                # Process events
                for event in self.wakeword.pending_events():
                    self.state_machine.handle_event(event)

                # Process audio events and handle loud noise
                for event in self.audio.pending_events():
                    handled = self.state_machine.handle_event(event)
                    if event.type == EventType.LOUD_NOISE_DETECTED:
                        self.idle_controller.handle_loud_noise(
                            time.time(), self.state_machine.current_state
                        )

                # Update idle controller and scheduler
                current_time = time.time()
                self.idle_controller.update(current_time, self.state_machine.current_state)
                face_state = self.scheduler.update(current_time)

                # Render frame
                metrics, render_time = self.renderer.render(face_state)

                # Draw debug overlay
                self.debug.draw(self.renderer.window, self, metrics, dt, render_time)

                self.renderer.flip()
        except Exception as e:
            logger.exception("Exception in main loop")
            raise
        finally:
            pygame.quit()
            logger.info("Simulator stopped")


def main():
    sim = Simulator()
    sim.run()


if __name__ == "__main__":
    main()
