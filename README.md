# Robot Face Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Python-first simulator and reference implementation for an ESP32-S3 based robot face device featuring expressive eye animations, audio processing, and wake-word detection.

This codebase is designed from the ground up to be cleanly ported to Arduino/C++ on real hardware.

## Table of Contents
- [Architecture](#architecture)
- [Hardware Target](#hardware-target)
- [Quick Start](#quick-start)
- [Controls](#controls)
- [Features](#features)
- [Display Realism](#display-realism)

## Architecture

### Core Design Principles
1. **Portable First**: All core logic is written exactly as it will run on ESP32-S3
2. **Clean Layers**: Strict separation between pure logic and platform adapters
3. **Hardware Realism**: Simulates actual display bandwidth, SPI constraints, and update patterns
4. **Parametric Animation**: No pre-rendered bitmaps, everything is procedural
5. **Minimal Dependencies**: Only pygame, numpy, sounddevice

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

## Quick Start

```bash
# Clone the repository
git clone https://github.com/PetrouilFan/robot_face_sim.git
cd robot_face_sim

# Install dependencies
uv sync

# Run the simulator
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

## Features

- **Expression System**: Complete clip library (blink, double blink, slow blink, happy, surprised, angry, sad, confused, thinking, worried, sleep/wake cycles)
- **Autonomous Behaviors**: 3-tier behavior pool system (common micro-idles, occasional personality beats, rare moments) with weighted random selection
- **Idle Controller**: Manages auto-blinks, micro-pose shifts, and sleep state transitions
- **Easing Library**: Rich set of easing functions (sine, cubic, elastic, back, bounce)
- **Face Rig Transforms**: Offset, tilt, scale, and eye gap transformations
- **Barrel Distortion**: Curved-screen effect via configurable warp parameter
- **Procedural Eye Rendering**: Dynamic contour generation with shape presets and parameters (top/bottom cut, corner raises, rotation, scale)
- **Performance Metrics**: Dirty rectangle tracking, SPI transfer estimation, frame budget analysis

## Display Realism

This simulator accurately models:
- Exact 240x240 pixel framebuffer
- Dirty rectangle tracking and partial updates
- SPI transfer bandwidth and timing calculations
- RGB565 pixel format constraints
- Frame budget estimation for real hardware

Metrics shown in debug overlay (`d` key):
- Dirty area in pixels and percentage
- Estimated bytes transferred over SPI
- Estimated transfer time in microseconds
- Frame budget status indicator
