from pydantic import BaseModel


class Record(BaseModel):
    color: dict[str, int]
    conductivity: float
    ph: float
    temperature: float
    tds: float
    turbidity: float
