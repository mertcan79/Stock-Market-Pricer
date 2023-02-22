from pydantic import BaseModel

class Payload(BaseModel):
    symbol: str
    currency: str
    dates: str | None