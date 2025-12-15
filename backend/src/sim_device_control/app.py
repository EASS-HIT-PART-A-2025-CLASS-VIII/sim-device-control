from fastapi import FastAPI, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
import socket
import inspect
from .schemas import SimDevice, DeviceType, LogRecord, MotorDirection
from .drivers.db import get_db
from .drivers.device_manager import get_device_manager

tags_metadata = [
    {
        "name": "General Device Control",
        "description": "General operations: add, remove, list.",
    },
    {
        "name": "Generic Device Operations",
        "description": "Operations applicable to all device types.",
    },
    {
        "name": "Temperature Sensor Operations",
        "description": "Operations specific to temperature sensors.",
    },
    {
        "name": "Pressure Sensor Operations",
        "description": "Operations specific to pressure sensors.",
    },
    {
        "name": "Humidity Sensor Operations",
        "description": "Operations specific to humidity sensors.",
    },
    {
        "name": "DC Motor Operations",
        "description": "Operations specific to DC motors.",
    },
    {
        "name": "Stepper Motor Operations",
        "description": "Operations specific to stepper motors.",
    },
    {
        "name": "Log Management",
        "description": "Operations for adding and viewing logs.",
    },
]

app = FastAPI(title="Simulated Device Controller API", openapi_tags=tags_metadata)


def add_record(db, logged_device_uuid: str = "", description: str = ""):
    try:
        record = LogRecord(
            uuid=uuid.uuid4(),
            user=f"{socket.gethostname()}-{socket.gethostbyname(socket.gethostname())}",
            device_uuid=logged_device_uuid,
            action=inspect.stack()[1].function,
            description=description,
            timestamp=datetime.now(),
        )
        db.add_log(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def match_device_type(db, device_uuid: str, device_type: DeviceType) -> None:
    matching_devices = [d for d in db.get_devices() if d.type == device_type]
    if device_uuid not in [d.uuid for d in matching_devices]:
        device_detail = device_type.value.lower().replace("_", " ")
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Device is not a {device_detail}",
        )
        raise HTTPException(status_code=404, detail=f"Device is not a {device_detail}")


# region general device operations


@app.get("/devices/", response_model=List[SimDevice], tags=["General Device Control"])
def list_devices(db=Depends(get_db)):
    add_record(db, description="Listed all devices")
    return db.get_devices()


