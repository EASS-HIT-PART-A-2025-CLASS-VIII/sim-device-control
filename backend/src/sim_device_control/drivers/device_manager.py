from typing import Any, List, Dict, Union, cast
from .base.base_controller import BaseControllerDriver
from .base.base_sensor import BaseSensorDriver
from .temperature import TemperatureSensorDriver
from ..schemas import DeviceType, SimDevice

DeviceDriverType = Union[BaseSensorDriver, BaseControllerDriver]

class DeviceManager:

    def __init__(self):
        self.drivers: List[DeviceDriverType] = []


    def add_device(self, device: SimDevice):
        if device.uuid in self.drivers:
            raise ValueError(f"Device {device.uuid} already exists")
        self.drivers.append(TemperatureSensorDriver(device.uuid))


    def remove_device(self, uuid: str):
        known_devices = self.list_devices()
        if uuid not in known_devices:
            raise ValueError(f"Device {uuid} does not exist")
        device = self._get_device(uuid)
        self.drivers.remove(device)


    def _get_device(self, uuid: str):
        for device in self.drivers:
            if device.uuid == uuid:
                return device
        raise ValueError(f"Device {uuid} does not exist")


    def list_devices(self):
        return [device.uuid for device in self.drivers]
    

    def get_status(self, uuid: str):
        device = self._get_device(uuid)
        return device._get_status()
    

    def get_version(self, uuid: str):
        device = self._get_device(uuid)
        return device._get_version()
    

    def read_temperature(self, uuid: str):
        device = cast(TemperatureSensorDriver, self._get_device(uuid))
        return device.read_temperature()