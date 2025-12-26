# Simulated Device (Rust)

Simulated MQTT IOT device written in Rust. It connects to an MQTT broker, announces its connection state, listens for JSON commands, performs device-specific operations, and publishes responses.

Implemented with `rumqttc` for MQTT, `serde`/`serde_json` for payloads, and `dotenvy` for environment configuration.

## Project Layout

```
sim-device/
├── Cargo.toml
├── Dockerfile
├── run-docker.sh
├── src
│   ├── main.rs
│   └── drivers
│       ├── dc_motor.rs
│       ├── device.rs
│       ├── humidity_sensor.rs
│       ├── mqtt.rs
│       ├── pressure_sensor.rs
│       ├── stepper_motor.rs
│       └── temperature_sensor.rs
└── target
```

## Prerequisites

- Rust 1.82+ (`rustup` recommended)
- An MQTT broker (e.g., Mosquitto, HiveMQ)
- Docker (optional, for containerized runs)

## Configuration

The app reads environment variables (via `.env` if present):

Configure environment variables:

```bash
cp .env.example .env
```

- `DEVICE_TYPE`: device type (e.g., `temperature_sensor`, `humidity_sensor`, `pressure_sensor`, `dc_motor`, `stepper_motor`)
- `DEVICE_ID`: unique identifier for this simulated device
- `MQTT_BROKER`: broker host or IP (e.g., `localhost`, `mqtt`, `broker.hivemq.com`)
- `MQTT_PORT`: broker port (e.g., `1883`)

## Build & Run (Local)

```bash
cargo build --release
cargo run
```

`cargo run` will load variables from `.env` automatically if present. You can override values on the command line, for example:

```bash
DEVICE_TYPE=humidity_sensor DEVICE_ID=dev1 cargo run
```

## Docker

Build and run the image:

```bash
docker build -t mqtt-device .
docker run --network host mqtt-device
```

Alternatively, you can run the `run-docker.sh` bash script:

```bash
./run-docker.sh
```

Notes:
- The container is configured with `STOPSIGNAL SIGTERM`. `docker stop` sends SIGTERM, which the app handles gracefully.

## MQTT Topics & Payloads

- Connection status topic: `sim-device-control/connections`
	- Connect payload: `{ "device_id": "<id>", "device_type": "<type>", "status": "connected" }`
	- Disconnect payload: `{ "device_id": "<id>", "device_type": "<type>", "status": "disconnected" }`

- Command topic: `sim-device-control/<device_id>/command`
    - Payload example: `{ "id": "<cmd_id>", "command": "<cmd>", "parameter": "<param>" }`
    - Commands per device type:
        - All device types:
            - `{ "id": "<cmd_id>", "command": "get_status", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "get_version", "parameter": "" }`
        - temperature_sensor:
            - `{ "id": "<cmd_id>", "command": "read_temperature", "parameter": "" }`
        - pressure_sensor:
            - `{ "id": "<cmd_id>", "command": "read_pressure", "parameter": "" }`
        - humidity_sensor:
            - `{ "id": "<cmd_id>", "command": "read_humidity", "parameter": "" }`
        - dc_motor:
            - `{ "id": "<cmd_id>", "command": "get_speed", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_speed", "parameter": "<f64 between 0.0-100.0>" }`
            - `{ "id": "<cmd_id>", "command": "get_direction", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_direction", "parameter": "<forward/backward>" }`
        - stepper_motor:
            - `{ "id": "<cmd_id>", "command": "get_speed", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_speed", "parameter": "<f64>" }`
            - `{ "id": "<cmd_id>", "command": "get_acceleration", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_acceleration", "parameter": "<f64>" }`
            - `{ "id": "<cmd_id>", "command": "get_direction", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_direction", "parameter": "<forward/backward>" }`
            - `{ "id": "<cmd_id>", "command": "get_location", "parameter": "" }`
            - `{ "id": "<cmd_id>", "command": "set_location_relative", "parameter": "<f64>" }`
            - `{ "id": "<cmd_id>", "command": "set_location_absolute", "parameter": "<f64>" }`

- Response topic: `sim-device-control/<device_id>/response`
    - Payload example: `{ "id": "<cmd_id>", "device_id": "<id>", "response": "<result>", "timestamp": <millis> }`

## Graceful Shutdown

- On startup, the device announces a `connected` status.
- The app handles Ctrl+C and Docker `SIGTERM` (via `ctrlc`), publishes a `disconnected` status, and exits cleanly.

## Troubleshooting

- If connection fails, verify `MQTT_BROKER` and `MQTT_PORT` and that the broker is reachable from your environment (container vs host).

