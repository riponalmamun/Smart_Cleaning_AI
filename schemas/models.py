from pydantic import BaseModel

class Cleaner(BaseModel):
    id: int
    name: str
    rating: float
    lat: float
    lon: float

class ScheduleInput(BaseModel):
    dates: list[str]

class PricingInput(BaseModel):
    area: str
    frequency: int
    rating: float
