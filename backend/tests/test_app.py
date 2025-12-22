import pytest
from fastapi.testclient import TestClient
from sim_device_control import schemas
from sim_device_control.app import app
from sim_device_control.drivers import device_manager
from sim_device_control import schemas
from sim_device_control.drivers import device_manager as dm_mod


@pytest.fixture
def client(app_with_test_db):
    return TestClient(app_with_test_db)


@pytest.fixture(autouse=True)
def clear_drivers():
    device_manager.device_manager.drivers.clear()
    yield
    device_manager.device_manager.drivers.clear()


@pytest.fixture(autouse=True)
def patch_manager_updates(monkeypatch):
    def _get_status(self, uuid: str, db):
        device = self._get_device(uuid)
        return device._get_status()

    def _get_version(self, uuid: str, db):
        device = self._get_device(uuid)
        return device._get_version()

    monkeypatch.setattr(dm_mod.DeviceManager, "get_status", _get_status)
    monkeypatch.setattr(dm_mod.DeviceManager, "get_version", _get_version)
    yield


def make_device_payload(
    u, name="device-1", type_val=schemas.DeviceType.TEMPERATURE_SENSOR
):
    return {
        "uuid": u,
        "type": type_val.value,
        "name": name,
        "status": "simulated",
        "description": "a device",
        "version": "1.0.0",
    }


# region general device operations tests


def test_list_devices_empty(client):
    r = client.get("/devices/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_device(client):
    payload = make_device_payload("uuid-100")
    r = client.post("/devices/", json=payload)
    assert r.status_code == 200
    created = r.json()
    assert created["uuid"] == "uuid-100"


def test_get_devices_by_type(client):
    payload = make_device_payload("uuid-101")
    client.post("/devices/", json=payload)
    device_type = payload["type"]
    r = client.get(f"/devices/type/{device_type}")
    assert r.status_code == 200
    matched = r.json()
    assert isinstance(matched, list)
    assert any(d["uuid"] == payload["uuid"] for d in matched)


def test_update_device_description(client):
    payload = make_device_payload("uuid-102")
    client.post("/devices/", json=payload)
    updated_description = "an updated description"
    r = client.put(
        f"/devices/update_description/uuid-102",
        params={"new_description": updated_description},
    )
    assert r.status_code == 200
    updated = r.json()
    assert updated["description"] == updated_description


def test_update_device_name(client):
    payload = make_device_payload("uuid-103")
    client.post("/devices/", json=payload)
    updated_name = "renamed-device"
    r = client.put(f"/devices/update_name/uuid-103", params={"new_name": updated_name})
    assert r.status_code == 200
    updated = r.json()
    assert updated["name"] == updated_name


# def test_update_device():
#     payload = make_device_payload("uuid-102")
#     client.post("/devices/", json = payload)
#     payload2 = make_device_payload("uuid-102", name = "renamed")
#     r = client.put(f"/devices/uuid-102", json = payload2)
#     assert r.status_code == 200
#     assert r.json()["name"] == "renamed"


def test_delete_device(client):
    payload = make_device_payload("uuid-104")
    client.post("/devices/", json=payload)
    r = client.delete(f"/devices/uuid-104")
    assert r.status_code == 204
    r = client.get("/devices/")
    assert r.status_code == 200
    assert all(d.get("uuid") != "uuid-104" for d in r.json())


# endregion

# region device specific operations tests

# region all device types tests


def test_get_device_status(client):
    payload = make_device_payload("uuid-201")
    client.post("/devices/", json=payload)
    r = client.get(f"/devices/get_status", params={"device_uuid": "uuid-201"})
    assert r.status_code == 200
    assert isinstance(r.json(), str)


def test_get_device_version(client):
    payload = make_device_payload("uuid-202")
    client.post("/devices/", json=payload)
    r = client.get(f"/devices/get_version", params={"device_uuid": "uuid-202"})
    assert r.status_code == 200
    assert isinstance(r.json(), str)


# endregion

# region temperature sensor operations tests


def test_read_temperature(client):
    payload = make_device_payload(
        "uuid-301", type_val=schemas.DeviceType.TEMPERATURE_SENSOR
    )
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/temperature_sensor/read_temperature",
        params={"device_uuid": "uuid-301"},
    )
    assert r.status_code == 200
    assert isinstance(r.json(), float)


# endregion

# region pressure sensor operations tests


def test_read_pressure(client):
    payload = make_device_payload(
        "uuid-302", type_val=schemas.DeviceType.PRESSURE_SENSOR
    )
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/pressure_sensor/read_pressure", params={"device_uuid": "uuid-302"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), float)


# endregion

# region humidity sensor operations tests


def test_read_humidity(client):
    payload = make_device_payload(
        "uuid-303", type_val=schemas.DeviceType.HUMIDITY_SENSOR
    )
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/humidity_sensor/read_humidity", params={"device_uuid": "uuid-303"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), float)


# endregion

# region dc motor operations tests


