from typing import Any, List, Dict, Union, cast
from ..schemas import DeviceType, SimDevice
from .base.base_controller import BaseControllerDriver
from .base.base_sensor import BaseSensorDriver
from .temperature import TemperatureSensorDriver
from .pressure import PressureSensorDriver
from .humidity import HumiditySensorDriver
from .dc_motor import DcMotorDriver

DeviceDriverType = Union[BaseSensorDriver, BaseControllerDriver]

class DeviceManager:

    def __init__(self):
        self.drivers: List[DeviceDriverType] = []

# region internal methods

    def add_device(self, device: SimDevice):
        if device.uuid in self.drivers:
            raise ValueError(f"Device {device.uuid} already exists")
        if device.type == DeviceType.TEMPERATURE_SENSOR:
            self.drivers.append(TemperatureSensorDriver(device.uuid))
        elif device.type == DeviceType.PRESSURE_SENSOR:
            self.drivers.append(PressureSensorDriver(device.uuid))
        elif device.type == DeviceType.HUMIDITY_SENSOR:
            self.drivers.append(HumiditySensorDriver(device.uuid))
        elif device.type == DeviceType.DC_MOTOR:
            self.drivers.append(DcMotorDriver(device.uuid))


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

    def get_status(self, uuid: str):
        device = self._get_device(uuid)
        return device._get_status()
    

    def get_version(self, uuid: str):
        device = self._get_device(uuid)
        return device._get_version()

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


    def set_dc_motor_direction(self, uuid: str, direction: DeviceType):
        device = cast(DcMotorDriver, self._get_device(uuid))
        device.set_direction(direction)

# endregion

# endregion

device_manager = DeviceManager()

def get_device_manager():
    return device_manager