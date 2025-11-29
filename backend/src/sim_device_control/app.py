from fastapi import FastAPI, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
import socket
import inspect
from .schemas import SimDevice, DeviceType, LogRecord
from .db import get_db

app = FastAPI(title="Simulated Device Controller API")

def add_record(db, device_uuid: str = "", description: str = ""):
    try:
        record = LogRecord(
            uuid = uuid.uuid4(),
            user = socket.gethostname() + "-" + socket.gethostbyname(socket.gethostname()),
            device_uuid = device_uuid,
            action = inspect.stack()[1].function,
            description = description,
            timestamp = datetime.now()
        )
        db.add_log(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# region general device operations

@app.get("/devices/", response_model=List[SimDevice])
def list_devices(db = Depends(get_db)):
    add_record(db, description = "Listed all devices")
    return db.get_devices()


@app.post("/devices/", response_model=SimDevice)
def create_device(device: SimDevice, db = Depends(get_db)):
    try:
        add_record(db, description = f"Attempting to create device {device.uuid}")
        db.add_device(device)
    except ValueError as e:
        add_record(db, description = f"Failed to create device {device.uuid}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    add_record(db, description = f"Successfully created device {device.uuid}")
    return device


@app.get("/devices/{device_type}", response_model=List[SimDevice])
def get_devices_by_type(device_type: DeviceType, db = Depends(get_db)):
    add_record(db, description = f"Attempting to get devices by type {device_type}")
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == device_type:
            match_devices.append(device)
    if len(match_devices) == 0:
        add_record(db, description = f"No devices found for type {device_type}")
        raise HTTPException(status_code=404, detail="Device type not found")
    add_record(db, description = f"Found {len(match_devices)} devices of type {device_type}")
    return match_devices


@app.put("/devices/{device_uuid}", response_model=SimDevice)
def update_device(device_uuid: str, updated_device: SimDevice, db = Depends(get_db)):
    try:
        add_record(db, description = f"Attempting to update device {device_uuid}")
        db.update_device(device_uuid, updated_device)
    except ValueError as e:
        add_record(db, description = f"failed to update device {device_uuid}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    add_record(db, description = f"Successfully updated device {device_uuid}")
    return updated_device


@app.delete("/devices/{device_uuid}")
def delete_device(device_uuid: str, db = Depends(get_db)):
    try: 
        add_record(db, description = f"Attempting to delete device {device_uuid}")
        db.delete_device(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to delete device {device_uuid}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    add_record(db, description = f"Successfully deleted device {device_uuid}")

# endregion

# region logging operations

@app.get("/logs/", response_model=List[LogRecord])
def list_logs(db = Depends(get_db)):
    add_record(db, description = "Listed all log records")
    return db.get_log()


@app.get("/logs/filtered", response_model=List[LogRecord])
def list_logs_by_time(start_time: datetime = "YYYY-MM-DDThh:mm:ss", end_time: datetime = "YYYY-MM-DDThh:mm:ss", db = Depends(get_db)):
    add_record(db, description = f"Listed log records from {start_time} to {end_time}")
    matched_logs: List[LogRecord] = []
    for record in db.get_log():
        if start_time <= record.timestamp <= end_time:
            matched_logs.append(record)
    return matched_logs


@app.post("/logs/", response_model=LogRecord)
def create_entry(action: str, description: str, device_uuid: str = "", db = Depends(get_db)):
    try:
        record = LogRecord(
            uuid = uuid.uuid4(),
            user = socket.gethostname() + "-" + socket.gethostbyname(socket.gethostname()),
            device_uuid = device_uuid,
            action = action,
            description = description,
            timestamp = datetime.now()
        )
        db.add_log(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return record

# endregion
