import random

import pytest
from fastapi.testclient import TestClient

from datahub.main import app
from datahub.opal import opal_headers


@pytest.fixture
def client():
    """Pytest Fixture for FastAPI Test Client."""
    client = TestClient(app)
    client.headers["Content-Type"] = "application/json"

    return client


@pytest.fixture
def opal_data():
    """Pytest Fixture for random Opal data input."""
    data = {}
    data["frame"] = 1
    for key in list(opal_headers.values()):
        data[key] = random.random() * random.choice([10, 100])
    return data


@pytest.fixture
def opal_data_array():
    """Pytest Fixture for random Opal data input in array format."""
    data = [1, 8.58]
    for x in range(43):
        data.append(random.random() * random.choice([10, 100]))
    return data
