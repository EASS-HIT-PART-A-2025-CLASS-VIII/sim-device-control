from abc import ABC, abstractmethod


class BaseSensorDriver(ABC):
    @abstractmethod
    def _read_data(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _get_status(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _get_version(self):
        raise NotImplementedError("Subclasses must implement this method")
