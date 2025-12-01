import random
from .base.base_controller import BaseSensorDriver

class TemperatureSensorDriver(BaseSensorDriver):

    def __init__(self, uuid: str):
        self.uuid = uuid


    def _read_data(self):
        return round(random.uniform(-20.0, 50.0), 2)
    

    def _get_status(self):
        return "Online"
    

    def _get_version(self):
        return "1.0.0"
    

    def read_temperature(self):
        return self._read_data()
    

    def get_status(self):
        return self._get_status()
    

    def get_version(self):
        return self._get_version()
