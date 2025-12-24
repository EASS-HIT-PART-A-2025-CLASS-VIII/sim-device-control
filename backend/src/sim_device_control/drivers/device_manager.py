from typing import Any, Dict, List, Union, cast
from fastapi import Depends
from .db import get_db
from . import db as db_driver
from ..schemas import DeviceType, MotorDirection, SimDevice
from .base.base_controller import BaseControllerDriver
from .base.base_sensor import BaseSensorDriver
from .temperature import TemperatureSensorDriver
from .pressure import PressureSensorDriver
from .humidity import HumiditySensorDriver
from .dc_motor import DcMotorDriver
from .stepper_motor import StepperMotorDriver


DeviceDriverType = Union[BaseSensorDriver, BaseControllerDriver]


class DeviceManager:
    def __init__(self):
        self.drivers: List[DeviceDriverType] = []
        db_gen = get_db()
        db = next(db_gen)
        try:
            devices_to_ping: List[SimDevice] = db_driver.get_devices(db)
            for device in devices_to_ping:
                try:
                    self.add_device(device)
                    device_driver = self._get_device(device.uuid)
                    status = device_driver._get_status()
                    device.status = status
                    db_driver.update_device(db, device.uuid, device)
                except ValueError:
                    self.remove_device(device.uuid)
                    db_driver.delete_device(db, device.uuid)
        finally:
            db_gen.close()

    # region internal methods

    driver_map: Dict[DeviceType, type] = {
        DeviceType.TEMPERATURE_SENSOR: TemperatureSensorDriver,
        DeviceType.PRESSURE_SENSOR: PressureSensorDriver,
        DeviceType.HUMIDITY_SENSOR: HumiditySensorDriver,
        DeviceType.DC_MOTOR: DcMotorDriver,
        DeviceType.STEPPER_MOTOR: StepperMotorDriver,
    }

    def add_device(self, device: SimDevice):
        if device.uuid in [d.uuid for d in self.drivers]:
            raise ValueError(f"Device {device.uuid} already exists")
        try:
            driver_class = self.driver_map[device.type]
        except KeyError:
            raise ValueError(f"Unsupported device type: {device.type}")
        self.drivers.append(driver_class(device.uuid))

    def remove_device(self, uuid: str):
        device_to_delete = self._get_device(uuid)
        self.drivers.remove(device_to_delete)

    def _get_device(self, uuid: str):
        for device in self.drivers:
            if device.uuid == uuid:
                return device
        raise ValueError(f"Device {uuid} does not exist")

    def list_devices(self):
        return [device.uuid for device in self.drivers]

    # endregion

    # region device operations

    # region all device types operations

    def get_status(self, uuid: str, db):
        device = self._get_device(uuid)
        status = device._get_status()
        # db_device = db.get_device_by_uuid(uuid)
        db_device = db_driver.get_device_by_uuid(db, uuid)
        db_device.status = status
        # db.update_device(uuid, updated_db_device)
        db_driver.update_device(db, uuid, db_device)
        return status

    def get_version(self, uuid: str, db):
        device = self._get_device(uuid)
        version = device._get_version()
        # db_device = db.get_device_by_uuid(uuid)
        db_device = db_driver.get_device_by_uuid(db, uuid)
        db_device.version = version
        # db.update_device(uuid, updated_db_device)
        db_driver.update_device(db, uuid, db_device)
        return version

    # endregion

    # region temperature sensor operations

    def read_temperature(self, uuid: str):
        device = cast(TemperatureSensorDriver, self._get_device(uuid))
        return device.read_temperature()

    # endregion

    # region pressure sensor operations

    def read_pressure(self, uuid: str):
        device = cast(PressureSensorDriver, self._get_device(uuid))
        return device.read_pressure()

    # endregion

    # region humidity sensor operations

    def read_humidity(self, uuid: str):
        device = cast(HumiditySensorDriver, self._get_device(uuid))
        return device.read_humidity()

    # endregion

    # region dc motor operations

    def get_dc_motor_speed(self, uuid: str):
        device = cast(DcMotorDriver, self._get_device(uuid))
        return device.get_speed()

    def get_dc_motor_direction(self, uuid: str):
        device = cast(DcMotorDriver, self._get_device(uuid))
        return device.get_direction()

    def set_dc_motor_speed(self, uuid: str, speed: float):
        device = cast(DcMotorDriver, self._get_device(uuid))
        device.set_speed(speed)

    def set_dc_motor_direction(self, uuid: str, direction: MotorDirection):
        device = cast(DcMotorDriver, self._get_device(uuid))
        device.set_direction(direction)

    # endregion

    # region stepper motor operations

    def get_stepper_motor_speed(self, uuid: str):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        return device.get_speed()

    def get_stepper_motor_direction(self, uuid: str):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        return device.get_direction()

    def get_stepper_motor_acceleration(self, uuid: str):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        return device.get_acceleration()

    def get_stepper_motor_location(self, uuid: str):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        return device.get_location()

    def set_stepper_motor_speed(self, uuid: str, speed: float):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        device.set_speed(speed)

    def set_stepper_motor_direction(self, uuid: str, direction: MotorDirection):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        device.set_direction(direction)

    def set_stepper_motor_acceleration(self, uuid: str, acceleration: float):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        device.set_acceleration(acceleration)

    def set_stepper_motor_absolute_location(self, uuid: str, location: int):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        device.move_absolute(location)

    def set_stepper_motor_relative_location(self, uuid: str, location: int):
        device = cast(StepperMotorDriver, self._get_device(uuid))
        device.move_relative(location)


# endregion

# endregion

# Provide a device manager session for FastAPI dependencies
device_manager = DeviceManager()


def get_device_manager():
    return device_manager
