from abc import ABC, abstractmethod

class BaseControllerDriver(ABC):

    @abstractmethod
    def _write_data(self):
        raise NotImplementedError("Subclasses must implement this method")


    @abstractmethod
    def _get_status(self):
        raise NotImplementedError("Subclasses must implement this method")


    @abstractmethod
    def _get_version(self):
        raise NotImplementedError("Subclasses must implement this method")
    