import json

import pandas as pd
import pytest

from datahub import data as dt


@pytest.fixture(autouse=True)
def reset_opal_data():
    """Pytest Fixture for resetting Opal data global variable."""
    dt.reset_data()


def test_post_opal_api(client, opal_data):
    """Tests POSTing Opal data to API."""
    from datahub.opal import opal_headers

    post_data = json.dumps(opal_data.copy())

    # Checks that the Opal global variable can be accessed.
    assert dt.opal_df.shape == (0, len(opal_headers))

    # Checks that a POST request can be successfully made.
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    # Checks that the Opal global variable has been updated.
    assert len(dt.opal_df.index) == 1


def test_post_opal_api_array(client, opal_data_array):
    """Tests POSTing Opal data to API in array format."""
    opal_data_array[5:5] = [1, 2, 3]
    post_data = json.dumps({"array": opal_data_array.copy()})

    # Checks that the Opal global variable has been reset.
    assert len(dt.opal_df.index) == 0

    # Checks that a POST request can be successfully made.
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data submitted successfully."}

    # Checks that the Opal global variable has been updated.
    assert len(dt.opal_df.index) == 1


def test_post_opal_api_invalid(client, opal_data, opal_data_array):
    """Tests error handling for invalid dict POST data."""
    from datahub.opal import opal_headers

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
        "detail": f"Array has invalid length. Expecting {len(opal_headers) + 4} items."
    }

    # Check that error is raised when the data on the server has been corrupted
    post_data = json.dumps(opal_data.copy())
    dt.opal_df.drop("Time", axis=1, inplace=True)

    response = client.post("/opal", data=post_data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Error with Opal data on server. Fails validation."
    }

    # Check that the Opal global variable has not been updated.
    assert len(dt.opal_df.index) == 0


def test_get_opal_api(client, opal_data):
    """Tests Opal data GET method."""
    post_data = json.dumps(opal_data.copy())
    client.post("/opal", data=post_data)

    response = client.get("/opal")

    # Converts API response to Dataframe and compares it to global variable.
    get_data = pd.DataFrame(**response.json()["data"])
    get_data["Time"] = pd.to_datetime(get_data["Time"], format="ISO8601")

    assert get_data.equals(dt.opal_df)


def test_opal_api_get_query(client, opal_data):
    """Tests the query parameters for the Opal GET method."""
    for x in range(4):
        exec(f"data_{x + 1} = opal_data.copy()")
        exec(f"data_{x + 1}['frame'] = {x + 1}")
        post_data = json.dumps(eval(f"data_{x + 1}"))
        client.post("/opal", data=post_data)

    response = client.get("/opal?start=2")
    assert response.json()["data"]["index"] == [2, 3, 4]

    response = client.get("/opal?end=2")
    assert response.json()["data"]["index"] == [1, 2]

    response = client.get("/opal?start=1&end=3")
    assert response.json()["data"]["index"] == [1, 2, 3]

    # Checks that empty data is returned when data isn't found.
    response = client.get("/opal?start=6")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()["data"]["index"]) == 0

    # Checks that an error is raised when parameters are invalid.
    response = client.get("/opal?start=3&end=1")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "End parameter cannot be less than Start parameter."
    }
