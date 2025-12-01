import pytest
from fastapi.testclient import TestClient
from sim_device_control import schemas
from sim_device_control.app import app
from sim_device_control.drivers import db

client = TestClient(app)

# override get_db dependency to use the shared fake session
from sim_device_control.drivers.db import get_db
app.dependency_overrides[get_db] = lambda: db.fake_db_session


@pytest.fixture(autouse=True)
def clear_tables():
    db.devices_table.clear()
    db.logs_table.clear()
    yield
    db.devices_table.clear()
    db.logs_table.clear()


def make_device_payload(u, name = "device-1", type_val = schemas.DeviceType.DIGITAL_PORT):
    return {
        "uuid": u,
        "type": type_val.value,
        "name": name,
        "status": "offline",
        "description": "a device",
    }


def test_list_devices_empty():
    r = client.get("/devices/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_device():
    payload = make_device_payload("uuid-100")
    r = client.post("/devices/", json=payload)
    assert r.status_code == 200
    created = r.json()
    assert created["uuid"] == "uuid-100"


def test_get_devices_by_type():
    payload = make_device_payload("uuid-101")
    client.post("/devices/", json=payload)
    r = client.get(f"/devices/{payload['type']}")
    assert r.status_code == 200
    matched = r.json()
    assert isinstance(matched, list)
    assert any(d["uuid"] == payload["uuid"] for d in matched)


def test_update_device():
    payload = make_device_payload("uuid-102")
    client.post("/devices/", json=payload)
    payload2 = make_device_payload("uuid-102", name = "renamed")
    r = client.put(f"/devices/uuid-102", json=payload2)
    assert r.status_code == 200
    assert r.json()["name"] == "renamed"


def test_delete_device():
    payload = make_device_payload("uuid-103")
    client.post("/devices/", json=payload)
    r = client.delete(f"/devices/uuid-103")
    assert r.status_code == 200
    # ensure deleted
    r = client.get("/devices/")
    assert r.status_code == 200
    assert all(d.get("uuid") != "uuid-103" for d in r.json())


def test_create_log():
    r = client.post("/logs/", params = {"action": "act", "description": "desc", "device_uuid": ""})
    assert r.status_code == 200
    log = r.json()
    assert log["action"] == "act"


def test_list_logs():
    # create a log entry then list
    client.post("/logs/", params = {"action": "act2", "description": "d", "device_uuid": ""})
    r = client.get("/logs/")
    assert r.status_code == 200
    logs = r.json()
    assert len(logs) >= 1
