import pandas as pd


def test_create_opal_frame():
    """Tests creation of blank Opal Dataframes."""
    from datahub.opal import create_opal_frame

    df = create_opal_frame()

    """Checks that Dataframe has 41 columns and only 1 row."""
    assert len(df.columns) == 41
    assert len(df.index) == 1

    time_data = df.iloc[0]["Time"]

    """Checks that 'Time' data is in Timestamp format."""
    assert type(time_data) == pd.Timestamp
    assert time_data == pd.Timestamp("2035-01-22 00:00:00")

    """Checks that all other data values are 0."""
    float_data = df.drop(columns=["Time"]).loc[0, :].values.flatten().tolist()
    assert all(v == 0 for v in float_data)


def test_append_opal_data(opal_data):
    """Tests appending new row of Opal data to Dataframe using custom accessor."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame

    data_1 = opal_data.copy()

    data_2 = opal_data.copy()
    data_2["frame"] = 2
    data_2["time"] = data_2["time"] + 7

    data_3 = data_2.copy()
    data_3["time"] = data_3["time"] + 7

    df = create_opal_frame()

    """Checks that Dataframe has an additonal row each time .append is used."""
    df.opal.append(data_1)
    assert len(df.columns) == 41
    assert len(df.index) == 2

    df.opal.append(data_2)
    assert len(df.index) == 3

    """Checks that data appended to Dataframe matches data input."""
    data_1["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_1["time"], unit="S"
    )
    data_2["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_2["time"], unit="S"
    )

    assert (df.iloc[1, :] == list(data_1.values())[1:]).all()
    assert (df.iloc[2, :] == list(data_2.values())[1:]).all()

    """Checks that data overwrites existing rows if they have the same index value."""
    df.opal.append(data_3)
    assert len(df.index) == 3

    data_3["time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
        data_3["time"], unit="S"
    )

    assert (df.iloc[2, :] == list(data_3.values())[1:]).all()


def test_append_opal_data_array(opal_data_array):
    """Tests appending new row of Opal data using array format."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame

    data_1 = opal_data_array.copy()

    df = create_opal_frame()

    """Checks that Dataframe is appended to correctly with array format data."""
    df.opal.append(data_1)

    assert len(df.columns) == 41
    assert len(df.index) == 2

    data_1[0] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(data_1[0], unit="S")
    assert (df.iloc[1, :] == data_1[0:]).all()
