import json

import pandas as pd
from fastapi.testclient import TestClient

from datahub import data as dt
from datahub.main import app

client = TestClient(app)
client.headers["Content-Type"] = "application/json"


def test_post_opal_api(opal_data):
    """Tests POSTing Opal data to API."""
    post_data = json.dumps(opal_data.copy())

    """Checks that the Opal global variable can be accessed."""
    assert len(dt.opal_df.columns) == 41
    assert len(dt.opal_df.index) == 1

    """Checks that a POST request can be successfully made."""
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    """Checks that the Opal global variable has been updated."""
    assert len(dt.opal_df.index) == 2


def test_post_opal_api_array(opal_data_array):
    """Tests POSTing Opal data to API."""
    post_data = json.dumps({"array": opal_data_array.copy()})

    """Checks that a POST request can be successfully made."""
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}


def test_post_opal_api_invalid(opal_data, opal_data_array):
    """Tests error handling for invalid dict POST data."""
    invalid_data = opal_data.copy().pop("frame")
    post_data = json.dumps(invalid_data)

    """Checks that error is raised when field is missing."""
    response = client.post("/opal", data=post_data)
    assert response.status_code == 422

    """Checks that error is raised when array length is invalid."""
    invalid_data = opal_data_array.copy()
    del invalid_data[0]
    post_data = json.dumps({"array": invalid_data})

    response = client.post("/opal", data=post_data)
    assert response.status_code == 400


def test_get_opal_api():
    """Tests Opal data GET method."""
    response = client.get("/opal")
    get_data = pd.DataFrame.from_dict(response.json())

    assert get_data == dt.opal_df
