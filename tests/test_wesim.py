import pandas as pd
import pytest


@pytest.fixture
def wesim_input_data():
    """The filepath for the test version of the wesim data."""
    from datahub.wesim import read_wesim

    return read_wesim("tests/data/wesim_example.xlsx")


def test_read_wesim(wesim_input_data):
    """Test the expected DataFrames are read in."""
    assert isinstance(wesim_input_data, dict)
    expected_dfs = [
        "Capacity",
        "RES output",
        "Storage output",
        "Demand",
        "Interconnector flows",
        "Interconnector Capacity",
    ]

    for name, df in wesim_input_data.items():
        assert name in expected_dfs
        assert isinstance(df, pd.DataFrame)


def test_structure_wesim(wesim_input_data):
    """Test the Regions DataFrames are appropriately filtered and structured."""
    from datahub.wesim import structure_wesim

    df = structure_wesim(wesim_input_data["Storage output"])

    assert df.shape == (30, 4)
    assert "Battery storage" in df
    assert "Pumped hydro storage" in df
    assert (df["Hour"].unique() == [1, 2, 3, 4, 5]).all()
    for code in df["Code"].unique():
        assert code in ["LON", "MID", "NEW", "SCO", "SEW", "Total"]
    assert not df.isnull().values.any()


def test_structure_capacity(wesim_input_data):
    """Test the Capacity DataFrame is appropriately filtered and structured."""
    from datahub.wesim import structure_capacity

    df = structure_capacity(wesim_input_data["Capacity"])

    expected_columns = [
        "Code",
        "Onshore wind",
        "Offshore wind",
        "Solar PV",
        "Other RES",
        "Hydro",
        "Nuclear",
        "CCGT",
        "Gas CCS",
        "OCGT",
        "Pumped hydro storage",
        "Battery storage",
    ]

    assert df.shape == (6, 12)
    for column in expected_columns:
        assert column in df
    for code in df["Code"].unique():
        assert code in ["LON", "MID", "NEW", "SCO", "SEW", "Total"]
    assert not df.isnull().values.any()


def test_get_wesim(mocker, wesim_input_data):
    """Test get_wesim returns a dictionary with appropriate DataFrames."""
    from datahub.wesim import get_wesim

    with mocker.patch("datahub.wesim.read_wesim", return_value=wesim_input_data):
        wesim = get_wesim()

    assert wesim["Capacity"].shape == (6, 12)
    assert wesim["Regions"].shape == (30, 10)
    assert wesim["Interconnector Capacity"].shape == (4, 2)
    assert wesim["Interconnectors"].shape == (25, 3)
