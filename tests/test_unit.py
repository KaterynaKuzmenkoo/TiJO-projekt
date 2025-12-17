import pytest
from app.calculations import (
    calculate_net_salary,
    calc,
    Inputs,
    ContractType,
    CalculatorFactory,
    EmploymentCalculator,
    MandateCalculator,
    WorkCalculator,
)


def almost_equal(actual, expected, epsilon=0.01):
    """Helper function to compare floating point numbers with tolerance."""
    assert abs(actual - expected) <= epsilon, f"Expected {expected}, but got {actual}"


class TestEmploymentContract:
    """Unit tests for employment contract."""

    def test_employment_basic_calculation(self):
        """Test basic salary calculation for employment contract."""
        # Arrange
        inputs = Inputs(gross=10000, contract=ContractType.EMPLOYMENT)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        almost_equal(result.social_total, 1371.00)
        assert result.tax_deductible_costs == 250.00
        assert result.pit_base == round(10000 - 1371 - 250, 2)
        almost_equal(result.pit, result.pit_base * 0.12)
        assert result.net == round(10000 - result.social_total - result.health - result.pit, 2)

    def test_employment_with_youth_tax_relief(self):
        """Test that youth tax relief zeroes PIT for people under 26."""
        # Arrange
        inputs = Inputs(
            gross=6000,
            contract=ContractType.EMPLOYMENT,
            age=22,
            youth_tax_relief=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.pit == 0.0, "Youth under 26 with youth_tax_relief should have zero PIT"
        assert result.social_total > 0, "Social contributions should still apply"

    def test_employment_with_custom_fixed_tax_deductible(self):
        """Test employment contract with custom fixed tax deductible costs value."""
        # Arrange
        custom_tax_deductible = 111.11
        inputs = Inputs(
            gross=9000,
            contract=ContractType.EMPLOYMENT,
            tax_deductible_fixed=custom_tax_deductible
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.tax_deductible_costs == custom_tax_deductible, f"Tax deductible costs should be custom value {custom_tax_deductible}"

    def test_employment_social_contributions_percentage(self):
        """Test that social contributions are calculated at 13.71%."""
        # Arrange
        gross_amount = 5000
        inputs = Inputs(gross=gross_amount, contract=ContractType.EMPLOYMENT)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        expected_social = gross_amount * 0.1371
        almost_equal(result.social_total, expected_social)


class TestMandateContract:
    """Unit tests for contract of mandate."""

    def test_mandate_with_social_contributions(self):
        """Test mandate calculation with social contributions included."""
        # Arrange
        gross_amount = 8000
        inputs = Inputs(
            gross=gross_amount,
            contract=ContractType.MANDATE,
            include_social_for_mandate=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        expected_social = gross_amount * 0.1371
        almost_equal(result.social_total, expected_social)
        expected_tax_deductible = round((gross_amount - expected_social) * 0.2, 2)
        assert result.tax_deductible_costs == expected_tax_deductible

    def test_mandate_student_no_social_contributions(self):
        """Test that students under 26 are exempt from social contributions on mandate."""
        # Arrange
        inputs = Inputs(
            gross=4000,
            contract=ContractType.MANDATE,
            age=21,
            is_student=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.social_total == 0.0
        assert result.health == 0.0
        assert result.tax_deductible_costs == round(4000 * 0.2, 2)

    def test_mandate_with_youth_tax_relief(self):
        """Test mandate with youth tax relief for people under 26."""
        # Arrange
        inputs = Inputs(
            gross=5000,
            contract=ContractType.MANDATE,
            age=23,
            youth_tax_relief=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.pit == 0.0, "Youth tax relief should zero PIT"

    def test_mandate_with_custom_percent_tax_deductible(self):
        """Test mandate with custom tax deductible percentage."""
        # Arrange
        custom_percent = 0.33
        gross_amount = 9000
        inputs = Inputs(
            gross=gross_amount,
            contract=ContractType.MANDATE,
            tax_deductible_percent=custom_percent
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        social = gross_amount * 0.1371
        expected_tax_deductible = round((gross_amount - social) * custom_percent, 2)
        assert result.tax_deductible_costs == expected_tax_deductible

    def test_mandate_without_social_contributions(self):
        """Test mandate when social contributions are disabled."""
        # Arrange
        inputs = Inputs(
            gross=6000,
            contract=ContractType.MANDATE,
            include_social_for_mandate=False
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.social_total == 0.0
        assert result.health == 0.0


class TestWorkContract:
    """Unit tests for contract for specific work."""

    def test_work_with_default_tax_deductible(self):
        """Test work with default 20% tax deductible costs."""
        # Arrange
        gross_amount = 7000
        inputs = Inputs(gross=gross_amount, contract=ContractType.WORK)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.social_total == 0.0
        assert result.health == 0.0
        assert result.tax_deductible_costs == round(gross_amount * 0.2, 2)
        assert result.pit > 0

    def test_work_with_creative_50_percent_tax_deductible(self):
        """Test work with 50% tax deductible costs for creative work."""
        # Arrange
        gross_amount = 7000
        inputs = Inputs(
            gross=gross_amount,
            contract=ContractType.WORK,
            creative_50=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.tax_deductible_costs == round(gross_amount * 0.5, 2)

    def test_work_no_youth_tax_relief(self):
        """Test that work contract doesn't get youth tax relief."""
        # Arrange
        inputs = Inputs(
            gross=5000,
            contract=ContractType.WORK,
            age=23,
            youth_tax_relief=True
        )

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        expected_tax_base = 5000 * 0.8
        expected_pit = round(expected_tax_base * 0.12, 2)
        almost_equal(result.pit, expected_pit)


class TestEdgeCases:
    """Unit tests for edge cases and boundary conditions."""

    def test_very_low_salary_non_negative_values(self):
        """Test that very low salary still produces non-negative values."""
        # Arrange
        inputs = Inputs(gross=1, contract=ContractType.EMPLOYMENT)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.pit_base >= 0, "PIT base should not be negative"
        assert result.net > 0, "Net salary should be positive"

    def test_values_rounded_to_two_decimal_places(self):
        """Test that all monetary values are rounded to 2 decimal places."""
        # Arrange
        inputs = Inputs(gross=1234.56, contract=ContractType.EMPLOYMENT)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        for value in (result.social_total, result.health, result.tax_deductible_costs,
                      result.pit_base, result.pit, result.net):
            formatted_value = f"{value:.2f}"
            assert float(formatted_value) == value

    def test_high_salary_calculation(self):
        """Test calculation with high salary amount."""
        # Arrange
        inputs = Inputs(gross=50000, contract=ContractType.EMPLOYMENT)

        # Act
        result = calculate_net_salary(inputs)

        # Assert
        assert result.net < inputs.gross
        assert result.social_total > 0
        assert result.health > 0
        assert result.pit > 0


class TestCalculatorFactory:
    """Unit tests for the Calculator Factory pattern."""

    def test_factory_creates_employment_calculator(self):
        """Test that factory creates correct calculator for employment contract."""
        # Arrange
        inputs = Inputs(gross=5000, contract=ContractType.EMPLOYMENT)

        # Act
        calculator = CalculatorFactory.create_calculator(inputs)

        # Assert
        assert isinstance(calculator, EmploymentCalculator)

    def test_factory_creates_mandate_calculator(self):
        """Test that factory creates correct calculator for mandate contract."""
        # Arrange
        inputs = Inputs(gross=5000, contract=ContractType.MANDATE)

        # Act
        calculator = CalculatorFactory.create_calculator(inputs)

        # Assert
        assert isinstance(calculator, MandateCalculator)

    def test_factory_creates_work_calculator(self):
        """Test that factory creates correct calculator for work contract."""
        # Arrange
        inputs = Inputs(gross=5000, contract=ContractType.WORK)

        # Act
        calculator = CalculatorFactory.create_calculator(inputs)

        # Assert
        assert isinstance(calculator, WorkCalculator)


class TestBackwardCompatibility:
    """Test backward compatibility with legacy calc function."""

    def test_legacy_calc_function_works(self):
        """Test that old calc() function still works for backward compatibility."""
        # Arrange
        inputs = Inputs(gross=8000, contract=ContractType.EMPLOYMENT)

        # Act
        result = calc(inputs)

        # Assert
        assert result is not None
        assert result.net > 0
        assert hasattr(result, 'social_total')
        assert hasattr(result, 'health')
        assert hasattr(result, 'tax_deductible_costs')
        assert hasattr(result, 'pit')
