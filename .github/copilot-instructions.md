## Purpose

Provide concise, actionable guidance so an AI coding agent can be immediately productive in this repository.

## Big picture

- This repo generates Home Assistant YAML dashboards by: 1) fetching live state from the Home Assistant Template API (`scripts/fetch_ha_data.py` + `queries/*.jinja`), 2) writing an intermediate `build/data.yaml`, and 3) rendering Jinja templates (`templates/*.jinja`) with `makejinja` to `build/dashboards/`.
- Deployment is handled via the `Makefile` using `rsync` or `scp` to copy `build/dashboards/` to the Home Assistant server.

## Key files to inspect

- `Makefile` — top-level tasks: `setup`, `generate`, `deploy`, `deploy-scp`, `freeze`, `clean`.
- `scripts/fetch_ha_data.py` — requests the HA Template API and writes `build/data.yaml`.
- `queries/*.jinja` — Jinja templates sent to HA's `/api/template` endpoint; output is JSON used as input to `makejinja`.
- `templates/dashboard.yaml.jinja` — dashboard template that iterates `areas.items()` and expects `build/data.yaml` to contain a top-level `areas` mapping.
- `makejinja.toml` — build configuration for `makejinja` (check if present/adjusted for environment).
- `requirements.txt` / `.venv` — Python deps and virtualenv workflow.
- `.env.example` — lists required environment variables (HA_URL, HA_TOKEN, HA_SSH_USER, HA_SSH_HOST, HA_DASHBOARD_PATH).

## Developer workflows & reproduceable commands

- Setup (one-time): `make setup` then `source .venv/bin/activate`.
- Generate dashboards locally: `make generate` (runs `scripts/fetch_ha_data.py` then `makejinja`).
- Deploy to HA server: `make deploy` (rsync) or `make deploy-scp` (scp).
- Update Python deps: install packages into the active `.venv`, then run `make freeze` and commit updated `requirements.txt`.
- Run fetch manually for debugging: `python3 scripts/fetch_ha_data.py` (ensure `.env` or env vars set).

## Project-specific conventions and gotchas

- Commit messages are enforced via Conventional Commits. Use `<type>: <description>` (e.g., `feat: add living room fan`). The repo has a commit-msg hook installed by `make setup`.
- Do NOT commit `.env` — use `.env.example` as reference.
- `queries/*.jinja` are NOT the final dashboards — they are rendered server-side by HA (via the Template API) and must produce JSON compatible with `templates/*.jinja`.
- `scripts/fetch_ha_data.py` wraps the JSON returned by HA into `{"areas": ...}` — templates depend on that key.
- The HA server must support the Advanced SSH add-on or otherwise have `rsync`/`scp` available for `make deploy` to work.

## Integration points & permissions

- Home Assistant Template API: script posts `queries/*.jinja` to `POST ${HA_URL}/api/template` with `Authorization: Bearer ${HA_TOKEN}`.
- Remote copy: `rsync`/`scp` using `$(HA_SSH_USER)@$(HA_SSH_HOST):$(HA_DASHBOARD_PATH)` — these env vars live in `.env`.

## Examples (copyable)

- Generate locally:

```
source .venv/bin/activate
make generate
ls build/dashboards/
```

- Debug fetch step only:

```
export HA_URL=http://homeassistant.local:8123
export HA_TOKEN=<<your_token>>
python3 scripts/fetch_ha_data.py
cat build/data.yaml
```

## What an AI agent should do first

1. Run `make setup` in a safe environment and `source .venv/bin/activate` to ensure tooling parity.
2. Run `python3 scripts/fetch_ha_data.py` (with `.env` or env vars) to produce `build/data.yaml` and inspect data shape.
3. Run `make generate` to verify templates render correctly into `build/dashboards/`.

## When to open a PR vs commit directly

- Small doc fixes or README clarity: open a PR (follow conventional commit message and CI hooks).
- Changes to `requirements.txt` must be committed via `make freeze` output and always go through review.

---

If any part of the environment (HA URL, token, or deployment host) changed or the `makejinja` configuration is different on your machine, tell me and I'll update these instructions accordingly.
