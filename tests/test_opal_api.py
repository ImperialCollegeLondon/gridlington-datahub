import json

from fastapi.testclient import TestClient

from datahub import data as dt
from datahub.main import app

client = TestClient(app)
client.headers["Content-Type"] = "application/json"


def test_post_opal_api(opal_data):
    """Tests POSTing Opal data to API."""
    post_data = json.dumps(opal_data)

    """Checks that the Opal global variable can be accessed."""
    assert len(dt.opal_df.columns) == 41
    assert len(dt.opal_df.index) == 1

    """Checks that a POST request can be successfully made."""
    response = client.post("/opal", data=post_data)
    assert response.status_code == 200

    """Checks that the Opal global variable has been updated."""
    assert len(dt.opal_df.index) == 2
