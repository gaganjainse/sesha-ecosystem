# Tutorial — voice, settings, and organizer working together

Status: living · last verified 2026-08-13
Components: [shesh-voice](https://github.com/gaganjainse/shesh-voice)
(Newelle fork), Smart Organizer v2 (shesh-desktop)

A daily-driver flow: speak to the assistant, it files your downloads, the
settings overlay stays out of the way.

## Setup order matters

1. **Voice overlay first.** Install shesh-voice per
   [GETTING_STARTED §1.5](../GETTING_STARTED.md); confirm the mini-window and
   hotkeys work (Newelle upstream supports STT/TTS with wakeword).
2. **Local model stack.** Voice talks to the local Ollama 6 GB stack; if
   Ollama is down the model router falls back free-first (see
   [model-router](../tools/model-router.md)).
3. **Then the organizer.** Follow
   [organize-downloads](organize-downloads.md) — dry-run, rules, systemd.

## The combined flow

- "Organize my downloads" → the organizer pipeline runs; every move is
  logged by the apply layer.
- Every tool call passes the audit guard — organizer moves match the policy
  in [skills/POLICY](../skills/POLICY.md), and anything novel asks first.

## Verify

- [ ] Ask by voice to organize Downloads; confirm the audit log shows the
      tool calls (`~/.local/share/shesh/audit/events.jsonl`).
- [ ] Confirm a deny case: ask the assistant to touch something under
      `~/.ssh` — it must refuse (policy `deny`, no confirmation prompt).
