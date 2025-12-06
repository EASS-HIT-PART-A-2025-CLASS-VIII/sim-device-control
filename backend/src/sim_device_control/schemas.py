from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid


class DeviceType(Enum):
    TEMPERATURE_SENSOR = "temperature_sensor"
    PRESSURE_SENSOR = "pressure_sensor"
    HUMIDITY_SENSOR = "humidity_sensor"
    DC_MOTOR = "dc_motor"
    STEPPER_MOTOR = "stepper_motor"
    # DIGITAL_PORT = "digital_port"
    # ANALOG_PORT = "analog_port"


class SimDevice(BaseModel):
    uuid: str
    type: DeviceType
    name: str
    status: str
    description: str


class LogRecord(BaseModel):
    uuid: uuid.UUID
    user: str
    device_uuid: str
    action: str
    description: str
    timestamp: datetime


class MotorDirection(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
