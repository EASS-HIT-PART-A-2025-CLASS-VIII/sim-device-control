from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="Simulated Device Controller API")

class DeviceType(Enum):
    TEMPERATURE_SENSOR = "temperature_sensor"
    PRESSURE_SENSOR = "pressure_sensor"
    HUMIDITY_SENSOR = "humidity_sensor"
    DC_MOTOR = "dc_motor"
    STEPPER_MOTOR = "stepper_motor"
    DIGITAL_PORT = "digital_port"
    ANALOG_PORT = "analog_port"

class SimDevice(BaseModel):
    id: int
    type: DeviceType
    name: str
    status: str
    description: str

devices_db: List[SimDevice] = []

@app.get("/devices/", response_model=List[SimDevice])
def list_devices():
    return devices_db

@app.get("/devices/{device_type}", response_model=SimDevice)
def get_device_by_type(device_type: DeviceType):
    match_devices: List[SimDevice] = []
    for device in devices_db:
        if device.type == device_type:
            match_devices.append(device)
    if len(match_devices) == 0:
        raise HTTPException(status_code=404, detail="Device type not found")
    return match_devices

@app.post("/devices/", response_model=SimDevice)
def create_device(device: SimDevice):
    devices_db.append(device)
    return device

@app.put("/devices/{device_id}", response_model=SimDevice)
def update_device(device_id: int, updated_device: SimDevice):
    for index, device in enumerate(devices_db):
        if device.id == device_id:
            devices_db[index] = updated_device
            return updated_device
    raise HTTPException(status_code=404, detail="Device not found")

@app.delete("/devices/{device_id}")
def delete_device(device_id: int):
    for index, device in enumerate(devices_db):
        if device.id == device_id:
            del devices_db[index]
            return {"detail": "Device deleted"}
    raise HTTPException(status_code=404, detail="Device not found")