from typing import Any, List, Dict, Union
from .base.base_controller import BaseControllerDriver, BaseSensorDriver
from ..schemas import DeviceType, SimDevice

DeviceDriverType = Union[BaseSensorDriver, BaseControllerDriver]

class DeviceManager:
    
    def __init__(self):
        self.drivers: List[DeviceDriverType] = []

    def add_device(self, device: SimDevice):
        if device.uuid in self.drivers:
            raise ValueError(f"Device {device.uuid} already exists")
        self.drivers.append(device)

    def remove_device(self, uuid: str):
        if uuid not in self.drivers:
            raise ValueError(f"Device {uuid} does not exist")
        del self.drivers[uuid]

    def get_device(self, uuid: str):
        for device in self.drivers:
            if device.uuid == uuid:
                return device
        raise ValueError(f"Device {uuid} does not exist")

    def list_devices(self):
        return [device.uuid for device in self.drivers]