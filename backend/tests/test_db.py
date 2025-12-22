import pytest
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import sqlalchemy

from sim_device_control import schemas
from sim_device_control.drivers import db


def make_device(u: str = "dev-1"):
    return schemas.SimDevice(
        uuid=u,
        type=schemas.DeviceType.TEMPERATURE_SENSOR,
        name="test",
        status="offline",
        description="desc",
        version="1.0.0",
    )


def test_add_and_get_device(db_session):
    device = make_device("uuid-1")
    db.add_device(db_session, device)
    devices = db.get_devices(db_session)
    assert len(devices) == 1
    assert devices[0].uuid == "uuid-1"


def test_add_duplicate_raises(db_session):
    device = make_device("dup-1")
    db.add_device(db_session, device)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db.add_device(db_session, device)


def test_update_device(db_session):
    device = make_device("u-to-update")
    db.add_device(db_session, device)
    updated = make_device("u-to-update")
    updated.name = "new-name"
    db.update_device(db_session, "u-to-update", updated)
    devices = db.get_devices(db_session)
    assert devices[0].name == "new-name"


def test_delete_device(db_session):
    device = make_device("u-del")
    db.add_device(db_session, device)
    db.delete_device(db_session, "u-del")
    assert db.get_devices(db_session) == []


def test_delete_nonexistent_raises(db_session):
    with pytest.raises(ValueError):
        db.delete_device(db_session, "no-such")


def test_logs_add_and_get(db_session):
    record = schemas.LogRecord(
        uuid=uuid.uuid4(),
        user="tester",
        device_uuid="u-1",
        action="act",
        description="d",
        timestamp=datetime.now(),
    )
    db.add_log(db_session, record)
    logs = db.get_logs(db_session)
    assert len(logs) == 1
    assert logs[0].action == "act"


def test_get_db_generator_yields_session_and_closes():
    gen = db.get_db()
    sess = next(gen)
    assert isinstance(sess, Session)
    gen.close()
