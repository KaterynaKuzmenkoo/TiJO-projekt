from pydantic import BaseModel, Field, condecimal
from enum import Enum
from typing import Optional

class ContractType(str, Enum):
    etat = "etat"
    zlecenie = "zlecenie"
    dzielo = "dzielo"

class CalcRequest(BaseModel):
    gross: condecimal(gt=0) = Field(..., description="Kwota brutto w PLN")
    contract: ContractType
    age: int = Field(30, ge=0, le=120)
    is_student: bool = False
    kup_fixed: Optional[float] = Field(None, ge=0)
    kup_percent: Optional[float] = Field(None, ge=0, le=1)
    creative_50: bool = False
    ulga_mlodzi: bool = False
    include_social_for_zlecenie: bool = True

class CalcResponse(BaseModel):
    social_total: float
    health: float
    kup: float
    pit_base: float
    pit: float
    net: float