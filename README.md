# sim-device-control

A proof-of-concept project for controlling simulated IoT devices through MQTT,
featuring a Python FastAPI backend, React UI and Rust device simulator.

**Project Internals**

As of now the project contains:
- Python FastAPI backend
- TypeScript React as a UI framework and Vite as a building tool and development server
- MySQL Database that saves logs and devices
- Rust based device simulation via MQTT

Project folder layout:

```
.
├── backend (Python - FastAPI)
│   ├── scripts
│   ├── src
│   │   ├── sim_device_control
│   │   │   └── drivers
│   │   │       └── base
│   └── tests
├── frontend (TypeScript - react, vite)
│   └── src
│       ├── assets
│       ├── components
│       ├── panels
│       └── utils
└── sim-device (Rust)
    ├── src
    │   └── drivers

```

**Docker**

Make sure to configure environment variables in EVERY SINGLE component of this project (the default values in the `.env.example` are suitable for a localized execution).
To make things simple you can run the following command to copy all `.env.example` files and create brand new `.env` files:

```bash
find . -type f -name ".env.example" -execdir cp .env.example .env \;
```

For the Database, configure these environment variables (make sure they match with the backend's variable or else you won't be able to connect or run the project)

Edit `.env` and set your Database user and password:

```
MYSQL_ROOT_PASSWORD=example_root_password
DB_USER=example_user
DB_PASSWORD=example_password
```

In order to run the project as a whole run the `docker-compose.yml` file (add the `-d` flag if you don't need to see terminal logging):

```bash
docker compose up --build
```

The backend is available at:
`http://localhost:8000/docs#`
The frontend is available at:
`http://localhost:5173/`

After running the docker compose file and making sure everything runs properly, in order to add devices, run the `docker-compose.device.yml` file (add the `-d` flag if you don't need to see terminal logging):

```bash
docker compose -f docker-compose.devices.yml up --build
```

You should now see a a new device for each device type in the frontend, feel free to change `docker-compose.device.yml` to run your very own device simulation configuration (for example, 5 unique temperature sensors or 2 of each device type).

If you need to run a specific component of the project, visit its directory and follow its README.md file

## TODO (Low priority)
- Add digital_io and analog_io as device types.