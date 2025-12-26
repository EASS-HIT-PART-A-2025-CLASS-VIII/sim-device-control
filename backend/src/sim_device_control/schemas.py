from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
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
    description: str
    status: str
    version: str


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


Base = declarative_base()


class DatabaseDevice(Base):
    __tablename__ = "devices"

    uuid = Column(String(225), primary_key=True)
    type = Column(SQLEnum(DeviceType), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(String(1024), nullable=True)
    version = Column(String(50), nullable=False)


class DatabaseLogRecord(Base):
    __tablename__ = "log_records"

    uuid = Column(String(225), primary_key=True)
    user = Column(String(255), nullable=False)
    device_uuid = Column(String(225))
    action = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    timestamp = Column(DateTime, default=datetime.now())
