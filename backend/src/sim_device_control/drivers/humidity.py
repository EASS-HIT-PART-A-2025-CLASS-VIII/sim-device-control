import random
from .base.base_sensor import BaseSensorDriver


class HumiditySensorDriver(BaseSensorDriver):
    def __init__(self, uuid: str):
        self.uuid = uuid

    def _read_data(self, **kwargs):
        mqtt_session = None
        mqtt_command = ""
        if "mqtt_session" in kwargs:
            mqtt_session = kwargs["mqtt_session"]
        if "humidity" in kwargs:
            if not mqtt_session:
                return round(random.uniform(-20.0, 50.0), 2)
            mqtt_command = "read_humidity"
        if mqtt_session:
            json_response = mqtt_session.send_command_and_wait(
                cmd_topic=f"sim-device-control/{self.uuid}/command",
                reply_topic=f"sim-device-control/{self.uuid}/response",
                command=mqtt_command,
                parameter="",
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
            return "Simulated Humidity Sensor"
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
            return "A simulated humidity sensor for testing purposes."
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

    def read_humidity(self, mqtt_session=None):
        return self._read_data(humidity=True, mqtt_session=mqtt_session)
