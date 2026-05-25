from pydantic import BaseModel
from typing import Optional

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    total_price: float | None = None
    
    class Config:
        from_attributes = True