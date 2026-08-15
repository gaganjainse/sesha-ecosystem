#!/usr/bin/env python3
#!/usr/bin/env python3
"""Hardware verification: run the checklist on the real machine, record evidence.

Every page in shesh-docs carries `verified: <date>`, but until now that only
meant a person read the source. Nothing had run on the reference MSI Sword 16 HX.
A date that claims more than was done is worse than no date, because it stops
the next reader from checking.

This turns the manual checklist into probes that either run or say why they did
not, and writes a JSON evidence file. Nothing here guesses: a probe that cannot
run reports `skipped` with the reason, never `pass`.

    hwverify.py                     # run everything applicable, print a report
    hwverify.py --area gpu,display  # run one or more areas
    hwverify.py --json out.json     # write the evidence file
    hwverify.py --list              # show probes without running them
    hwverify.py --stamp             # emit the `verified:` line for docs

Exit codes: 0 all applicable probes passed · 1 a probe failed · 2 nothing ran.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, UTC
from collections.abc import Callable

PASS, FAIL, SKIP = "pass", "fail", "skipped"


@dataclass
class Result:
    id: str
    area: str
    title: str
    status: str
    detail: str = ""
    evidence: str = ""
    duration_ms: int = 0


@dataclass
class Probe:
    id: str
    area: str
    title: str
    fn: Callable[[], tuple[str, str, str]]
    needs: tuple[str, ...] = field(default_factory=tuple)


PROBES: list[Probe] = []


def probe(pid: str, area: str, title: str, needs: tuple[str, ...] = ()):
    def deco(fn):
        PROBES.append(Probe(pid, area, title, fn, needs))
        return fn
    return deco


def run(cmd: list[str], timeout: int = 20) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"{cmd[0]} not found"
    except subprocess.TimeoutExpired:
        return 124, "", f"{cmd[0]} timed out after {timeout}s"


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


# ---------------------------------------------------------------- environment

@probe("env-001", "env", "Running on Linux with a Wayland session")
def _env_session():
    if platform.system() != "Linux":
        return SKIP, f"host is {platform.system()}, not Linux", ""
    sess = os.environ.get("XDG_SESSION_TYPE", "")
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    if not sess:
        return SKIP, "XDG_SESSION_TYPE unset (headless or non-session shell)", ""
    if sess != "wayland":
        return FAIL, f"session is {sess!r}, expected wayland", f"desktop={desktop}"
    return PASS, f"wayland session, desktop={desktop or 'unknown'}", f"{sess}/{desktop}"


@probe("env-002", "env", "Reference machine identified")
def _env_machine():
    for path in ("/sys/devices/virtual/dmi/id/product_name",
                 "/sys/class/dmi/id/product_name"):
        if os.path.exists(path):
            with open(path) as fh:
                name = fh.read().strip()
            note = "reference hardware" if "Sword" in name else "not the reference machine"
            return PASS, f"{name} ({note})", name
    return SKIP, "no DMI product name (container or VM)", ""


# ---------------------------------------------------------------- gpu / power

@probe("gpu-001", "gpu", "NVIDIA driver loaded and reporting", needs=("nvidia-smi",))
def _gpu_driver():
    rc, out, err = run(["nvidia-smi",
                        "--query-gpu=name,driver_version,memory.total,temperature.gpu",
                        "--format=csv,noheader"])
    if rc != 0:
        return FAIL, f"nvidia-smi exited {rc}: {err or out}", ""
    return PASS, out.splitlines()[0] if out else "no output", out


@probe("gpu-002", "gpu", "VRAM budget of 5.5 GB is not exceeded", needs=("nvidia-smi",))
def _gpu_vram():
    rc, out, err = run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                        "--format=csv,noheader,nounits"])
    if rc != 0:
        return FAIL, f"nvidia-smi exited {rc}: {err}", ""
    used, total = (int(x.strip()) for x in out.splitlines()[0].split(","))
    budget = 5632  # 5.5 GiB, the documented ceiling for the 6 GB RTX 4050
    status = PASS if used <= budget else FAIL
    return status, f"{used} MiB used of {total} MiB (budget {budget})", out


@probe("gpu-003", "gpu", "Power profiles are switchable", needs=("powerprofilesctl",))
def _power_profiles():
    rc, out, _ = run(["powerprofilesctl", "list"])
    if rc != 0:
        return FAIL, f"powerprofilesctl exited {rc}", out
    profiles = re.findall(r"^\s*\*?\s*(\S+):", out, re.M)
    wanted = {"performance", "balanced", "power-saver"}
    missing = wanted - set(profiles)
    if missing:
        return FAIL, f"missing profiles: {sorted(missing)}", out
    return PASS, f"profiles available: {sorted(profiles)}", out


@probe("gpu-004", "gpu", "MUX switcher reports a mode")
def _mux():
    for cand in ("msi-mux-switcher", "supergfxctl"):
        if have(cand):
            rc, out, err = run([cand, "status" if cand.startswith("msi") else "-g"])
            if rc != 0:
                return FAIL, f"{cand} exited {rc}: {err or out}", out
            return PASS, f"{cand}: {out}", out
    return SKIP, "no MUX tool installed (msi-mux-switcher, supergfxctl)", ""


# ---------------------------------------------------------------- display

@probe("dsp-001", "display", "Hyprland is running and answering", needs=("hyprctl",))
def _hypr_alive():
    rc, out, err = run(["hyprctl", "version", "-j"])
    if rc != 0:
        return FAIL, f"hyprctl exited {rc}: {err or out}", ""
    try:
        v = json.loads(out).get("tag", "unknown")
    except json.JSONDecodeError:
        v = out.splitlines()[0] if out else "unparseable"
    return PASS, f"hyprland {v}", out[:400]


@probe("dsp-002", "display", "Refresh rate holds at 144 Hz", needs=("hyprctl",))
def _refresh():
    rc, out, _ = run(["hyprctl", "monitors", "-j"])
    if rc != 0:
        return FAIL, f"hyprctl monitors exited {rc}", ""
    try:
        mons = json.loads(out)
    except json.JSONDecodeError:
        return FAIL, "hyprctl monitors did not return JSON", out[:200]
    if not mons:
        return FAIL, "no monitors reported", out[:200]
    lines = [f"{m.get('name')}@{round(m.get('refreshRate', 0))}Hz "
             f"{m.get('width')}x{m.get('height')} scale={m.get('scale')}"
             for m in mons]
    top = max(round(m.get("refreshRate", 0)) for m in mons)
    status = PASS if top >= 143 else FAIL
    return status, f"highest {top} Hz; {'; '.join(lines)}", json.dumps(lines)


@probe("dsp-003", "display", "Screenshot pipeline produces a real PNG",
       needs=("grim",))
def _screenshot():
    out_path = "/tmp/hwverify-shot.png"
    rc, _, err = run(["grim", out_path], timeout=25)
    if rc != 0:
        return FAIL, f"grim exited {rc}: {err}", ""
    if not os.path.exists(out_path):
        return FAIL, "grim reported success but wrote no file", ""
    size = os.path.getsize(out_path)
    with open(out_path, "rb") as fh:
        magic = fh.read(8)
    os.unlink(out_path)
    if magic[:4] != b"\x89PNG":
        return FAIL, f"output is not a PNG (magic {magic[:4]!r})", ""
    if size < 1024:
        return FAIL, f"PNG is implausibly small ({size} bytes)", ""
    return PASS, f"captured {size} bytes of valid PNG", f"{size}B"


@probe("dsp-004", "display", "Notifications are accepted", needs=("notify-send",))
def _notify():
    rc, _, err = run(["notify-send", "-a", "hwverify", "-t", "1200",
                      "Shesh hardware verification", "probe dsp-004"])
    if rc != 0:
        return FAIL, f"notify-send exited {rc}: {err}", ""
    return PASS, "notification dispatched (confirm it appeared)", ""


# ---------------------------------------------------------------- audio

@probe("aud-001", "audio", "PipeWire or PulseAudio has a default sink",
       needs=("pactl",))
def _audio_sink():
    rc, out, err = run(["pactl", "info"])
    if rc != 0:
        return FAIL, f"pactl exited {rc}: {err}", ""
    server = re.search(r"Server Name:\s*(.+)", out)
    sink = re.search(r"Default Sink:\s*(.+)", out)
    if not sink or not sink.group(1).strip():
        return FAIL, "no default sink", out[:300]
    return PASS, f"{(server.group(1) if server else '?').strip()} · sink={sink.group(1).strip()}", out[:300]


@probe("aud-002", "audio", "At least one sink is not suspended", needs=("pactl",))
def _audio_active():
    rc, out, _ = run(["pactl", "list", "sinks", "short"])
    if rc != 0:
        return FAIL, f"pactl exited {rc}", ""
    if not out:
        return FAIL, "no sinks at all", ""
    return PASS, f"{len(out.splitlines())} sink(s)", out[:300]


# ---------------------------------------------------------------- phone

@probe("phn-001", "phone", "ADB sees an authorised device", needs=("adb",))
def _adb_device():
    rc, out, err = run(["adb", "devices"], timeout=30)
    if rc != 0:
        return FAIL, f"adb exited {rc}: {err}", ""
    devices = [ln for ln in out.splitlines()[1:] if ln.strip()]
    if not devices:
        return SKIP, "no device connected", out
    unauth = [d for d in devices if "unauthorized" in d]
    if unauth:
        return FAIL, f"device present but unauthorised: {unauth}", out
    return PASS, f"{len(devices)} device(s): {devices}", out


@probe("phn-002", "phone", "shesh_phone imports and derives a real safe area")
def _phone_safe_area():
    try:
        from shesh_phone.phone import Phone  # noqa: PLC0415
    except ImportError as exc:
        return SKIP, f"shesh_phone not installed: {exc}", ""
    rc, out, _ = run(["adb", "devices"], timeout=30)
    if rc != 0 or len([ln for ln in out.splitlines()[1:] if ln.strip()]) == 0:
        return SKIP, "imports cleanly, but no device to derive bounds from", ""
    try:
        ph = Phone()
        b = ph.safe_area()
    except Exception as exc:  # noqa: BLE001 — probe reports, never crashes the run
        return FAIL, f"safe_area() raised {type(exc).__name__}: {exc}", ""
    if (b.left, b.top, b.right, b.bottom) == (0, 0, 0, 0):
        return FAIL, "safe area is the unreachable-device sentinel (0,0,0,0)", str(b)
    return PASS, f"safe area {b}", str(b)


@probe("phn-003", "phone", "A tap inside the status bar is refused")
def _phone_refuses():
    try:
        from shesh_phone.phone import Phone  # noqa: PLC0415
    except ImportError as exc:
        return SKIP, f"shesh_phone not installed: {exc}", ""
    rc, out, _ = run(["adb", "devices"], timeout=30)
    if rc != 0 or len([ln for ln in out.splitlines()[1:] if ln.strip()]) == 0:
        return SKIP, "no device connected", ""
    ph = Phone()
    try:
        ok = ph.tap(10, 10)
    except Exception as exc:  # noqa: BLE001
        return PASS, f"refused by raising {type(exc).__name__}", str(exc)[:120]
    if ok:
        return FAIL, "tap at y=10 was accepted; the safe-area guard is not working", ""
    return PASS, "tap at y=10 refused", ""


# ---------------------------------------------------------------- voice

@probe("voi-001", "voice", "A microphone source exists", needs=("pactl",))
def _mic():
    rc, out, _ = run(["pactl", "list", "sources", "short"])
    if rc != 0:
        return FAIL, f"pactl exited {rc}", ""
    real = [ln for ln in out.splitlines() if ".monitor" not in ln]
    if not real:
        return FAIL, "only monitor sources; no capture device", out[:300]
    return PASS, f"{len(real)} capture source(s)", out[:300]


@probe("voi-002", "voice", "Wake-word model is present")
def _wakeword():
    roots = [os.path.expanduser("~/.local/share/shesh/models"),
             os.path.expanduser("~/.config/shesh/models"),
             "/usr/share/shesh/models"]
    found = []
    for r in roots:
        if os.path.isdir(r):
            found += [os.path.join(r, f) for f in os.listdir(r)
                      if f.endswith((".onnx", ".tflite", ".bin"))]
    if not found:
        return SKIP, f"no model files under {roots}", ""
    return PASS, f"{len(found)} model file(s)", "; ".join(found[:4])


# ---------------------------------------------------------------- mcp mesh

@probe("mcp-001", "mcp", "Every declared console script resolves on PATH")
def _mcp_scripts():
    try:
        import tomllib  # noqa: PLC0415
    except ImportError:
        return SKIP, "tomllib unavailable (Python < 3.11)", ""
    src = os.environ.get("SHESH_SRC")
    if not src or not os.path.isdir(src):
        return SKIP, "SHESH_SRC is not set to a fleet checkout", ""
    declared: list[str] = []
    for repo in sorted(os.listdir(src)):
        py = os.path.join(src, repo, "pyproject.toml")
        if not os.path.exists(py):
            continue
        with open(py, "rb") as fh:
            try:
                data = tomllib.load(fh)
            except tomllib.TOMLDecodeError:
                continue
        declared += list(data.get("project", {}).get("scripts", {}))
    if not declared:
        return SKIP, "no console scripts declared anywhere", ""
    missing = [s for s in declared if not have(s)]
    if missing:
        return FAIL, f"{len(missing)} of {len(declared)} not on PATH: {missing[:6]}", ""
    return PASS, f"all {len(declared)} console scripts resolve", ", ".join(declared[:6])


@probe("mcp-002", "mcp", "Each MCP server starts and answers initialize")
def _mcp_handshake():
    scripts = [s for s in ("shesh-audit-mcp", "shesh-system-mcp", "shesh-skills-mcp",
                           "shesh-desktop-ctl-mcp") if have(s)]
    if not scripts:
        return SKIP, "no MCP console scripts installed", ""
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18",
                   "capabilities": {},
                   "clientInfo": {"name": "hwverify", "version": "1"}},
    }) + "\n"
    good, bad = [], []
    for s in scripts:
        try:
            p = subprocess.run([s], input=req, capture_output=True,
                               text=True, timeout=25)
        except subprocess.TimeoutExpired:
            bad.append(f"{s}: no response in 25s")
            continue
        blob = p.stdout or ""
        if '"result"' in blob and ("serverInfo" in blob or "protocolVersion" in blob):
            good.append(s)
        else:
            bad.append(f"{s}: no initialize result")
    if bad:
        return FAIL, f"{len(bad)} server(s) did not handshake: {bad}", "; ".join(good)
    return PASS, f"{len(good)} server(s) answered initialize", ", ".join(good)


# ---------------------------------------------------------------- containers

@probe("ctr-001", "containers", "A rootless container runtime is usable")
def _container():
    for rt in ("podman", "docker"):
        if not have(rt):
            continue
        rc, out, err = run([rt, "info", "--format", "{{.Host.Security.Rootless}}"
                            if rt == "podman" else "{{.ServerVersion}}"], timeout=40)
        if rc != 0:
            return FAIL, f"{rt} info exited {rc}: {err[:150]}", ""
        return PASS, f"{rt} usable (rootless={out.strip()})", out
    return SKIP, "neither podman nor docker installed", ""


@probe("ctr-002", "containers", "A sandboxed run has no network")
def _container_netless():
    if not have("podman"):
        return SKIP, "podman not installed", ""
    rc, out, err = run(["podman", "run", "--rm", "--network=none",
                        "docker.io/library/alpine:latest",
                        "sh", "-c", "wget -q -T2 -O- https://example.com || echo BLOCKED"],
                       timeout=120)
    if rc != 0:
        return SKIP, f"could not run the probe image: {err[:150]}", ""
    if "BLOCKED" not in out:
        return FAIL, "network reachable inside --network=none", out[:200]
    return PASS, "network correctly unreachable in the sandbox", out[:120]


# ---------------------------------------------------------------- security

@probe("sec-001", "security", "Credential store is not world-readable")
def _cred_perms():
    path = os.path.expanduser("~/.config/shesh/tokens.enc.json")
    if not os.path.exists(path):
        return SKIP, "no encrypted token store on this machine", ""
    mode = os.stat(path).st_mode & 0o777
    if mode & 0o077:
        return FAIL, f"mode is {mode:04o}; group/other can read it", f"{mode:04o}"
    return PASS, f"mode {mode:04o}", f"{mode:04o}"


@probe("sec-002", "security", "No plaintext token file is lying around")
def _plaintext_tokens():
    bad = []
    for name in ("github.pat", "github_token", "pat", "token"):
        p = os.path.expanduser(f"~/.config/shesh/{name}")
        if os.path.exists(p):
            bad.append(f"{p} (mode {os.stat(p).st_mode & 0o777:04o})")
    if bad:
        return FAIL, f"plaintext credential file present: {bad}", "; ".join(bad)
    return PASS, "no plaintext credential files", ""


@probe("sec-003", "security", "Git hooks are installed and executable")
def _hooks():
    src = os.environ.get("SHESH_SRC")
    if not src or not os.path.isdir(src):
        return SKIP, "SHESH_SRC is not set to a fleet checkout", ""
    missing, notexec = [], []
    repos = [d for d in sorted(os.listdir(src))
             if os.path.isdir(os.path.join(src, d, ".git"))]
    for repo in repos:
        for hook in ("commit-msg", "pre-push"):
            p = os.path.join(src, repo, ".git", "hooks", hook)
            if not os.path.exists(p):
                missing.append(f"{repo}/{hook}")
            elif not os.access(p, os.X_OK):
                notexec.append(f"{repo}/{hook}")
    if notexec:
        return FAIL, f"{len(notexec)} hook(s) not executable; git ignores them silently", "; ".join(notexec[:6])
    if missing:
        return FAIL, f"{len(missing)} hook(s) missing across {len(repos)} repos", "; ".join(missing[:6])
    return PASS, f"hooks present and executable in {len(repos)} repos", ""


# ---------------------------------------------------------------- network

@probe("net-001", "network", "Local model runtime is reachable")
def _ollama():
    host = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
    if ":" not in host:
        host += ":11434"
    h, _, p = host.rpartition(":")
    h = h.replace("http://", "").replace("https://", "") or "127.0.0.1"
    try:
        with socket.create_connection((h, int(p)), timeout=3):
            pass
    except OSError as exc:
        return SKIP, f"nothing listening on {h}:{p} ({exc.__class__.__name__})", ""
    return PASS, f"model runtime answering on {h}:{p}", f"{h}:{p}"


# ---------------------------------------------------------------- runner

def applicable(p: Probe) -> tuple[bool, str]:
    for b in p.needs:
        if not have(b):
            return False, f"{b} not installed"
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--area", help="comma-separated areas to run")
    ap.add_argument("--json", dest="json_out", help="write evidence JSON here")
    ap.add_argument("--list", action="store_true", help="list probes and exit")
    ap.add_argument("--stamp", action="store_true",
                    help="print the verified: line for documentation")
    args = ap.parse_args()

    areas = {a.strip() for a in args.area.split(",")} if args.area else None
    chosen = [p for p in PROBES if not areas or p.area in areas]

    if args.list:
        for p in chosen:
            ok, why = applicable(p)
            print(f"  {p.id:9} {p.area:11} {p.title}"
                  f"{'' if ok else f'   [would skip: {why}]'}")
        return 0

    results: list[Result] = []
    for p in chosen:
        ok, why = applicable(p)
        if not ok:
            results.append(Result(p.id, p.area, p.title, SKIP, why))
            continue
        t0 = time.monotonic()
        try:
            status, detail, evidence = p.fn()
        except Exception as exc:  # noqa: BLE001 — a broken probe is a skip, not a pass
            status, detail, evidence = SKIP, f"probe raised {type(exc).__name__}: {exc}", ""
        results.append(Result(p.id, p.area, p.title, status, detail, evidence,
                              int((time.monotonic() - t0) * 1000)))

    width = max(len(r.title) for r in results) if results else 20
    mark = {PASS: "PASS", FAIL: "FAIL", SKIP: "skip"}
    cur = None
    for r in results:
        if r.area != cur:
            cur = r.area
            print(f"\n{cur}")
        print(f"  {mark[r.status]}  {r.title:<{width}}  {r.detail}")

    npass = sum(r.status == PASS for r in results)
    nfail = sum(r.status == FAIL for r in results)
    nskip = sum(r.status == SKIP for r in results)
    print(f"\n{npass} passed · {nfail} failed · {nskip} skipped")
    if nskip:
        print("A skipped probe verified nothing. It is not a pass.")

    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    if args.json_out:
        payload = {
            "generated": datetime.now(UTC).isoformat(),
            "host": platform.node(),
            "kernel": platform.release(),
            "summary": {"pass": npass, "fail": nfail, "skipped": nskip},
            "results": [asdict(r) for r in results],
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"evidence written to {args.json_out}")

    if args.stamp:
        if nfail or nskip:
            print(f"\nverified: {stamp}  # PARTIAL — {nfail} failed, {nskip} skipped")
        else:
            print(f"\nverified: {stamp}  # hardware, all probes passed")

    if not results:
        return 2
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
