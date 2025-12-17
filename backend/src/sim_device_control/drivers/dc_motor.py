from .base.base_sensor import BaseSensorDriver
from .base.base_controller import BaseControllerDriver
from ..schemas import MotorDirection


class DcMotorDriver(BaseSensorDriver, BaseControllerDriver):
    def __init__(self, uuid: str):
        self.uuid = uuid
        self.speed = 0.0
        self.direction = MotorDirection.FORWARD

    def _read_data(self):
        return {"speed": self.speed, "direction": self.direction}

    def _write_data(self, **kwargs):
        if "speed" in kwargs:
            self.speed = kwargs["speed"]
        if "direction" in kwargs:
            self.direction = kwargs["direction"]

    def _get_status(self):
        return "Simulation"

    def _get_version(self):
        return "1.0.0"

    def get_speed(self):
        return self._read_data()["speed"]

    def get_direction(self):
        return self._read_data()["direction"]

    def set_speed(self, set_speed: float):
        if 0.0 <= set_speed <= 100.0:
            self._write_data(speed=set_speed)
        else:
            raise ValueError("Speed must be between 0.0 and 100.0")

    def set_direction(self, set_direction: MotorDirection):
        if isinstance(set_direction, MotorDirection):
            self._write_data(direction=set_direction)
        else:
            raise ValueError("Invalid direction value")
