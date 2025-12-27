from .base.base_sensor import BaseSensorDriver
from .base.base_controller import BaseControllerDriver
from ..schemas import MotorDirection


class DcMotorDriver(BaseSensorDriver, BaseControllerDriver):
    def __init__(self, uuid: str):
        self.uuid = uuid
        self.speed: float = 0.0
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
            return "Simulated DC Motor"
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
            return "A simulated DC Motor for testing purposes."
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

    def set_speed(self, set_speed: float, mqtt_session=None):
        if 0.0 <= set_speed <= 100.0:
            self._write_data(speed=set_speed, mqtt_session=mqtt_session)
        else:
            raise ValueError("Speed must be between 0.0 and 100.0")

    def set_direction(self, set_direction: MotorDirection, mqtt_session=None):
        if isinstance(set_direction, MotorDirection):
            self._write_data(direction=set_direction, mqtt_session=mqtt_session)
        else:
            raise ValueError("Invalid direction value")
