import h5py  # type: ignore
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


def test_post_dsr_api(dsr_data_path):
    """Tests POSTing DSR data as a hdf5 file to the API."""
    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})

    assert response.status_code == 200
    assert response.json() == {"filename": dsr_data_path.name}

    # Checks that the DSR global variable has been updated
    assert len(dt.dsr_data) == 1


def test_post_dsr_api_invalid(dsr_data_path):
    """Tests POSTing invalid DSR data to API."""
    # Check invalid array lengths raises an error
    with h5py.File(dsr_data_path, "r+") as dsr_data:
        amount = dsr_data.pop("Amount")[...]
        dsr_data["Amount"] = np.append(amount, 1.0)
        cost = dsr_data.pop("Cost")[...]
        dsr_data["Cost"] = cost[1:]

    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid size for: Amount, Cost."

    # Check missing fields raises an error
    with h5py.File(dsr_data_path, "r+") as dsr_data:
        dsr_data.pop("Amount")

    with open(dsr_data_path, "rb") as dsr_data:
        response = client.post("/dsr", files={"file": dsr_data})
        assert response.status_code == 422
        assert response.json()["detail"] == "Missing required fields: Amount."

    # Checks that the DSR global variable has not been updated
    assert len(dt.dsr_data) == 0


def test_get_dsr_api(dsr_data):
    """Tests DSR data GET method."""
    dt.dsr_data.append(dsr_data)

    response = client.get("/dsr")
    response_data = response.json()["data"][0]
    assert response_data.keys() == dsr_data.keys()
    for (key, received), expected in zip(
        response.json()["data"][0].items(), dt.dsr_data[0].values()
    ):
        if key in ["Name", "Warn"]:
            assert received == expected
            continue
        assert np.allclose(received, expected)

    # Add another entry with changed data
    new_data = dsr_data.copy()
    new_data["Name"] = "A new entry"
    dt.dsr_data.append(new_data)
    new_data = dsr_data.copy()
    new_data["Name"] = "Another new entry"
    dt.dsr_data.append(new_data)

    response = client.get("/dsr")
    assert response.json()["data"][0]["Name"] == dt.dsr_data[2]["Name"]

    # Checks index filtering
    response = client.get("/dsr?start=1")
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["Name"] == dt.dsr_data[1]["Name"]
    assert response.json()["data"][1]["Name"] == dt.dsr_data[2]["Name"]

    response = client.get("/dsr?start=0&end=1")
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["Name"] == dt.dsr_data[0]["Name"]
    assert response.json()["data"][1]["Name"] == dt.dsr_data[1]["Name"]

    # Checks column filtering
    response = client.get("/dsr?col=activities")
    assert len(response.json()["data"][0].keys()) == 1
    assert "Activities" in response.json()["data"][0].keys()

    response = client.get("/dsr?col=activity types,kwh cost")
    assert len(response.json()["data"][0].keys()) == 2
    assert "Activity Types" in response.json()["data"][0].keys()
    assert "kWh Cost" in response.json()["data"][0].keys()
