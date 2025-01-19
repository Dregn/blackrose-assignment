"""
Pydantic model for random numbers.
Used for request validation and response formatting.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal,Optional

class ExcelRecord(BaseModel):
    user: Optional[str] = Field(None, description="Username associated with the record")
    broker: str = Field(..., description="Broker name")
    API_key: str = Field(..., description="API key of the user", alias="API key")
    API_secret: str = Field(..., description="API secret of the user", alias="API secret")
    pnl: float = Field(..., description="Profit and loss")
    margin: float = Field(..., description="Margin value")
    max_risk: float = Field(..., description="Maximum risk value")

    @validator("user", "API_key", "API_secret")
    def validate_non_empty(cls, value):
        if not value.strip():
            raise ValueError(f"{cls.__name__} must not be empty")
        return value
