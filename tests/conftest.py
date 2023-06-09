import random

import numpy as np
import pytest
from fastapi.testclient import TestClient

from datahub.dsr import DSRModel
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


@pytest.fixture
def dsr_data():
    """Pytest Fixture for random Opal data input."""
    data = {}
    for field in list(DSRModel.__fields__.values()):
        if field.annotation == str:
            data[field.alias] = "Name or Warning"
        else:
            data[field.alias] = np.random.rand(*field.field_info.extra["size"]).tolist()
    return data
