from typing import List, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings
from ..schemas import Base, DatabaseDevice, DatabaseLogRecord, SimDevice

# region Real DB

engine = create_engine(
    f"{settings.database_url}"
    f"{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}",
    pool_pre_ping=True,
    echo=True,
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# region Device table operations

def add_device(db: Session, device: SimDevice):
    db_device = DatabaseDevice(
        uuid=device.uuid,
        type=device.type,
        name=device.name,
        status=device.status,
        description=device.description,
        version=device.version
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session) -> List[DatabaseDevice]:
    return db.query(DatabaseDevice).all()

def get_device_by_uuid(db: Session, uuid: str):
    device = db.query(DatabaseDevice).filter(DatabaseDevice.uuid == uuid).first()
    if not device:
        raise ValueError("Device not found")
    return device

def update_device(db: Session, uuid: str, updated_device: SimDevice):
    db_device = get_device_by_uuid(db, uuid)
    db_device.name = updated_device.name
    db_device.status = updated_device.status
    db_device.description = updated_device.description
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_device(db: Session, uuid: str):
    db_device = get_device_by_uuid(db, uuid)
    db.delete(db_device)
    db.commit()

# endregion

# region Log table operations

def add_log(db: Session, log: DatabaseLogRecord):
    db_log = DatabaseLogRecord(
        uuid=str(log.uuid),
        user=log.user,
        device_uuid=log.device_uuid,
        action=log.action,
        description=log.description,
        timestamp=log.timestamp
    )
    db.add(db_log)
    db.commit()
    return db_log

def get_logs(db: Session) -> List[DatabaseLogRecord]:
    return db.query(DatabaseLogRecord).all()

# endregion

# endregion


# region Fake DB for testing purposes

devices_table: List[Any] = []
logs_table: List[Any] = []

class FakeDBSession:
    def __init__(self):
        self.devices = devices_table
        self.logs = logs_table

    # region device table operations

    def add_device(self, device: Any):
        if device.uuid in [d.uuid for d in self.devices]:
            raise ValueError("Device with this ID already exists")
        self.devices.append(device)

    def get_devices(self):
        return self.devices
    
    def get_device_by_uuid(self, device_uuid: str):
        for device in self.devices:
            if device.uuid == device_uuid:
                return device
        raise ValueError("Device not found")

    def delete_device(self, device_uuid: str):
        for device in self.devices:
            if device.uuid == device_uuid:
                self.devices.remove(device)
                return
        raise ValueError("Device not found")

    def update_device(self, device_uuid: str, updated_device: Any):
        for index, device in enumerate(self.devices):
            if device.uuid == device_uuid:
                self.devices[index] = updated_device
                return updated_device
        raise ValueError("Device not found")

    # endregion

    # region log table operations

    def add_log(self, record: Any):
        self.logs.append(record)

    def get_log(self):
        return list(self.logs)

    def delete_log(self, record: Any):
        if record in self.logs:
            self.logs.remove(record)

    # endregion

    def commit(self):
        pass

    def close(self):
        pass

fake_db_session = FakeDBSession()

# endregion


def get_db():
    # db = fake_db_session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
