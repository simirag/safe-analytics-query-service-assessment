from .conftest import client, analytic_employee_data
from ..config import settings


class TestAnalyticsAPI:
    def test_health_check(self, client):
        response = client.get("/health/")
        assert response.status_code == 200

    def test_query_analytics(self, client):
        response = client.post("/query", json={
            "group_by": "department",
            "filter": {
                "location": "New York"
            }
        })
        assert response.status_code == 200

    def test_query_analytics_invalid_group_by(self, client):
        response = client.post("/query", json={
            "group_by": "invalid_field",
            "filter": {
                "location": "New York"
            }
        })
        assert response.status_code == 200
        assert "error" in response.json()
    
    def test_query_analytics_invalid_filter(self, client):
        response = client.post("/query", json={
            "group_by": "department",
            "filter": {
                "invalid_field": "value"
            }
        })
        assert response.status_code == 200
        assert "error" in response.json()
    
    def test_query_analytics_group_by_only(self, client):
        response = client.post("/query", json={
            "group_by": "location"
        })
        assert response.status_code == 200
        # assert "data" in response.json()

    def test_query_analytics_group_by_and_filter(self, client, analytic_employee_data):
        settings.SUPPRESSED = 2
        response = client.post("/query", json={
            "group_by": "department",
            "filter": {
                "location": "San Francisco"
            }
        })
        assert response.status_code == 200
        assert response.json() == {"IT": 3}
    
    def test_query_analytics_suppressed(self, client):
        settings.SUPPRESSED = 4
        response = client.post("/query", json={
            "group_by": "department",
            "filter": {
                "location": "San Francisco"
            }
        })
        assert response.status_code == 200
        assert response.json() == {"IT": "Suppressed"}

