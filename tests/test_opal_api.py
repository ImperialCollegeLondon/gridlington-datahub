import json

import pandas as pd
import pytest

from datahub import data as dt
from datahub.opal import create_opal_frame


@pytest.fixture(autouse=True)
def reset_opal_data():
    """Pytest Fixture for resetting Opal data global variable."""
    dt.opal_df = create_opal_frame()


def test_post_opal_api(client, opal_data):
    """Tests POSTing Opal data to API."""
    post_data = json.dumps(opal_data.copy())

    # Checks that the Opal global variable can be accessed.
    assert len(dt.opal_df.columns) == 41
    assert len(dt.opal_df.index) == 1

    # Checks that a POST request can be successfully made.
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    # Checks that the Opal global variable has been updated.
    assert len(dt.opal_df.index) == 2


def test_post_opal_api_array(client, opal_data_array):
    """Tests POSTing Opal data to API in array format."""
    post_data = json.dumps({"array": opal_data_array.copy()})

    # Checks that the Opal global variable has been reset.
    assert len(dt.opal_df.index) == 1

    # Checks that a POST request can be successfully made.
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    # Checks that the Opal global variable has been updated.
    assert len(dt.opal_df.index) == 2


def test_post_opal_api_invalid(client, opal_data, opal_data_array):
    """Tests error handling for invalid dict POST data."""
    invalid_data = opal_data.copy()
    invalid_data.pop("frame")
    post_data = json.dumps(invalid_data)

    # Checks that error is raised when field is missing.
    response = client.post("/opal", data=post_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"

    # Checks that error is raised when array length is invalid."""
    invalid_data = opal_data_array.copy()
    del invalid_data[0]
    post_data = json.dumps({"array": invalid_data})

    response = client.post("/opal", data=post_data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Array has invalid length. Expecting 45 items."
    }


def test_get_opal_api(client, opal_data):
    """Tests Opal data GET method."""
    post_data = json.dumps(opal_data.copy())
    client.post("/opal", data=post_data)

    response = client.get("/opal")

    # Converts API response to Dataframe and compares it to global variable.
    get_data = pd.DataFrame(**response.json()["data"])
    get_data["Time"] = pd.to_datetime(get_data["Time"], format="ISO8601")

    assert get_data.equals(dt.opal_df)
