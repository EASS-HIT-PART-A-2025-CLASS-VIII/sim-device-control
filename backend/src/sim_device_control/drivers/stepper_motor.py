from enum import Enum
import random
from .base.base_sensor import BaseSensorDriver
from .base.base_controller import BaseControllerDriver
from ..schemas import MotorDirection

class StepperMotorDriver(BaseSensorDriver, BaseControllerDriver):

    speed: float = 0.0
    acceleration: float = 0.0
    location: int = 0
    direction: MotorDirection = MotorDirection.FORWARD

    def __init__(self, uuid: str):
        self.uuid = uuid


    def _read_data(self):
        return {
            "speed": self.speed,
            "direction": self.direction,
            "acceleration": self.acceleration,
            "location": self.location
        }
    
    
    def _write_data(self, **kwargs):
        if 'speed' in kwargs:
            self.speed = kwargs['speed']
        if 'direction' in kwargs:
            self.direction = kwargs['direction']
        if 'acceleration' in kwargs:
            self.acceleration = kwargs['acceleration']
        if 'absolute_location' in kwargs:
            self.location = kwargs['absolute_location']
        if 'relative_location' in kwargs:
            self.location += kwargs['relative_location']


    def _get_status(self):
        return "Online"
    

    def _get_version(self):
        return "1.0.0"


    def get_speed(self):
        return self._read_data()["speed"]
    

    def get_direction(self):
        return self._read_data()["direction"]
    

    def get_acceleration(self):
        return self._read_data().get("acceleration")
    

    def get_location(self):
        return self._read_data().get("location")
    

    def set_speed(self, set_speed: float):
        self._write_data(speed = set_speed)


    def set_direction(self, set_direction: MotorDirection):
        if isinstance(set_direction, MotorDirection):
            self._write_data(direction = set_direction)
        else:
            raise ValueError("Invalid direction value")
        

    def set_acceleration(self, set_acceleration: float):
        self._write_data(acceleration = set_acceleration)


    def move_absolute(self, absolute_location: int):
        self._write_data(absolute_location = absolute_location)


    def move_relative(self, relative_location: int):
        self._write_data(relative_location = relative_location)