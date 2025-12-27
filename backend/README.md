# Backend

Simulated Device Controller - FastAPI

FastAPI service that exposes CRUD endpoints for simulated devices and a simple logging API. Backend code is grouped under `src/sim_device_control/` by responsibility: routes and API (`app.py`), domain schemas (`schemas.py`), and a small fake persistence layer (`db.py`) used for demos and tests.

Project layout

```
backend/
├── Dockerfile
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
├── run-docker.sh
├── scripts
├── src
│   └── sim_device_control
│       ├── app.py
│       ├── drivers
│       │   ├── base
│       │   │   ├── base_controller.py
│       │   │   └── base_sensor.py
│       │   ├── db.py
│       │   ├── dc_motor.py
│       │   ├── device_manager.py
│       │   ├── humidity.py
│       │   ├── pressure.py
│       │   ├── stepper_motor.py
│       │   └── temperature.py
│       ├── __init__.py
│       ├── __main__.py
│       └── schemas.py
├── tests
│   ├── conftest.py
│   ├── test_app.py
│   └── test_db.py
└── uv.lock
```

**Prerequisites:**
- Python 3.12+
- Virtualenv
- Docker (for container builds)

**Getting started (local)**

Create and activate your virtualenv and install dependencies (project uses a `.venv` by convention):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env`.
set your Database user and password:

```
DATABASE_USER="example_user"
DATABASE_PASSWORD="example_password"
```
set your MQTT broker and port:

```
MQTT_BROKER="example_broker"
MQTT_PORT=1883
```

Run the API locally with uvicorn (module entrypoint):

```bash
python -m uvicorn sim_device_control.app:app --reload --host 0.0.0.0 --port 8000
```

If debugging is required then you can run `__main__.py` via vscode (use included .vscode/launch.json).

The ASGI app object is `sim_device_control.app:app` for other runners (Docker, tests, CI).

**Tests**

Run the pytest suite:

```bash
pytest -q
```

The tests use `fastapi.testclient.TestClient` and a `conftest.py` helper so the `src/` package is importable during test runs.

**Docker**

Build and run the image (example):

```bash
docker build -t sim-device-control .
docker run -p 8000:8000 sim-device-control
```

Alternatively, you can run the `run-docker.sh` bash script:

```bash
./run-docker.sh
```

