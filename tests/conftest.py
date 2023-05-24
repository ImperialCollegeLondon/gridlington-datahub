import random

import pytest

from datahub.opal import opal_headers


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
    data = {}
    data["array"] = [1, 8.58]
    for x in range(43):
        data["array"].append(random.random() * random.choice([10, 100]))
    return data
