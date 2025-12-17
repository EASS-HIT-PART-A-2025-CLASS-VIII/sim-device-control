import random
from .base.base_sensor import BaseSensorDriver


class HumiditySensorDriver(BaseSensorDriver):
    def __init__(self, uuid: str):
        self.uuid = uuid

    def _read_data(self):
        return round(random.uniform(0.0, 100.0), 2)

    def _get_status(self):
        return "Simulation"

    def _get_version(self):
        return "1.0.0"

    def read_humidity(self):
        return self._read_data()
