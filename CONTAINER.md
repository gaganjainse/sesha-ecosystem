# Shesh development / canary container

One-command reproducible environment matching the CachyOS/Arch target.

## Build

```bash
podman build -t shesh-dev .
# or with docker
docker build -t shesh-dev .
```

## Run the canary gate

```bash
podman run --rm shesh-dev
```

## Drop into a shell

```bash
podman run --rm -it shesh-dev bash
```

## What's inside

- Arch base + Python 3, git, ruff, restic, podman (for nested sandboxing)
- The `shesh-ecosystem` package and every `shesh-*` component installed editable
- The canary gate (`pytest tests/`) as the default command

No models, API keys, or secrets are baked in. For Distrobox on the host:

```bash
distrobox create --image shesh-dev --name shesh
distrobox enter shesh
```
