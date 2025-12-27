import sys
import os

# Disable MQTT before importing any sim_device_control modules
os.environ["SIM_DEVICE_CONTROL_DISABLE_MQTT"] = "1"
os.environ["SIM_DEVICE_CONTROL_DISABLE_MANAGER"] = "1"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# Ensure the package in `src/` can be imported during tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
from sim_device_control.schemas import Base
from sim_device_control.drivers import db as db_driver
from sim_device_control import app as app_module
from sim_device_control.app import app as fastapi_app


# Use an in-memory SQLite database for tests and override SessionLocal
@pytest.fixture(scope="session")
def test_engine():
    # Use StaticPool so the same in-memory DB is reused across sessions/threads
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="session")
def SessionForTests(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def patch_sessionlocal(SessionForTests):
    original = db_driver.SessionLocal
    db_driver.SessionLocal = SessionForTests
    try:
        yield
    finally:
        db_driver.SessionLocal = original


@pytest.fixture
def db_session(SessionForTests):
    session = SessionForTests()
    try:
        yield session
    finally:
        session.close()


# Clear all tables before each test for isolation
@pytest.fixture(autouse=True)
def clear_db(db_session):
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture
def app_with_test_db(db_session):
    from sim_device_control.drivers.device_manager import DeviceManager

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Create a test device manager with MQTT disabled
    test_device_manager = DeviceManager(enable_mqtt=False)

    def override_get_device_manager():
        return test_device_manager

    fastapi_app.dependency_overrides[db_driver.get_db] = override_get_db
    fastapi_app.dependency_overrides[app_module.get_db] = override_get_db
    fastapi_app.dependency_overrides[app_module.get_device_manager] = (
        override_get_device_manager
    )
    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()
        test_device_manager.stop()
