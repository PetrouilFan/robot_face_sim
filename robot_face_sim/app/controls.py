import pygame
from dataclasses import dataclass

from ..core import State


@dataclass
class Controls:
    simulator: "Simulator"

    def handle_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.simulator.running = False

            # Expression clips (direct play)
            elif event.key == pygame.K_b:
                self.simulator.scheduler.play(self.simulator.animations.get("blink"))
            elif event.key == pygame.K_n:
                self.simulator.scheduler.play(self.simulator.animations.get("double_blink"))
            elif event.key == pygame.K_h:
                self.simulator.scheduler.play(self.simulator.animations.get("happy"))
            elif event.key == pygame.K_o:
                self.simulator.scheduler.play(self.simulator.animations.get("surprised"))
            elif event.key == pygame.K_a:
                self.simulator.scheduler.play(self.simulator.animations.get("angry"))
            elif event.key == pygame.K_j:
                self.simulator.scheduler.play(self.simulator.animations.get("sad"))
            elif event.key == pygame.K_c:
                self.simulator.scheduler.play(self.simulator.animations.get("confused"))
            elif event.key == pygame.K_x:
                self.simulator.scheduler.play(self.simulator.animations.get("thinking"))
            # New personality clips
            elif event.key == pygame.K_y:
                self.simulator.scheduler.play(self.simulator.animations.get("yawn"))
            elif event.key == pygame.K_l:
                self.simulator.scheduler.play(self.simulator.animations.get("tiny_smile_arc"))
            elif event.key == pygame.K_e:
                self.simulator.scheduler.play(self.simulator.animations.get("proud_focus"))
            elif event.key == pygame.K_r:
                self.simulator.scheduler.play(self.simulator.animations.get("worried"))
            elif event.key == pygame.K_u:
                self.simulator.scheduler.play(self.simulator.animations.get("curious_peek"))
            # Rare / wow clips
            elif event.key == pygame.K_g:
                self.simulator.scheduler.play(self.simulator.animations.get("glitch_split"))
            elif event.key == pygame.K_p:
                self.simulator.scheduler.play(self.simulator.animations.get("sleep_peek"))
            elif event.key == pygame.K_q:
                self.simulator.scheduler.play(self.simulator.animations.get("whip_look"))
            elif event.key == pygame.K_t:
                self.simulator.scheduler.play(self.simulator.animations.get("recoil_bounce"))
            elif event.key == pygame.K_i:
                self.simulator.scheduler.play(self.simulator.animations.get("squash_pop"))
            elif event.key == pygame.K_k:
                self.simulator.scheduler.play(self.simulator.animations.get("orbit_search"))
            elif event.key == pygame.K_z:
                self.simulator.scheduler.play(self.simulator.animations.get("panic_pingpong"))
            elif event.key == pygame.K_v:
                self.simulator.scheduler.play(self.simulator.animations.get("happy_hop"))
            elif event.key == pygame.K_m:
                self.simulator.scheduler.play(self.simulator.animations.get("dramatic_side_freeze"))
            elif event.key == pygame.K_F1:
                self.simulator.scheduler.play(self.simulator.animations.get("boot_scan"))

            # Simulate loud noise
            elif event.key == pygame.K_EXCLAIM or event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.simulator.idle_controller.handle_loud_noise(
                    __import__("time").time(),
                    self.simulator.state_machine.current_state,
                )

            # State transitions
            elif event.key == pygame.K_1:
                self.simulator.state_machine.transition(State.IDLE)
            elif event.key == pygame.K_2:
                self.simulator.state_machine.transition(State.LISTENING)
            elif event.key == pygame.K_3:
                self.simulator.state_machine.transition(State.THINKING)
            elif event.key == pygame.K_4:
                self.simulator.state_machine.transition(State.SPEAKING)
            elif event.key == pygame.K_5:
                self.simulator.state_machine.transition(State.ANGRY)
            elif event.key == pygame.K_6:
                self.simulator.state_machine.transition(State.SAD)
            elif event.key == pygame.K_7:
                self.simulator.state_machine.transition(State.CONFUSED)
            elif event.key == pygame.K_s:
                if self.simulator.state_machine.current_state == State.SLEEPING:
                    self.simulator.state_machine.transition(State.IDLE)
                else:
                    self.simulator.state_machine.transition(State.SLEEPING)

            # System toggles
            elif event.key == pygame.K_w:
                self.simulator.wakeword.trigger()
            elif event.key == pygame.K_d:
                self.simulator.debug.config.enabled = (
                    not self.simulator.debug.config.enabled
                )
            elif event.key == pygame.K_f:
                self.simulator.renderer.config.force_full_frame = (
                    not self.simulator.renderer.config.force_full_frame
                )
            elif event.key == pygame.K_PERIOD:
                # Toggle warp: 0.0 -> 0.10 -> 0.20 -> 0.0
                current = self.simulator.scheduler.base_state.rig.face_warp
                if current < 0.01:
                    self.simulator.scheduler.base_state.rig.face_warp = 0.10
                elif current < 0.15:
                    self.simulator.scheduler.base_state.rig.face_warp = 0.20
                else:
                    self.simulator.scheduler.base_state.rig.face_warp = 0.0
            elif event.key == pygame.K_SLASH or event.key == pygame.K_QUESTION:
                self.simulator.debug.config.show_help = (
                    not self.simulator.debug.config.show_help
                )