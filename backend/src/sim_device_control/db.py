from typing import List, Any

# Fake DB "tables"
devices_table: List[Any] = []
logs_table: List[Any] = []

# Fake session class
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


# Provide a database session for FastAPI dependencies
fake_db_session = FakeDBSession()

def get_db():
    db = fake_db_session
    try:
        yield db
    finally:
        db.close()