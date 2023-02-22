import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "PrismFP"
    PROJECT_VERSION: str = "1.0.0"

    API_KEY_MARKETSTACK = "33936a5a7100719d4e1e22ac4eba062a"

    API_KEY_EXCHANGERATESAPI = "UK8jUasW7UaUrMSJBIbnILRHeKyo8VPN"