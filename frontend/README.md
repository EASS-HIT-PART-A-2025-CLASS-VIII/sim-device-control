# Frontend

Simulated Device Controller - React + Vite

A React + TypeScript frontend for controlling simulated devices and viewing logs. The UI provides device CRUD, sensor panels, a DC motor control, and a log viewer with time-based filtering.

Project layout

```
frontend/
├── Dockerfile
├── package.json
├── run-docker.sh
├── vite.config.ts
├── .env.example
├── src
│   ├── components
│   │   ├── device-action.tsx
│   │   ├── device-details.tsx
│   │   ├── device-selector.tsx
│   │   ├── device-write-action.tsx
│   │   └── device-read-action.tsx
│   ├── panels
│   │   ├── temperature-sensor.tsx
│   │   ├── pressure-sensor.tsx
│   │   ├── humidity-sensor.tsx
│   │   ├── dc-motor.tsx
│   │   └── log-viewer.tsx
│   ├── utils
│   │   └── device-dependancies.ts
│   ├── App.tsx
│   └── main.tsx
```

**Prerequisites:**
- Node.js 20+
- npm
- Docker (for container builds)

**Getting started (local)**

Install dependencies:

```bash
npm install
```

Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` and set your backend URL:

```
VITE_API_TARGET=http://backend:8000
```

Run the app locally with the Vite dev server:

```bash
npm run dev
```

If debugging is required then you can use the developer tools in your browser (F12 or Ctrl+Shift+I).

The app entry point is `src/main.tsx`.

**Docker**

Build and run the image (example):

```bash
docker build -t frontend .
docker run -p 5173:5173 frontend
```

Alternatively, you can run the `run-docker.sh` bash script:

```bash
./run-docker.sh
```

Note: Update `VITE_API_TARGET` in the Dockerfile to point to your backend service when running in Docker.

