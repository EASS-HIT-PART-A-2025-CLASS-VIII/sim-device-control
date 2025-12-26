import os
import sys
import time
import threading
from typing import Any, Dict, List, Union, cast
from fastapi import Depends
from .db import get_db
from .mqtt import MqttDriver
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
    def __init__(self, enable_mqtt: bool | None = None):
        # Default to disabling MQTT when tests are running or an opt-out flag is set
        if enable_mqtt is None:
            enable_mqtt = not (
                os.getenv("SIM_DEVICE_CONTROL_DISABLE_MQTT")
                or os.getenv("PYTEST_CURRENT_TEST")
            )
        self.enable_mqtt = enable_mqtt

        self.mqtt_session = None
        monitor_connections = None
        self._stop_event = threading.Event()
        self._drivers_lock = threading.Lock()

        if self.enable_mqtt:
            self.mqtt_session = MqttDriver("broker.hivemq.com")
            self.mqtt_session.connect()
            self.mqtt_session.start()

            def monitor_connections(mqtt_session, add_device, remove_device):
                known = {}

                while not self._stop_event.wait(1):
                    with mqtt_session._device_lock:
                        current = dict(mqtt_session.devices)

                    # Device connected
                    for device_id, device_info in current.items():
                        if device_id not in known:
                            print(f"[CONNECTED] {device_id} ({device_info['type']})")
                            try:
                                add_device(
                                    SimDevice(
                                        uuid=device_id,
                                        type=DeviceType(device_info["type"]),
                                        name=device_info["name"],
                                        description=device_info["description"],
                                        status=device_info["status"],
                                        version=device_info["version"],
                                    )
                                )
                                print(
                                    f"Added device {device_id} of type {device_info['type']}"
                                )
                            except Exception as e:
                                print(f"Failed to add device {device_id}: {e}")

                    # Device disconnected
                    for device_id in list(known):
                        if device_id not in current:
                            print(f"[DISCONNECTED] {device_id}")
                            try:
                                remove_device(device_id)
                                print(f"Removed device {device_id}")
                            except Exception as e:
                                print(f"Failed to remove device {device_id}: {e}")

                    known = current

        self.drivers: List[DeviceDriverType] = []
        db_gen = get_db()
        self.db = next(db_gen)
        try:
            devices_to_ping: List[SimDevice] = db_driver.get_devices(self.db)
            for device in devices_to_ping:
                try:
                    self.add_device(device)
                    device_driver = self._get_device(device.uuid)
                    status = device_driver._get_status()
                    device.status = status
                    db_driver.update_device(self.db, device.uuid, device)
                except ValueError:
                    self.remove_device(device.uuid)
                    db_driver.delete_device(self.db, device.uuid)
        finally:
            db_gen.close()
            if self.enable_mqtt and monitor_connections is not None:
                monitor_thread = threading.Thread(
                    target=monitor_connections,
                    args=(self.mqtt_session, self.add_device, self.remove_device),
                    daemon=True,
                )
                monitor_thread.start()

    def stop(self):
        self._stop_event.set()

    # region internal methods

    driver_map: Dict[DeviceType, type] = {
        DeviceType.TEMPERATURE_SENSOR: TemperatureSensorDriver,
        DeviceType.PRESSURE_SENSOR: PressureSensorDriver,
        DeviceType.HUMIDITY_SENSOR: HumiditySensorDriver,
        DeviceType.DC_MOTOR: DcMotorDriver,
        DeviceType.STEPPER_MOTOR: StepperMotorDriver,
    }

    def add_device(self, device: SimDevice):
        with self._drivers_lock:
            if device.uuid in [d.uuid for d in self.drivers]:
                raise ValueError(f"Device {device.uuid} already exists")
            try:
                driver_class = self.driver_map[device.type]
            except KeyError:
                raise ValueError(f"Unsupported device type: {device.type}")
            self.drivers.append(driver_class(device.uuid))
            db_driver.add_device(self.db, device)

    def remove_device(self, uuid: str):
        with self._drivers_lock:
            device_to_delete = self._get_device(uuid)
            self.drivers.remove(device_to_delete)
            db_driver.delete_device(self.db, device_to_delete.uuid)

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

    def get_status(self, uuid: str, db=None):
        active_db = db or self.db
        device = self._get_device(uuid)
        status = device._get_status()
        db_device = db_driver.get_device_by_uuid(active_db, uuid)
        db_device.status = status
        db_driver.update_device(active_db, uuid, db_device)
        return status

    def get_version(self, uuid: str, db=None):
        active_db = db or self.db
        device = self._get_device(uuid)
        version = device._get_version()
        db_device = db_driver.get_device_by_uuid(active_db, uuid)
        db_device.version = version
        db_driver.update_device(active_db, uuid, db_device)
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
_device_manager = None


def get_device_manager():
    global _device_manager
    if _device_manager is None:
        _device_manager = DeviceManager()
    return _device_manager


# Auto-start the manager (and MQTT listener) when not explicitly disabled.
# Keeps tests safe while restoring runtime behavior for incoming MQTT payloads.
if not (
    os.getenv("SIM_DEVICE_CONTROL_DISABLE_MANAGER")
    or os.getenv("PYTEST_CURRENT_TEST")
    or "pytest" in sys.modules
):
    _device_manager = DeviceManager()


def __getattr__(name):
    if name == "device_manager":
        return get_device_manager()
    raise AttributeError(name)
