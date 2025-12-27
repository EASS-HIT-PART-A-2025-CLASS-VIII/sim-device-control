from .base.base_sensor import BaseSensorDriver
from .base.base_controller import BaseControllerDriver
from ..schemas import MotorDirection


class StepperMotorDriver(BaseSensorDriver, BaseControllerDriver):
    def __init__(self, uuid: str):
        self.uuid = uuid
        self.speed: float = 0.0
        self.acceleration: float = 0.0
        self.location: float = 0.0
        self.direction: MotorDirection = MotorDirection.FORWARD

    def _read_data(self, **kwargs):
        mqtt_session = None
        mqtt_command = ""
        if "mqtt_session" in kwargs:
            mqtt_session = kwargs["mqtt_session"]
        if "speed" in kwargs:
            if not mqtt_session:
                return self.speed
            mqtt_command = "get_speed"
        if "direction" in kwargs:
            if not mqtt_session:
                return self.direction
            mqtt_command = "get_direction"
        if "acceleration" in kwargs:
            if not mqtt_session:
                return self.acceleration
            mqtt_command = "get_acceleration"
        if "location" in kwargs:
            if not mqtt_session:
                return self.location
            mqtt_command = "get_location"
        if mqtt_session:
            json_response = mqtt_session.send_command_and_wait(
                cmd_topic=f"sim-device-control/{self.uuid}/command",
                reply_topic=f"sim-device-control/{self.uuid}/response",
                command=mqtt_command,
                parameter="",
                timeout=5,
            )
            return json_response["response"]

    def _write_data(self, **kwargs):
        mqtt_session = None
        mqtt_command = ""
        if "mqtt_session" in kwargs:
            mqtt_session = kwargs["mqtt_session"]
        if "speed" in kwargs:
            self.speed = kwargs["speed"]
            mqtt_command = "set_speed"
            mqtt_parameter = str(self.speed)
        if "direction" in kwargs:
            self.direction = kwargs["direction"]
            mqtt_command = "set_direction"
            mqtt_parameter = self.direction.value
        if "acceleration" in kwargs:
            self.acceleration = kwargs["acceleration"]
            mqtt_command = "set_acceleration"
            mqtt_parameter = str(self.acceleration)
        if "absolute_location" in kwargs:
            self.location = kwargs["absolute_location"]
            mqtt_command = "set_location_absolute"
            mqtt_parameter = str(self.location)
        if "relative_location" in kwargs:
            self.location += float(kwargs["relative_location"])
            mqtt_command = "set_location_relative"
            mqtt_parameter = str(kwargs["relative_location"])
        if mqtt_session:
            json_response = mqtt_session.send_command_and_wait(
                cmd_topic=f"sim-device-control/{self.uuid}/command",
                reply_topic=f"sim-device-control/{self.uuid}/response",
                command=mqtt_command,
                parameter=mqtt_parameter,
                timeout=5,
            )
        return json_response["response"]

    def _get_status(self, mqtt_session=None):
        if not mqtt_session:
            return "Simulation"
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="get_status",
            parameter="",
            timeout=5,
        )
        return json_response["response"]

    def _get_version(self, mqtt_session=None):
        if not mqtt_session:
            return "1.0.0"
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="get_version",
            parameter="",
            timeout=5,
        )
        return json_response["response"]

    def _get_name(self, mqtt_session=None):
        if not mqtt_session:
            return "Simulated Stepper Motor"
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="get_name",
            parameter="",
            timeout=5,
        )
        return json_response["response"]

    def _get_description(self, mqtt_session=None):
        if not mqtt_session:
            return "A simulated stepper motor for testing purposes."
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="get_description",
            parameter="",
            timeout=5,
        )
        return json_response["response"]

    def _update_name(self, new_name: str, mqtt_session=None):
        if not mqtt_session:
            return new_name
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="set_name",
            parameter=new_name,
            timeout=5,
        )
        return json_response["response"]

    def _update_description(self, new_description: str, mqtt_session=None):
        if not mqtt_session:
            return new_description
        json_response = mqtt_session.send_command_and_wait(
            cmd_topic=f"sim-device-control/{self.uuid}/command",
            reply_topic=f"sim-device-control/{self.uuid}/response",
            command="set_description",
            parameter=new_description,
            timeout=5,
        )
        return json_response["response"]

    def get_speed(self, mqtt_session=None):
        self.speed = float(self._read_data(speed=True, mqtt_session=mqtt_session))
        return self.speed

    def get_direction(self, mqtt_session=None):
        self.direction = MotorDirection(
            self._read_data(direction=True, mqtt_session=mqtt_session)
        )
        return self.direction

    def get_acceleration(self, mqtt_session=None):
        self.acceleration = float(
            self._read_data(acceleration=True, mqtt_session=mqtt_session)
        )
        return self.acceleration

    def get_location(self, mqtt_session=None):
        self.location = float(self._read_data(location=True, mqtt_session=mqtt_session))
        return self.location

    def set_speed(self, set_speed: float, mqtt_session=None):
        self._write_data(speed=set_speed, mqtt_session=mqtt_session)

    def set_direction(self, set_direction: MotorDirection, mqtt_session=None):
        if isinstance(set_direction, MotorDirection):
            self._write_data(direction=set_direction, mqtt_session=mqtt_session)
        else:
            raise ValueError("Invalid direction value")

    def set_acceleration(self, set_acceleration: float, mqtt_session=None):
        self._write_data(acceleration=set_acceleration, mqtt_session=mqtt_session)

    def move_absolute(self, absolute_location: int, mqtt_session=None):
        self._write_data(absolute_location=absolute_location, mqtt_session=mqtt_session)

    def move_relative(self, relative_location: int, mqtt_session=None):
        self._write_data(relative_location=relative_location, mqtt_session=mqtt_session)
