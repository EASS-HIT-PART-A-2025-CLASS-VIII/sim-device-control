
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# Find .env at the backend root (2 levels up from this file)
ENV_FILE = Path(__file__).parent.parent.parent / ".env"

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=str(ENV_FILE) if ENV_FILE.exists() else None)
    
    database_url: str = "mysql+pymysql://"
    database_user: str = ""
    database_password: str = ""
    database_host: str = "db"
    database_port: int = 3306
    database_name: str = "sim_device_control"


settings = Settings()