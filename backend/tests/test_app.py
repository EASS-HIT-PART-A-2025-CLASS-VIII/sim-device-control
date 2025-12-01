import pytest
from fastapi.testclient import TestClient
from sim_device_control import schemas
from sim_device_control.app import app
from sim_device_control.drivers import db, device_manager
from sim_device_control.drivers.device_manager import get_device_manager
from sim_device_control.drivers.db import get_db


app.dependency_overrides[get_db] = lambda: db.fake_db_session
app.dependency_overrides[get_device_manager] = lambda: device_manager.device_manager

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tables():
    db.devices_table.clear()
    db.logs_table.clear()
    device_manager.device_manager.drivers.clear()
    yield
    db.devices_table.clear()
    db.logs_table.clear()
    device_manager.device_manager.drivers.clear()

def make_device_payload(u, name = "device-1", type_val = schemas.DeviceType.TEMPERATURE_SENSOR):
    return {
        "uuid": u,
        "type": type_val.value,
        "name": name,
        "status": "simulated",
        "description": "a device",
    }

# region general device operations tests

def test_list_devices_empty():
    r = client.get("/devices/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_device():
    payload = make_device_payload("uuid-100")
    r = client.post("/devices/", json = payload)
    assert r.status_code == 200
    created = r.json()
    assert created["uuid"] == "uuid-100"


def test_get_devices_by_type():
    payload = make_device_payload("uuid-101")
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/type/{payload['type']}")
    assert r.status_code == 200
    matched = r.json()
    assert isinstance(matched, list)
    assert any(d["uuid"] == payload["uuid"] for d in matched)


# def test_update_device():
#     payload = make_device_payload("uuid-102")
#     client.post("/devices/", json = payload)
#     payload2 = make_device_payload("uuid-102", name = "renamed")
#     r = client.put(f"/devices/uuid-102", json = payload2)
#     assert r.status_code == 200
#     assert r.json()["name"] == "renamed"


def test_delete_device():
    payload = make_device_payload("uuid-103")
    client.post("/devices/", json = payload)
    r = client.delete(f"/devices/uuid-103")
    assert r.status_code == 200
    r = client.get("/devices/")
    assert r.status_code == 200
    assert all(d.get("uuid") != "uuid-103" for d in r.json())

# endregion

# region device specific operations tests

# region all device types tests

def test_get_device_status():
    payload = make_device_payload("uuid-201")
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/get_status", params = {"device_uuid": "uuid-201"})
    assert r.status_code == 200
    assert isinstance(r.json(), str)


def test_get_device_version():
    payload = make_device_payload("uuid-202")
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/get_version", params = {"device_uuid": "uuid-202"})
    assert r.status_code == 200
    assert isinstance(r.json(), str)

# endregion

# region temperature sensor operations tests

def test_read_temperature():
    payload = make_device_payload("uuid-301", type_val = schemas.DeviceType.TEMPERATURE_SENSOR)
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/temperature_sensor/read_temperature", params = {"device_uuid": "uuid-301"})
    assert r.status_code == 200
    assert isinstance(r.json(), float)

# endregion

# region pressure sensor operations tests

def test_read_pressure():
    payload = make_device_payload("uuid-302", type_val = schemas.DeviceType.PRESSURE_SENSOR)
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/pressure_sensor/read_pressure", params = {"device_uuid": "uuid-302"})
    assert r.status_code == 200
    assert isinstance(r.json(), float)

# endregion

# region humidity sensor operations tests

def test_read_humidity():
    payload = make_device_payload("uuid-303", type_val = schemas.DeviceType.HUMIDITY_SENSOR)
    client.post("/devices/", json = payload)
    r = client.get(f"/devices/humidity_sensor/read_humidity", params = {"device_uuid": "uuid-303"})
    assert r.status_code == 200
    assert isinstance(r.json(), float)

# endregion

# endregion

# region logging operations tests

def test_create_log():
    r = client.post("/logs/", params = {"action": "act", "description": "desc", "device_uuid": ""})
    assert r.status_code == 200
    log = r.json()
    assert log["action"] == "act"


def test_list_logs():
    client.post("/logs/", params = {"action": "act2", "description": "d", "device_uuid": ""})
    r = client.get("/logs/")
    assert r.status_code == 200
    logs = r.json()
    assert len(logs) >= 1

# endregion