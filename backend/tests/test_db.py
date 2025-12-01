import pytest
from datetime import datetime
import uuid

from sim_device_control import schemas
from sim_device_control.drivers import db

@pytest.fixture(autouse = True)
def clear_tables():
    # ensure tables are empty before each test
    db.devices_table.clear()
    db.logs_table.clear()
    yield
    db.devices_table.clear()
    db.logs_table.clear()


def make_device(u: str = "dev-1"):
    return schemas.SimDevice(
        uuid=u,
        type=schemas.DeviceType.DIGITAL_PORT,
        name="test",
        status="offline",
        description="desc",
    )


def test_add_and_get_device():
    session = db.fake_db_session
    device = make_device("uuid-1")
    session.add_device(device)
    devices = session.get_devices()
    assert len(devices) == 1
    assert devices[0].uuid == "uuid-1"


def test_add_duplicate_raises():
    session = db.fake_db_session
    device = make_device("dup-1")
    session.add_device(device)
    with pytest.raises(ValueError):
        session.add_device(device)


def test_update_device():
    session = db.fake_db_session
    device = make_device("u-to-update")
    session.add_device(device)
    updated = make_device("u-to-update")
    updated.name = "new-name"
    session.update_device("u-to-update", updated)
    devices = session.get_devices()
    assert devices[0].name == "new-name"


def test_delete_device():
    session = db.fake_db_session
    device = make_device("u-del")
    session.add_device(device)
    session.delete_device("u-del")
    assert session.get_devices() == []


def test_delete_nonexistent_raises():
    session = db.fake_db_session
    with pytest.raises(ValueError):
        session.delete_device("no-such")


def test_logs_add_and_get():
    session = db.fake_db_session
    record = schemas.LogRecord(
        uuid=uuid.uuid4(),
        user="tester",
        device_uuid="u-1",
        action="act",
        description="d",
        timestamp=datetime.now(),
    )
    session.add_log(record)
    logs = session.get_log()
    assert len(logs) == 1
    assert logs[0].action == "act"


def test_get_db_generator_yields_session_and_closes():
    gen = db.get_db()
    sess = next(gen)
    assert sess is db.fake_db_session
    gen.close()
