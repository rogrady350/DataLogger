<!-- Copilot / AI agent instructions for the DataLogger (RaceDash) project -->

# Quick Intent

This repository implements a small Pygame-based dashboard (RaceDash). These notes give an AI coding agent the minimal, concrete knowledge needed to be productive: the big-picture architecture, how to run the app locally, project-specific patterns, and a short list of discoverable TODOs to avoid wasted work.

**Big Picture**
- **App type**: Single-process Pygame desktop app started from `main.py`.
- **Responsibilities**: `main.py` boots Pygame, creates the window and the main loop. The `ui` package handles all drawing. `sensors` is the place for hardware/reader implementations and `logging` is intended for data persistence.
- **Data flow**: sensor readers should produce numeric values which are passed to UI draw code (gauges) each frame; `ScreenManager` orchestrates frame drawing at ~30 FPS.

**Key Files / Directories**
- `main.py`: program entrypoint and main loop. Keep Pygame init/quit logic here.
- `ui/screen_manager.py`: central UI orchestrator — create fonts here and reuse across frames.
- `ui/gauges.py`: layout helpers and gauge drawing functions. Layout helpers return `pygame.Rect` instances for gauge placement.
- `sensors/`: sensor driver implementations (e.g., `ads_reader.py`, `mock_reader.py`).
- `logging/`: logger/datalogger stubs (`datalogger.py`).
- `requirements.txt`: dependency pinning (`pygame==2.6.1`).

**How to Run (developer steps)**
- Install dependencies: `python -m pip install -r requirements.txt`.
- Run locally (Windows PowerShell):

```powershell
python .\main.py
```

Run from the project root so imports resolve correctly.

**Project-specific Conventions & Patterns**
- **Single-frame draw model**: All drawing occurs during `ScreenManager.draw()` and then `pygame.display.flip()` is called in `main.py`. Avoid calling `flip()` from other modules.
- **Font reuse**: Fonts are created once (see `ScreenManager.__init__`) and reused every frame to avoid performance issues. Follow that pattern when adding new UI elements.
- **Layout helpers**: `ui/gauges.py` exposes `get_layout_rects(screen_width, screen_height, count)` which delegates to grid helpers. These functions should return lists of `pygame.Rect` for consistent layout.
- **Minimal sensor API**: Sensor modules are expected to provide a simple interface that yields numeric values per read (no async/event bus in current design). Keep sensor implementations synchronous and lightweight.
- **Keep side-effects localized**: `main.py` manages initialization/cleanup (Pygame lifecycle). Other modules should not call `pygame.init()` or `pygame.quit()`.

**Discoverable TODOs & Caveats (do not assume otherwise)**
- `logging/datalogger.py` is empty — data persistence is not implemented yet.
- `sensors/ads_reader.py` is empty; `sensors/mock_reader.py` is only a stub. Expect to implement sensor logic when adding real hardware support.
- Bug to watch: `ui/gauges.py` defines `_grid_rects(...)` but currently does not return the computed `rects` list. Many callers assume a return value — fix or be careful when modifying layout helpers.
- UI functions assume a `pygame.Surface` named `screen` is supplied; do not create or swap surfaces outside `main.py`/`ScreenManager` without understanding frame lifecycle.

**When editing code**
- Small, focused changes are preferred. Preserve the entrypoint behavior in `main.py` and keep drawing logic inside `ScreenManager`.
- If adding heavy work (I/O, blocking reads), move it to a separate thread or implement sampling that completes within a frame time slice (30 FPS target).

**No tests / CI**
- There are no tests or CI configs in the repository. Ask the maintainer before adding a test framework.

---

If anything here is unclear or you want the instructions to be stricter about style or testing, tell me which section to expand or correct and I'll iterate.
