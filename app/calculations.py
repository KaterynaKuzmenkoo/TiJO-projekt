from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class ContractType(str, Enum):
    ETAT = "etat"
    ZLECENIE = "zlecenie"
    DZIELO = "dzielo"


@dataclass
class Inputs:
    gross: float
    contract: ContractType
    age: int = 30
    is_student: bool = False
    kup_fixed: float | None = None
    kup_percent: float | None = None
    creative_50: bool = False
    ulga_mlodzi: bool = False
    include_social_for_zlecenie: bool = True


@dataclass
class Result:
    social_total: float
    health: float
    kup: float
    pit_base: float
    pit: float
    net: float


SOCIAL_EMPLOYEE_PERCENTAGE = 0.1371
HEALTH_PERCENTAGE = 0.09
INCOME_TAX_PERCENTAGE = 0.12
DEFAULT_TAX_DEDUCTIBLE_COSTS_ETAT = 250.0
DEFAULT_TAX_DEDUCTIBLE_COSTS_PERCENTAGE = 0.2


def _round_to_two_decimals(value: float) -> float:
    return round(value + 1e-9, 2)


class SalaryCalculator(ABC):

    def __init__(self, inputs: Inputs):
        self.inputs = inputs
        self.gross_amount = float(inputs.gross)

    @abstractmethod
    def calculate_social_contributions(self) -> float:
        pass

    @abstractmethod
    def calculate_tax_deductible_costs(self, social_contributions: float) -> float:
        pass

    def calculate_health_contribution(self, social_contributions: float) -> float:
        health_base = self.gross_amount - social_contributions
        return max(0.0, health_base) * HEALTH_PERCENTAGE

    def calculate_income_tax(self, social_contributions: float, tax_deductible_costs: float) -> float:
        tax_base = max(0.0, self.gross_amount - social_contributions - tax_deductible_costs)
        tax = tax_base * INCOME_TAX_PERCENTAGE

        if self._is_eligible_for_youth_tax_relief():
            return 0.0

        return tax

    def _is_eligible_for_youth_tax_relief(self) -> bool:
        return (self.inputs.ulga_mlodzi and
                self.inputs.age < 26 and
                self.inputs.contract in (ContractType.ETAT, ContractType.ZLECENIE))

    def calculate(self) -> Result:
        social_contributions = self.calculate_social_contributions()
        health_contribution = self.calculate_health_contribution(social_contributions)
        tax_deductible_costs = self.calculate_tax_deductible_costs(social_contributions)

        tax_base = max(0.0, self.gross_amount - social_contributions - tax_deductible_costs)
        income_tax = self.calculate_income_tax(social_contributions, tax_deductible_costs)

        net_salary = self.gross_amount - social_contributions - health_contribution - income_tax

        return Result(
            social_total=_round_to_two_decimals(social_contributions),
            health=_round_to_two_decimals(health_contribution),
            kup=_round_to_two_decimals(tax_deductible_costs),
            pit_base=_round_to_two_decimals(tax_base),
            pit=_round_to_two_decimals(income_tax),
            net=_round_to_two_decimals(net_salary),
        )


class EtatCalculator(SalaryCalculator):

    def calculate_social_contributions(self) -> float:
        return self.gross_amount * SOCIAL_EMPLOYEE_PERCENTAGE

    def calculate_tax_deductible_costs(self, social_contributions: float) -> float:
        if self.inputs.kup_fixed is not None:
            return self.inputs.kup_fixed
        return DEFAULT_TAX_DEDUCTIBLE_COSTS_ETAT

    def calculate_health_contribution(self, social_contributions: float) -> float:
        return super().calculate_health_contribution(social_contributions)


class ZlecenieCalculator(SalaryCalculator):

    def calculate_social_contributions(self) -> float:
        if not self.inputs.include_social_for_zlecenie:
            return 0.0

        if self.inputs.is_student and self.inputs.age < 26:
            return 0.0

        return self.gross_amount * SOCIAL_EMPLOYEE_PERCENTAGE

    def calculate_tax_deductible_costs(self, social_contributions: float) -> float:
        percentage = self._get_tax_deductible_percentage()
        base_for_costs = self.gross_amount - social_contributions
        return base_for_costs * percentage

    def _get_tax_deductible_percentage(self) -> float:
        if self.inputs.creative_50:
            return 0.5
        if self.inputs.kup_percent is not None:
            return self.inputs.kup_percent
        return DEFAULT_TAX_DEDUCTIBLE_COSTS_PERCENTAGE

    def calculate_health_contribution(self, social_contributions: float) -> float:
        if social_contributions > 0:
            return super().calculate_health_contribution(social_contributions)
        return 0.0


class DzieloCalculator(SalaryCalculator):

    def calculate_social_contributions(self) -> float:
        return 0.0

    def calculate_tax_deductible_costs(self, social_contributions: float) -> float:
        percentage = self._get_tax_deductible_percentage()
        return self.gross_amount * percentage

    def _get_tax_deductible_percentage(self) -> float:
        if self.inputs.creative_50:
            return 0.5
        if self.inputs.kup_percent is not None:
            return self.inputs.kup_percent
        return DEFAULT_TAX_DEDUCTIBLE_COSTS_PERCENTAGE

    def calculate_health_contribution(self, social_contributions: float) -> float:
        return 0.0

    def calculate_income_tax(self, social_contributions: float, tax_deductible_costs: float) -> float:
        tax_base = max(0.0, self.gross_amount - social_contributions - tax_deductible_costs)
        return tax_base * INCOME_TAX_PERCENTAGE


class CalculatorFactory:

    @staticmethod
    def create_calculator(inputs: Inputs) -> SalaryCalculator:
        calculators = {
            ContractType.ETAT: EtatCalculator,
            ContractType.ZLECENIE: ZlecenieCalculator,
            ContractType.DZIELO: DzieloCalculator,
        }

        calculator_class = calculators.get(inputs.contract)
        if calculator_class is None:
            raise ValueError(f"Unknown contract type: {inputs.contract}")

        return calculator_class(inputs)


def calculate_net_salary(inputs: Inputs) -> Result:
    calculator = CalculatorFactory.create_calculator(inputs)
    return calculator.calculate()


def calc(inputs: Inputs) -> Result:
    return calculate_net_salary(inputs)
