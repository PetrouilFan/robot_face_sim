# Robot Face Simulator

ESP32-S3 Robot Face Reference Implementation

This is a Python-first simulator and architecture prototype for an ESP32-S3 based robot face device with expressive eye animations, audio, and wake-word detection.

This codebase is the **reference implementation** for behavior and architecture, designed from day one to be ported cleanly to Arduino/C++ on real hardware.

## Architecture

### Core Design Principles
1.  **Portable First**: All core logic is written exactly as it will run on ESP32-S3
2.  **Clean Layers**: Strict separation between pure logic and platform adapters
3.  **Hardware Realism**: Simulates actual display bandwidth, SPI constraints, and update patterns
4.  **Parametric Animation**: No pre-rendered bitmaps, everything is procedural
5.  **Minimal Dependencies**: Only pygame, numpy, sounddevice

### Layers
| Module | Purpose | Port Status |
|--------|---------|-------------|
| `core/` | Pure logic, state machines, animation engine, eye model | 100% portable to C++ |
| `render/` | Pygame display simulator with ST7789 SPI constraints | Platform adapter |
| `audio/` | Audio interfaces with fake and real backends | Maps directly to I2S DMA tasks |
| `wakeword/` | Wake word detector abstraction | Maps directly to ESP-SR / microWakeWord |
| `app/` | Desktop simulator runtime | Desktop only |

## Hardware Target
- ESP32-S3 microcontroller
- 1.54" 240x240 ST7789 IPS LCD over SPI
- INMP441 I2S microphone
- MAX98357A I2S audio amplifier

## Running the Simulator

```bash
# Install dependencies
uv sync

# Run
uv run python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `b` | Soft blink |
| `h` | Happy expression |
| `s` | Sleep close |
| `o` | Surprised open |
| `d` | Toggle debug overlay |
| `f` | Toggle full frame/dirty-rect |
| `ESC` | Exit |

## Display Realism Simulation

This simulator accurately models:
- Exact 240x240 pixel framebuffer
- Dirty rectangle tracking and partial updates
- SPI transfer bandwidth and timing calculations
- RGB565 pixel format constraints
- Frame budget estimation for real hardware

Metrics shown in debug overlay:
- Dirty area in pixels and percentage
- Estimated bytes transferred over SPI
- Estimated transfer time in microseconds
- Frame budget status indicator

## Porting Notes

### ESP32-S3 Arduino Port Plan
1.  Copy **entire `core/` module verbatim** - this is pure portable logic
2.  Replace pygame renderer with LovyanGFX implementation
3.  Replace audio backend with ESP32 I2S driver
4.  Replace wake word detector with ESP-SR / microWakeWord
5.  Replace main loop with FreeRTOS tasks

All timing models, state machines, animation clips, and eye parameters will work exactly the same on hardware.

## Status

| Feature | Status |
|---------|--------|
| Core types and interfaces | Done |
| State machine implementation | Done |
| Timeline and clip engine | Done |
| Expression clips | Done |
| Behavior pool system | Done |
| IdleController with autonomous behaviors | Done |
| Easing function library | Done |
| Face rig transform layer | Done |
| Barrel distortion (curved-screen) | Done |
| Pygame renderer | Done |
| Dirty rectangle tracking | Done |
| Procedural eye contour generation | Done |
| Eye shaping parameters | Done |
| Audio interface and fake backend | Done |
| Wake word interface and fake backend | Done |
| Debug overlay | Done |
| Performance metrics | Done |

## Implemented Features

- Complete expression clip library (blink, double_blink, slow_blink, happy, surprised, angry, sad, confused, thinking, worried, sleep/wake cycles)
- Behavior pool system with 3-tier scheduling (common micro-idles, occasional personality beats, rare "wow" moments)
- IdleController for autonomous idle behaviors, auto-blinks, micro-pose shifts, and sleep state management
- Easing function library (sine, cubic, elastic, back, bounce curves)
- Face rig transforms (offset, tilt, scale, eye_gap)
- Barrel distortion (face_warp) for curved-screen effect
- Procedural eye contour generation with presets
- Eye shaping parameters (top_cut, bottom_cut, corner raises, rotation, scale_x/y)
