# sim-device-control

A small demo project that exposes a FastAPI service for controlling simulated devices and collecting logs.

**Project Internals**

As of now the project contains:
- Python fastapi backend
- Typescript React as a UI framework and Vite as a building tool and development server

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

In order to run the project as a whole run the docker-compose.yml file:

```bash
docker compose up -d --build
```

If you need to run a specific component of the project, visit its directory and follow its README.md file

## TODO
- Implement a Database
- have the backend communicate with the Database
- Dockerize the Database
- Implement MQTT protocol in the backend
- Create a simple rust project to behave as a simulated device
- Dockerize the rust project