@app.post("/devices/", response_model=SimDevice, tags=["General Device Control"])
def create_device(
    device: SimDevice, db=Depends(get_db), manager=Depends(get_device_manager)
):
    try:
        add_record(db, description=f"Attempting to create device {device.uuid}")
        manager.add_device(device)
        db.add_device(device)
    except ValueError as e:
        add_record(db, description=f"Failed to create device {device.uuid}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    add_record(db, description=f"Successfully created device {device.uuid}")
    return device


@app.get(
    "/devices/type/{device_type}",
    response_model=List[SimDevice],
    tags=["General Device Control"],
)
def get_devices_by_type(device_type: DeviceType, db=Depends(get_db)):
    add_record(db, description=f"Attempting to get devices by type {device_type}")
    matching_devices = [d for d in db.get_devices() if d.type == device_type]
    add_record(
        db, description=f"Found {len(matching_devices)} devices of type {device_type}"
    )
    return matching_devices


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


@app.delete("/devices/{device_uuid}", tags=["General Device Control"], status_code=204)
def delete_device(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    try:
        add_record(db, description=f"Attempting to delete device {device_uuid}")
        manager.remove_device(device_uuid)
        db.delete_device(device_uuid)
    except ValueError as e:
        add_record(db, description=f"Failed to delete device {device_uuid}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    add_record(db, description=f"Successfully deleted device {device_uuid}")


# endregion

# region device specific operations

# region all device types


@app.get("/devices/get_status", response_model=str, tags=["All Device Types"])
def get_device_status(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    try:
        add_record(db, logged_device_uuid=device_uuid, description="Getting status")
        device_status = manager.get_status(device_uuid)
        add_record(
            db, logged_device_uuid=device_uuid, description=f"Status: {device_status}"
        )
        return device_status
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to get status: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/devices/get_version", response_model=str, tags=["All Device Types"])
def get_device_version(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    try:
        add_record(db, logged_device_uuid=device_uuid, description="Getting version")
        device_version = manager.get_version(device_uuid)
        add_record(
            db, logged_device_uuid=device_uuid, description=f"Version: {device_version}"
        )
        return device_version
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to get version from device: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# region temperature sensor operations


@app.get(
    "/devices/temperature_sensor/read_temperature",
    response_model=float,
    tags=["Temperature Sensor Operations"],
)
def read_temperature(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.TEMPERATURE_SENSOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description="Reading temperature from sensor",
        )
        temperature = manager.read_temperature(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read temperature: {temperature}",
        )
        return temperature
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read temperature from sensor: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# region pressure sensor operations


@app.get(
    "/devices/pressure_sensor/read_pressure",
    response_model=float,
    tags=["Pressure Sensor Operations"],
)
def read_pressure(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.PRESSURE_SENSOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description="Reading pressure from sensor",
        )
        pressure = manager.read_pressure(device_uuid)
        add_record(
            db, logged_device_uuid=device_uuid, description=f"Read pressure: {pressure}"
        )
        return pressure
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read pressure from sensor: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# region humidity sensor operations


@app.get(
    "/devices/humidity_sensor/read_humidity",
    response_model=float,
    tags=["Humidity Sensor Operations"],
)
def read_humidity(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.HUMIDITY_SENSOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading humidity from sensor",
        )
        humidity = manager.read_humidity(device_uuid)
        add_record(
            db, logged_device_uuid=device_uuid, description=f"Read humidity: {humidity}"
        )
        return humidity
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read humidity from sensor: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# region dc motor operations


@app.get(
    "/devices/dc_motor/get_speed", response_model=float, tags=["DC Motor Operations"]
)
def get_dc_motor_speed(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.DC_MOTOR)
    try:
        add_record(
            db, logged_device_uuid=device_uuid, description=f"Reading dc motor speed"
        )
        speed = manager.get_dc_motor_speed(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read dc motor speed: {speed}",
        )
        return speed
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read dc motor speed: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/devices/dc_motor/get_direction",
    response_model=MotorDirection,
    tags=["DC Motor Operations"],
)
def get_dc_motor_direction(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.DC_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading dc motor direction",
        )
        direction = manager.get_dc_motor_direction(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read dc motor direction: {direction}",
        )
        return direction
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read dc motor direction: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/devices/dc_motor/set_speed", tags=["DC Motor Operations"], status_code=204)
def set_dc_motor_speed(
    device_uuid: str,
    speed: float,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.DC_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting dc motor speed: {speed}",
        )
        manager.set_dc_motor_speed(device_uuid, speed)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set speed for motor: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/dc_motor/set_direction", tags=["DC Motor Operations"], status_code=204
)
def set_dc_motor_direction(
    device_uuid: str,
    direction: MotorDirection,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.DC_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting dc motor direction: {direction}",
        )
        manager.set_dc_motor_direction(device_uuid, direction)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set dc motor direction: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# region stepper motor operations


@app.get(
    "/devices/stepper_motor/get_speed",
    response_model=float,
    tags=["Stepper Motor Operations"],
)
def get_stepper_motor_speed(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading stepper motor speed",
        )
        speed = manager.get_stepper_motor_speed(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read stepper motor speed: {speed}",
        )
        return speed
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read stepper motor speed: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/devices/stepper_motor/get_direction",
    response_model=MotorDirection,
    tags=["Stepper Motor Operations"],
)
def get_stepper_motor_direction(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading stepper motor direction",
        )
        direction = manager.get_stepper_motor_direction(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read stepper motor direction: {direction}",
        )
        return direction
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read stepper motor direction: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/devices/stepper_motor/get_acceleration",
    response_model=float,
    tags=["Stepper Motor Operations"],
)
def get_stepper_motor_acceleration(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading stepper motor acceleration",
        )
        acceleration = manager.get_stepper_motor_acceleration(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read stepper motor acceleration: {acceleration}",
        )
        return acceleration
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read stepper motor acceleration: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/devices/stepper_motor/get_location",
    response_model=int,
    tags=["Stepper Motor Operations"],
)
def get_stepper_motor_location(
    device_uuid: str, db=Depends(get_db), manager=Depends(get_device_manager)
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Reading stepper motor location",
        )
        location = manager.get_stepper_motor_location(device_uuid)
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Read stepper motor location: {location}",
        )
        return location
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to read stepper motor location: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/stepper_motor/set_speed",
    tags=["Stepper Motor Operations"],
    status_code=204,
)
def set_stepper_motor_speed(
    device_uuid: str,
    speed: float,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting stepper motor speed: {speed}",
        )
        manager.set_stepper_motor_speed(device_uuid, speed)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set speed for motor: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/stepper_motor/set_direction",
    tags=["Stepper Motor Operations"],
    status_code=204,
)
def set_stepper_motor_direction(
    device_uuid: str,
    direction: MotorDirection,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting stepper motor direction: {direction}",
        )
        manager.set_stepper_motor_direction(device_uuid, direction)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set stepper motor direction: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/stepper_motor/set_acceleration",
    tags=["Stepper Motor Operations"],
    status_code=204,
)
def set_stepper_motor_acceleration(
    device_uuid: str,
    acceleration: float,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting stepper motor acceleration: {acceleration}",
        )
        manager.set_stepper_motor_acceleration(device_uuid, acceleration)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set stepper motor acceleration: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/stepper_motor/set_absolute_location",
    tags=["Stepper Motor Operations"],
    status_code=204,
)
def set_stepper_motor_absolute_location(
    device_uuid: str,
    absolute_location: float,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting stepper motor absolute location: {absolute_location}",
        )
        manager.set_stepper_motor_absolute_location(device_uuid, absolute_location)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set stepper motor absolute location: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/devices/stepper_motor/set_relative_location",
    tags=["Stepper Motor Operations"],
    status_code=204,
)
def set_stepper_motor_relative_location(
    device_uuid: str,
    relative_location: float,
    db=Depends(get_db),
    manager=Depends(get_device_manager),
):
    match_device_type(db, device_uuid, DeviceType.STEPPER_MOTOR)
    try:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Setting stepper motor relative location: {relative_location}",
        )
        manager.set_stepper_motor_relative_location(device_uuid, relative_location)
    except ValueError as e:
        add_record(
            db,
            logged_device_uuid=device_uuid,
            description=f"Failed to set stepper motor relative location: {str(e)}",
        )
        raise HTTPException(status_code=404, detail=str(e))


# endregion

# endregion

# region logging operations


@app.get("/logs/", response_model=List[LogRecord], tags=["Log Management"])
def list_logs(db=Depends(get_db)):
    add_record(db, description="Listed all log records")
    return db.get_log()


@app.get("/logs/filtered", response_model=List[LogRecord], tags=["Log Management"])
def list_logs_by_time(
    start_time: datetime = "YYYY-MM-DDThh:mm:ss",
    end_time: datetime = "YYYY-MM-DDThh:mm:ss",
    db=Depends(get_db),
):
    add_record(db, description=f"Listed log records from {start_time} to {end_time}")
    matching_logs = [r for r in db.get_log() if start_time <= r.timestamp <= end_time]
    return matching_logs


@app.post("/logs/", response_model=LogRecord, tags=["Log Management"])
def create_entry(
    action: str, description: str, device_uuid: str = "", db=Depends(get_db)
):
    try:
        record = LogRecord(
            uuid=uuid.uuid4(),
            user=f"{socket.gethostname()}-{socket.gethostbyname(socket.gethostname())}",
            device_uuid=device_uuid,
            action=action,
            description=description,
            timestamp=datetime.now(),
        )
        db.add_log(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return record


# endregion
