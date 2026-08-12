# 🎞️ shesh-media

Soma media tools — screenshots, screen recording, wallpaper, audio routing.

- Part of [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)
- Layer: Soma (body)
- Provides: screenshots, recording, wallpaper, audio-routing

## Tools
- `take_screenshot` — grim+slurp pipeline, returns path
- `start_recording` / `stop_recording` — wf-recorder / obs
- `set_wallpaper` — swaybg / hyprpaper
- `set_audio_sink` / `list_sinks` — wpctl / pactl

All behind Guard — protected paths denied.

## Dev
```bash
uv sync && uv run pytest
```
