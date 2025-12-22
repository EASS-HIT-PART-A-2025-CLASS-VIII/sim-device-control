# sim-device-control

A small demo project that exposes a FastAPI service for controlling simulated devices and collecting logs.

**Project Internals**

As of now the project contains:
- Python fastapi backend
- Typescript React as a UI framework and Vite as a building tool and development server
- MySQL Database that saves logs and devices

Project folders layout:

```
.
├── backend
│   ├── scripts
│   ├── src
│   │   ├── sim_device_control
│   │   │   └── drivers
│   │   │       └── base
│   └── tests
└── frontend
    └── src
        ├── assets
        ├── components
        ├── panels
        └── utils
```

**Docker**

Make sure to configure environment variables in EVERY SINGLE component of this project.
For the Database, configure these environment variables (make sure they match with the backend's variable or else you won't be able to connect or run the project)

```bash
cp .env.example .env
```

Edit `.env` and set your Database user and password:

```
MYSQL_ROOT_PASSWORD=example_root_password
DB_USER=example_user
DB_PASSWORD=example_password
```

In order to run the project as a whole run the docker-compose.yml file:

```bash
docker compose up --build
```

If you need to run a specific component of the project, visit its directory and follow its README.md file

## TODO
- Implement MQTT protocol in the backend
- Create a simple rust project to behave as a simulated device
- Dockerize the rust project
