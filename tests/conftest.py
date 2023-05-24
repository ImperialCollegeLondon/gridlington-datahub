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
