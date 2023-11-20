import numpy as np
import pandas as pd
import pytest


def test_create_opal_frame():
    """Tests creation of blank Opal Dataframes."""
    from datahub.opal import create_opal_frame, opal_headers

    df = create_opal_frame()

    # Checks that Dataframe has 41 columns and only 1 row.
    assert df.shape == (0, len(opal_headers))

    # Checks that 'Time' data is in correct dtype
    assert np.issubdtype(df["Time"].dtype, np.datetime64)

    # Checks that all other data types are int or float
    dtypes = df.dtypes
    assert ((dtypes.drop("Time") == int) | (dtypes.drop("Time") == float)).all()


def test_append_opal_data(opal_data):
    """Tests appending new row of Opal data to Dataframe using custom accessor."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame, opal_headers

    data_1 = opal_data.copy()

    data_2 = opal_data.copy()
    data_2["frame"] = 2
    data_2["time"] = data_2["time"] + 7

    data_3 = data_2.copy()
    data_3["time"] = data_3["time"] + 7

    df = create_opal_frame()

    # Checks that Dataframe has an additonal row each time .append is used.
    df.opal.append(data_1)
    assert df.shape == (1, len(opal_headers))

    df.opal.append(data_2)
    assert len(df.index) == 2

    # Checks that data appended to Dataframe matches data input.
    data_1["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_1["time"], unit="S"
    )
    data_2["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_2["time"], unit="S"
    )

    assert (df.loc[1] == list(data_1.values())[1:]).all()
    assert (df.loc[2] == list(data_2.values())[1:]).all()

    # Checks that data overwrites existing rows if they have the same index value.
    df.opal.append(data_3)
    assert len(df.index) == 2

    data_3["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_3["time"], unit="S"
    )

    assert (df.loc[2] == list(data_3.values())[1:]).all()


def test_append_validate(opal_data):
    """Tests appending new row of Opal data to Dataframe using custom accessor."""
    from datahub.opal import create_opal_frame

    # Check incorrect type
    df = create_opal_frame()
    df["Total Generation"] = df["Total Generation"].astype(str)
    with pytest.raises(AssertionError):
        df.opal.append(opal_data)

    df = create_opal_frame()
    df["Time"] = df["Time"].astype(str)
    with pytest.raises(AssertionError):
        df.opal.append(opal_data)

    df.drop("Time", axis=1, inplace=True)
    with pytest.raises(AssertionError):
        df.opal.append(opal_data)

    # Checks that Dataframe does not have an additional row
    assert len(df.index) == 0


def test_append_opal_data_array(opal_data_array):
    """Tests appending new row of Opal data using array format."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame, opal_headers

    data_1 = opal_data_array.copy()

    df = create_opal_frame()

    # Checks that Dataframe is appended to correctly with array format data.
    df.opal.append(data_1)

    assert df.shape == (1, len(opal_headers))

    data_1[1] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(data_1[1], unit="S")

    assert (df.loc[1] == data_1[1:]).all()
