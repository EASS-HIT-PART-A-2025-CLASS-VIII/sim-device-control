# sim-device-control

A small demo project that exposes a FastAPI service for controlling simulated devices and collecting logs.

**Backend**

Everything under this section requires you to be under the `backend/` folder.

Simulated Device Controller - FastAPI

FastAPI service that exposes CRUD endpoints for simulated devices and a simple logging API. Backend code is grouped under `src/sim_device_control/` by responsibility: routes and API (`app.py`), domain schemas (`schemas.py`), and a small fake persistence layer (`db.py`) used for demos and tests.

Project layout

```
backend/
├── src/sim_device_control/
│   ├── __init__.py        # package metadata
│   ├── app.py             # FastAPI app + routes
│   ├── schemas.py         # Pydantic request/response models and enums
│   ├── db.py              # small in-memory "fake" DB + get_db dependency
│   └── __main__.py        # uvicorn entrypoint for local dev
├── tests/                 # pytest test suite (unit + integration with TestClient)
├── requirements.txt       # runtime dependencies
├── requirements-dev.txt   # dev / test dependencies
├── pyproject.toml
└── run-*.sh               # helper scripts for running in venv or Docker
```

Getting started (local)

Create and activate your virtualenv and install dependencies (project uses a `.venv` by convention):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API locally with uvicorn (module entrypoint):

```bash
python -m uvicorn sim_device_control.__main__:app --reload --host 0.0.0.0 --port 8000
```

Also possible with running `__main__.py` via vscode.

The ASGI app object is `sim_device_control.app:app` for other runners (Docker, tests, CI).

Tests

Run the pytest suite:

```bash
pytest -q
```

The tests use `fastapi.testclient.TestClient` and a `conftest.py` helper so the `src/` package is importable during test runs.

Docker

Build and run the image (example):

```bash
docker build -t sim-device-control .
docker run -p 8000:8000 sim-device-control
```

Alternatively, you can run the `run-docker.sh` bash script:

```bash
./run-docker.sh
```

