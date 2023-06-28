import json

import pytest
from fastapi.testclient import TestClient

from datahub import data as dt
from datahub.main import app

client = TestClient(app)
client.headers["Content-Type"] = "application/json"


@pytest.fixture(autouse=True)
def reset_dsr_data():
    """Pytest Fixture for resetting DSR data global variable."""
    dt.dsr_data = []


def test_validate_dsr_arrays(dsr_data):
    """Tests the validate_dsr_arrays function."""
    from datahub.dsr import DSRModel, validate_dsr_arrays

    dsr = DSRModel(**dsr_data)

    assert validate_dsr_arrays(dsr.dict(by_alias=True)) == []

    dsr.amount.append(1.0)
    dsr.cost.pop()

    assert validate_dsr_arrays(dsr.dict(by_alias=True)) == ["Amount", "Cost"]


def test_post_dsr_api(dsr_data):
    """Tests POSTing DSR data to API."""
    # Checks that a POST request can be successfully made
    response = client.post("/dsr", data=json.dumps(dsr_data))
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    # Checks that the DSR global variable has been updated
    assert len(dt.dsr_data) == 1


def test_post_dsr_api_invalid(dsr_data):
    """Tests POSTing DSR data to API."""
    # Checks invalid array lengths raises an error
    dsr_data["Amount"].append(1.0)
    dsr_data["Cost"][0].pop()

    response = client.post("/dsr", data=json.dumps(dsr_data))
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid size for: Amount, Cost."}

    # Checks missing fields raises an error
    dsr_data.pop("Amount")

    response = client.post("/dsr", data=json.dumps(dsr_data))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_get_dsr_api():
    """Tests DSR data GET method."""
    dt.dsr_data = [0, 1, 2, 3, 4, 5]

    response = client.get("/dsr")
    assert response.json()["data"] == dt.dsr_data

    response = client.get("/dsr?start=2")
    assert response.json()["data"] == dt.dsr_data[2:]

    response = client.get("/dsr?end=2")
    assert response.json()["data"] == dt.dsr_data[:3]

    response = client.get("/dsr?start=1&end=2")
    assert response.json()["data"] == dt.dsr_data[1:3]
