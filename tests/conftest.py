import h5py  # type: ignore
import numpy as np
import pytest
from fastapi.testclient import TestClient

from datahub.dsr import DSRModel, read_dsr_file
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
        data[key] = np.random.randint(100)
    data["time"] = 8.58
    return data


@pytest.fixture
def opal_data_array(opal_data):
    """Pytest Fixture for random Opal data input in array format."""
    data = list(opal_data.values())
    return data


@pytest.fixture
def dsr_data(dsr_data_path):
    """Pytest Fixture for DSR data as a dictionary."""
    return read_dsr_file(dsr_data_path)


@pytest.fixture
def dsr_data_path(tmp_path):
    """The path to a temporary HDF5 file with first-time-only generated DSR data."""
    # Define the file path within the temporary directory
    file_path = tmp_path / "data.h5"

    # Check if the file already exists
    if file_path.is_file():
        # If the file exists, return its path
        return file_path

    # Otherwise, create and write data to the file
    with h5py.File(file_path, "w") as h5file:
        for field in list(DSRModel.__fields__.values()):
            if field.annotation == str:
                h5file[field.alias] = "Name or Warning"
            else:
                shape = field.field_info.extra["shape"]
                if shape[0] is None:
                    shape = (10, shape[1])
                dtype = "|S13" if field.alias == "Activity Types" else "float32"
                h5file[field.alias] = np.random.rand(*shape).astype(dtype)

    # Return the path to the file
    return file_path


@pytest.fixture
def wesim_input_data():
    """The filepath for the test version of the wesim data."""
    from datahub.wesim import read_wesim

    return read_wesim("tests/data/wesim_example.xlsx")
