import h5py
import numpy as np
import pytest
from fastapi.testclient import TestClient

from datahub import data as dt
from datahub.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_dsr_data():
    """Pytest Fixture for resetting DSR data global variable."""
    dt.dsr_data = []


def test_validate_dsr_arrays(dsr_data):
    """Tests the validate_dsr_arrays function."""
    from datahub.dsr import validate_dsr_arrays

    assert validate_dsr_arrays(dsr_data) == []

    dsr_data["Amount"] = np.append(dsr_data["Amount"], 1.0)
    dsr_data["Cost"] = np.delete(dsr_data["Cost"], 1)

    assert validate_dsr_arrays(dsr_data) == ["Amount", "Cost"]


def test_post_dsr_api(dsr_data_path):
    """Tests POSTing DSR data as a hdf5 file to the API."""
    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})

    assert response.status_code == 200
    assert response.json() == {"filename": dsr_data_path.name}

    # Checks that the DSR global variable has been updated
    assert len(dt.dsr_data) == 1


def test_post_dsr_api_invalid(dsr_data_path):
    """Tests POSTing DSR data to API."""
    with h5py.File(dsr_data_path, "r+") as dsr_data:
        # Checks invalid array lengths raises an error
        amount = dsr_data.pop("Amount")[...]
        dsr_data["Amount"] = np.append(amount, 1.0)
        cost = dsr_data.pop("Cost")[...]
        dsr_data["Cost"] = cost[1:]

    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid size for: Amount, Cost."}

    with h5py.File(dsr_data_path, "r+") as dsr_data:
        # Checks missing fields raises an error
        dsr_data.pop("Amount")

    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})
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