def test_read_dc_motor_speed(client):
    payload = make_device_payload("uuid-304", type_val=schemas.DeviceType.DC_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(f"/devices/dc_motor/get_speed", params={"device_uuid": "uuid-304"})
    assert r.status_code == 200
    assert isinstance(r.json(), float)


def test_read_dc_motor_direction(client):
    payload = make_device_payload("uuid-305", type_val=schemas.DeviceType.DC_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/dc_motor/get_direction", params={"device_uuid": "uuid-305"}
    )
    assert r.status_code == 200
    assert r.json() in [dir.value for dir in schemas.MotorDirection]


def test_set_dc_motor_speed(client):
    payload = make_device_payload("uuid-306", type_val=schemas.DeviceType.DC_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/dc_motor/set_speed",
        params={"device_uuid": "uuid-306", "speed": 75.0},
    )
    assert r.status_code == 204
    r2 = client.get(f"/devices/dc_motor/get_speed", params={"device_uuid": "uuid-306"})
    assert r2.status_code == 200
    assert r2.json() == 75.0


def test_set_dc_motor_direction(client):
    payload = make_device_payload("uuid-307", type_val=schemas.DeviceType.DC_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/dc_motor/set_direction",
        params={
            "device_uuid": "uuid-307",
            "direction": schemas.MotorDirection.FORWARD.value,
        },
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/dc_motor/get_direction", params={"device_uuid": "uuid-307"}
    )
    assert r2.status_code == 200
    assert r2.json() == schemas.MotorDirection.FORWARD.value


# endregion

# region stepper motor operations tests


def test_read_stepper_motor_speed(client):
    payload = make_device_payload("uuid-308", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/stepper_motor/get_speed", params={"device_uuid": "uuid-308"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), float)


def test_read_stepper_motor_direction(client):
    payload = make_device_payload("uuid-309", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/stepper_motor/get_direction", params={"device_uuid": "uuid-309"}
    )
    assert r.status_code == 200
    assert r.json() in [dir.value for dir in schemas.MotorDirection]


def test_read_stepper_motor_acceleration(client):
    payload = make_device_payload("uuid-310", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/stepper_motor/get_acceleration", params={"device_uuid": "uuid-310"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), float)


def test_read_stepper_motor_location(client):
    payload = make_device_payload("uuid-311", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.get(
        f"/devices/stepper_motor/get_location", params={"device_uuid": "uuid-311"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), int)


def test_set_stepper_motor_speed(client):
    payload = make_device_payload("uuid-312", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/stepper_motor/set_speed",
        params={"device_uuid": "uuid-312", "speed": 50.0},
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/stepper_motor/get_speed", params={"device_uuid": "uuid-312"}
    )
    assert r2.status_code == 200
    assert r2.json() == 50.0


def test_set_stepper_motor_direction(client):
    payload = make_device_payload("uuid-313", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/stepper_motor/set_direction",
        params={
            "device_uuid": "uuid-313",
            "direction": schemas.MotorDirection.BACKWARD.value,
        },
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/stepper_motor/get_direction", params={"device_uuid": "uuid-313"}
    )
    assert r2.status_code == 200
    assert r2.json() == schemas.MotorDirection.BACKWARD.value


def test_set_stepper_motor_acceleration(client):
    payload = make_device_payload("uuid-314", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/stepper_motor/set_acceleration",
        params={"device_uuid": "uuid-314", "acceleration": 10.0},
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/stepper_motor/get_acceleration", params={"device_uuid": "uuid-314"}
    )
    assert r2.status_code == 200
    assert r2.json() == 10.0


def test_move_stepper_motor_absolute(client):
    payload = make_device_payload("uuid-315", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    r = client.put(
        f"/devices/stepper_motor/set_absolute_location",
        params={"device_uuid": "uuid-315", "absolute_location": 100},
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/stepper_motor/get_location", params={"device_uuid": "uuid-315"}
    )
    assert r2.status_code == 200
    assert r2.json() == 100


def test_move_stepper_motor_relative(client):
    payload = make_device_payload("uuid-316", type_val=schemas.DeviceType.STEPPER_MOTOR)
    client.post("/devices/", json=payload)
    client.put(
        f"/devices/stepper_motor/set_absolute_location",
        params={"device_uuid": "uuid-316", "absolute_location": 50},
    )
    r = client.put(
        f"/devices/stepper_motor/set_relative_location",
        params={"device_uuid": "uuid-316", "relative_location": 25},
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/devices/stepper_motor/get_location", params={"device_uuid": "uuid-316"}
    )
    assert r2.status_code == 200
    assert r2.json() == 75


# endregion

# endregion

# region logging operations tests


def test_create_log(client):
    r = client.post(
        "/logs/", params={"action": "act", "description": "desc", "device_uuid": ""}
    )
    assert r.status_code == 200
    log = r.json()
    assert log["action"] == "act"


def test_list_logs(client):
    client.post(
        "/logs/", params={"action": "act2", "description": "d", "device_uuid": ""}
    )
    r = client.get("/logs/")
    assert r.status_code == 200
    logs = r.json()
    assert len(logs) >= 1


# endregion
