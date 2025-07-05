import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.endpoints.stats import router

app = FastAPI()
app.include_router(router)

@patch("app.db.stats_orm.get_all_statistics")
def test_stats(mock_get_all_stats):
	mock_get_all_stats.return_value = {
		"Total requests to /stats": 1, "Total requests to /tickets*": 0, "Total auth failures": 0, "Total requests": 0
	}

	client = TestClient(app=app)
	response = client.get("/stats")

	assert response.status_code == 200
	assert "Total requests to /stats" in response.json()
	assert "Total auth failures" in response.json()
	assert "Total requests" in response.json()
