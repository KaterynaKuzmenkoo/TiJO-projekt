import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Integration tests for the health check endpoint."""

    def test_health_endpoint_returns_ok_status(self, client):
        """Test that health endpoint returns successful status."""
        # Arrange
        expected_response = {"status": "ok"}

        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected_response


class TestCalculateEndpointEmployment:
    """Integration tests for employment contract calculations."""

    def test_calculate_employment_basic_request(self, client):
        """Test basic employment calculation through API."""
        # Arrange
        payload = {
            "gross": 8000,
            "contract": "employment"
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "net" in data
        assert data["net"] > 0
        assert data["net"] < payload["gross"]

    def test_calculate_employment_with_custom_tax_deductible(self, client):
        """Test employment calculation with custom fixed tax deductible costs value."""
        # Arrange
        payload = {
            "gross": 10000,
            "contract": "employment",
            "tax_deductible_fixed": 300.00
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["tax_deductible_costs"] == 300.00

    def test_calculate_employment_with_youth_relief(self, client):
        """Test employment calculation with youth tax relief."""
        # Arrange
        payload = {
            "gross": 6000,
            "contract": "employment",
            "age": 24,
            "youth_tax_relief": True
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["pit"] == 0.0

    def test_calculate_employment_returns_all_required_fields(self, client):
        """Test that employment calculation returns all required response fields."""
        # Arrange
        payload = {
            "gross": 7500,
            "contract": "employment"
        }
        required_fields = ["social_total", "health", "tax_deductible_costs", "pit_base", "pit", "net"]

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], (int, float))


class TestCalculateEndpointMandate:
    """Integration tests for contract of mandate calculations."""

    def test_calculate_mandate_with_social_contributions(self, client):
        """Test mandate calculation with social contributions."""
        # Arrange
        payload = {
            "gross": 5000,
            "contract": "mandate",
            "include_social_for_mandate": True
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["social_total"] > 0
        assert data["health"] > 0

    def test_calculate_mandate_student_exemption(self, client):
        """Test mandate for student under 26 with no social contributions."""
        # Arrange
        payload = {
            "gross": 4000,
            "contract": "mandate",
            "age": 22,
            "is_student": True
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["social_total"] == 0.0
        assert data["health"] == 0.0

    def test_calculate_mandate_with_custom_tax_deductible_percent(self, client):
        """Test mandate calculation with custom tax deductible percentage."""
        # Arrange
        payload = {
            "gross": 6000,
            "contract": "mandate",
            "tax_deductible_percent": 0.40
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        expected_tax_deductible_approx = (6000 - 6000 * 0.1371) * 0.40
        assert abs(data["tax_deductible_costs"] - expected_tax_deductible_approx) < 1.0


class TestCalculateEndpointWork:
    """Integration tests for contract for specific work calculations."""

    def test_calculate_work_basic(self, client):
        """Test basic work calculation."""
        # Arrange
        payload = {
            "gross": 5000,
            "contract": "work"
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["social_total"] == 0.0
        assert data["health"] == 0.0
        assert data["pit"] > 0

    def test_calculate_work_with_creative_50_tax_deductible(self, client):
        """Test work calculation with 50% creative tax deductible costs."""
        # Arrange
        payload = {
            "gross": 7000,
            "contract": "work",
            "creative_50": True
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["tax_deductible_costs"] == 3500.0
        assert data["pit"] >= 0


class TestValidationAndErrorHandling:
    """Integration tests for input validation and error handling."""

    def test_calculate_with_invalid_contract_type(self, client):
        """Test that invalid contract type returns validation error."""
        # Arrange
        payload = {
            "gross": 5000,
            "contract": "invalid_type"
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 422

    def test_calculate_with_negative_gross(self, client):
        """Test that negative gross amount returns validation error."""
        # Arrange
        payload = {
            "gross": -1000,
            "contract": "employment"
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 422

    def test_calculate_with_invalid_age(self, client):
        """Test that invalid age returns validation error."""
        # Arrange
        payload = {
            "gross": 5000,
            "contract": "employment",
            "age": 150
        }

        # Act
        response = client.post("/api/calculate", json=payload)

        # Assert
        assert response.status_code == 422


class TestStaticFilesAndFrontend:
    """Integration tests for static files and frontend."""

    def test_index_page_loads_successfully(self, client):
        """Test that index page is served correctly."""
        # Arrange & Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "Kalkulator wynagrodzenia netto" in response.text



    def test_static_css_file_accessible(self, client):
        """Test that CSS file is accessible."""
        # Arrange & Act
        response = client.get("/static/styles.css")

        # Assert
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_static_js_file_accessible(self, client):
        """Test that JavaScript file is accessible."""
        # Arrange & Act
        response = client.get("/static/app.js")

        # Assert
        assert response.status_code == 200
        content_type = response.headers.get("content-type", "")
        assert "javascript" in content_type or "text/plain" in content_type
