import json
import uuid
import threading
import time
import paho.mqtt.client as mqtt


class MqttDriver:
    def __init__(self, broker_address, port=1883):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.port = port

        self._handlers = {}
        self._pending_requests = {}

        self.devices = {}
        self._device_lock = threading.Lock()

        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect

    def connect(self):
        self.client.connect(self.broker_address, self.port)

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code", rc)
        for topic in self._handlers:
            client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload_raw = msg.payload.decode()

        # ---- Device connection handling ----
        if topic == "sim-device-control/connections":
            payload = json.loads(payload_raw)
            device_id = payload.get("device_id")
            device_type = payload.get("device_type")
            device_name = payload.get("name")
            device_description = payload.get("description")
            device_status = payload.get("status")
            device_version = payload.get("version")
            action = payload.get("action")

            if not device_id or not action:
                return

            with self._device_lock:
                if action == "connected":
                    self.devices[device_id] = {
                        "type": device_type,
                        "name": device_name,
                        "description": device_description,
                        "status": device_status,
                        "version": device_version,
                    }
                elif action == "disconnected":
                    self.devices.pop(device_id, None)
            return

        # ---- Device responses handling ----
        payload = json.loads(payload_raw)

        request_id = payload.get("id")
        if request_id in self._pending_requests:
            event, storage = self._pending_requests[request_id]
            storage["response"] = payload
            event.set()
            return

        handler = self._handlers.get(topic)
        if handler:
            handler(topic, payload)

    def subscribe(self, topic, handler=None, qos=1):
        if handler:
            self._handlers[topic] = handler
        self.client.subscribe(topic, qos=qos)

    def publish(self, topic, message, qos=1, retain=False):
        self.client.publish(topic, json.dumps(message), qos=qos, retain=retain)

    def send_command_and_wait(
        self, cmd_topic, reply_topic, command, parameter, timeout=5
    ):
        request_id = str(uuid.uuid4())
        event = threading.Event()
        response_holder = {}

        self._pending_requests[request_id] = (event, response_holder)

        self.subscribe(reply_topic)

        command_payload = {
            "id": request_id,
            "command": command,
            "parameter": parameter,
        }

        self.publish(cmd_topic, command_payload)

        if not event.wait(timeout):
            del self._pending_requests[request_id]
            raise TimeoutError("No reply received")

        response = response_holder["response"]
        del self._pending_requests[request_id]
        return response

    def start(self):
        self.subscribe("sim-device-control/connections")
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
