# Superfortress

An experiment in a Supernote-sideloadable sim game. The goal, in order:

1. Prove a Python app can be built and sideloaded onto a Supernote A5X.
2. Build a tiny Dwarf-Fortress-flavored simulation: a world that keeps
   changing over time (right now: a worker who autonomously harvests
   trees into wood) rendered on a simple grid map.

## Status: v0.1 — smallest useful slice

- `sim.py` — the simulation itself (world grid, resources, one worker).
  No Kivy/graphics dependency, so it can be run and sanity-checked on its
  own: `python sim.py`.
- `main.py` — Kivy app that renders the grid and drives the sim on a
  timer. Redraws are event-driven (only on state change) and capped to a
  low frame rate, since this needs to eventually behave on an e-ink
  screen rather than fight it.
- `buildozer.spec` / `requirements.txt` — Android packaging config.
- `SIDELOADING.md` — how to build the APK and get it installed on the
  device.

## Quick local check (no device needed)

```bash
pip install kivy
python main.py
```

You should see a grid map with a white dot (the worker) wandering to the
nearest tree, harvesting it, and the wood counter in the top bar
increasing every ~1.5 seconds. Pause/Resume toggles the simulation.

## Next steps

- Build the APK and confirm it installs/launches on the actual A5X
  (see `SIDELOADING.md`).
- Once sideloading is confirmed working, expand the simulation: more
  resource types, more workers, simple building/designation mechanics.
