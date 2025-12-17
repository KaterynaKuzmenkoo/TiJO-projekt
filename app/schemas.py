from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, Optional

class ContractType(str, Enum):
    employment = "employment"
    mandate = "mandate"
    work = "work"

class CalcRequest(BaseModel):
    gross: Annotated[float, Field(gt=0, description="Kwota brutto w PLN")]
    contract: ContractType
    age: int = Field(30, ge=0, le=120)
    is_student: bool = False
    tax_deductible_fixed: Optional[float] = Field(None, ge=0)
    tax_deductible_percent: Optional[float] = Field(None, ge=0, le=1)
    creative_50: bool = False
    youth_tax_relief: bool = False
    include_social_for_mandate: bool = True

class CalcResponse(BaseModel):
    social_total: float
    health: float
    tax_deductible_costs: float
    pit_base: float
    pit: float
    net: float