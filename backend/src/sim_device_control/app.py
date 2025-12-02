from fastapi import FastAPI, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
import socket
import inspect
from .schemas import SimDevice, DeviceType, LogRecord, MotorDirection
from .drivers.db import get_db
from .drivers.device_manager import get_device_manager
from .drivers import device_manager

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
        raise HTTPException(status_code=400, detail = str(e))


# region general device operations

@app.get("/devices/", response_model = List[SimDevice])
def list_devices(db = Depends(get_db)):
    add_record(db, description = "Listed all devices")
    return db.get_devices()


@app.post("/devices/", response_model = SimDevice)
def create_device(device: SimDevice, db = Depends(get_db), manager = Depends(get_device_manager)):
    try:
        add_record(db, description = f"Attempting to create device {device.uuid}")
        manager.add_device(device)
        db.add_device(device)
    except ValueError as e:
        add_record(db, description = f"Failed to create device {device.uuid}: {str(e)}")
        raise HTTPException(status_code=400, detail = str(e))
    add_record(db, description = f"Successfully created device {device.uuid}")
    return device


@app.get("/devices/type/{device_type}", response_model = List[SimDevice])
def get_devices_by_type(device_type: DeviceType, db = Depends(get_db)):
    add_record(db, description = f"Attempting to get devices by type {device_type}")
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == device_type:
            match_devices.append(device)
    if len(match_devices) == 0:
        add_record(db, description = f"No devices found for type {device_type}")
        raise HTTPException(status_code = 404, detail="Device type not found")
    add_record(db, description = f"Found {len(match_devices)} devices of type {device_type}")
    return match_devices


# You can't actually change an existing device's info, disabled in case it would be needed later
#
# @app.put("/devices/{device_uuid}", response_model = SimDevice)
# def update_device(device_uuid: str, updated_device: SimDevice, db = Depends(get_db)):
#     try:
#         add_record(db, description = f"Attempting to update device {device_uuid}")
#         device_controller.add_device(updated_device)
#         device_controller.remove_device(device_uuid)
#         db.update_device(device_uuid, updated_device)
#     except ValueError as e:
#         add_record(db, description = f"failed to update device {device_uuid}: {str(e)}")
#         raise HTTPException(status_code = 404, detail = str(e))
#     add_record(db, description = f"Successfully updated device {device_uuid}")
#     return updated_device


@app.delete("/devices/{device_uuid}")
def delete_device(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    try: 
        add_record(db, description = f"Attempting to delete device {device_uuid}")
        manager.remove_device(device_uuid)
        db.delete_device(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to delete device {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))
    add_record(db, description = f"Successfully deleted device {device_uuid}")

# endregion

# region device specific operations

# region all device types

@app.get("/devices/get_status", response_model = str)
def get_device_status(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    try:
        add_record(db, description = f"Getting status from device {device_uuid}")
        return manager.get_status(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to get status from device {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))


@app.get("/devices/get_version", response_model = str)
def get_device_version(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    try:
        add_record(db, description = f"Getting version from device {device_uuid}")
        return manager.get_version(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to get version from device {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))
    
# endregion

# region temperature sensor operations

@app.get("/devices/temperature_sensor/read_temperature", response_model = float)
def read_temperature(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.TEMPERATURE_SENSOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a temperature sensor")
        raise HTTPException(status_code = 404, detail="Device is not a temperature sensor")
    try:
        add_record(db, description = f"Reading temperature from sensor {device_uuid}")
        return manager.read_temperature(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to read temperature from sensor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))

# endregion

# region pressure sensor operations

@app.get("/devices/pressure_sensor/read_pressure", response_model = float)
def read_pressure(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.PRESSURE_SENSOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a pressure sensor")
        raise HTTPException(status_code = 404, detail="Device is not a pressure sensor")
    try:
        add_record(db, description = f"Reading pressure from sensor {device_uuid}")
        return manager.read_pressure(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to read pressure from sensor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))

# endregion

# region humidity sensor operations

@app.get("/devices/humidity_sensor/read_humidity", response_model = float)
def read_humidity(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.HUMIDITY_SENSOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a humidity sensor")
        raise HTTPException(status_code = 404, detail="Device is not a humidity sensor")
    try:
        add_record(db, description = f"Reading humidity from sensor {device_uuid}")
        return manager.read_humidity(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to read humidity from sensor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))

# endregion

# region dc motor operations

@app.get("/devices/dc_motor/get_speed", response_model = float)
def get_dc_motor_speed(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.DC_MOTOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a dc motor")
        raise HTTPException(status_code = 404, detail = "Device is not a dc motor")
    try:
        add_record(db, description = f"Reading dc motor speed from motor {device_uuid}")
        return manager.get_dc_motor_speed(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to read dc motor speed from motor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))
    

@app.get("/devices/dc_motor/get_direction", response_model = MotorDirection)
def get_dc_motor_direction(device_uuid: str, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.DC_MOTOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a dc motor")
        raise HTTPException(status_code = 404, detail = "Device is not a dc motor")
    try:
        add_record(db, description = f"Reading dc motor direction from motor {device_uuid}")
        return manager.get_dc_motor_direction(device_uuid)
    except ValueError as e:
        add_record(db, description = f"Failed to read dc motor direction from motor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))


@app.put("/devices/dc_motor/set_speed")
def set_dc_motor_speed(device_uuid: str, speed: float, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.DC_MOTOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a dc motor")
        raise HTTPException(status_code = 404, detail = "Device is not a dc motor")
    try:
        add_record(db, description = f"Setting dc motor speed for motor {device_uuid} to {speed}")
        manager.set_dc_motor_speed(device_uuid, speed)
    except ValueError as e:
        add_record(db, description = f"Failed to set dc motor speed for motor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))
    

@app.put("/devices/dc_motor/set_direction")
def set_dc_motor_direction(device_uuid: str, direction: MotorDirection, db = Depends(get_db), manager = Depends(get_device_manager)):
    match_devices: List[SimDevice] = []
    for device in db.get_devices():
        if device.type == DeviceType.DC_MOTOR:
            match_devices.append(device)
    if device_uuid not in [d.uuid for d in match_devices]:
        add_record(db, description = f"Device {device_uuid} is not a dc motor")
        raise HTTPException(status_code = 404, detail = "Device is not a dc motor")
    try:
        add_record(db, description = f"Setting dc motor direction for motor {device_uuid} to {direction}")
        manager.set_dc_motor_direction(device_uuid, direction)
    except ValueError as e:
        add_record(db, description = f"Failed to set dc motor direction for motor {device_uuid}: {str(e)}")
        raise HTTPException(status_code = 404, detail = str(e))

# endregion

# endregion

# region logging operations

@app.get("/logs/", response_model = List[LogRecord])
def list_logs(db = Depends(get_db)):
    add_record(db, description = "Listed all log records")
    return db.get_log()


@app.get("/logs/filtered", response_model = List[LogRecord])
def list_logs_by_time(start_time: datetime = "YYYY-MM-DDThh:mm:ss", end_time: datetime = "YYYY-MM-DDThh:mm:ss", db = Depends(get_db)):
    add_record(db, description = f"Listed log records from {start_time} to {end_time}")
    matched_logs: List[LogRecord] = []
    for record in db.get_log():
        if start_time <= record.timestamp <= end_time:
            matched_logs.append(record)
    return matched_logs


@app.post("/logs/", response_model = LogRecord)
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
        raise HTTPException(status_code=400, detail = str(e))
    return record

# endregion
