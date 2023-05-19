import pandas as pd

from .opal_dummy_data import data_1, data_2, data_3

keys = []
for key in data_1:
    keys.append(key)


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


def test_append_opal_data():
    """Tests appending new row of Opal data to Dataframe using custom accessor."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame

    df = create_opal_frame()

    """Checks that Dataframe has an additonal row each time .append is used."""
    df.opal.append(data_1)
    assert len(df.columns) == 41
    assert len(df.index) == 2

    df.opal.append(data_2)
    assert len(df.index) == 3

    """Checks that data appended to Dataframe matches data input."""
    for x in range(1, 42):
        if x == 1:
            value_1 = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
                data_1[keys[x]], unit="S"
            )
            value_2 = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
                data_2[keys[x]], unit="S"
            )
        else:
            value_1 = data_1[keys[x]]
            value_2 = data_2[keys[x]]

        assert df.iloc[1][x - 1] == value_1
        assert df.iloc[2][x - 1] == value_2

    """Checks that data overwrites existing rows if they have the same index value."""
    df.opal.append(data_3)

    assert len(df.columns) == 41
    assert len(df.index) == 3

    for x in range(1, 42):
        if x == 1:
            value = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
                data_3[keys[x]], unit="S"
            )
        else:
            value = data_3[keys[x]]

        assert df.iloc[2][x - 1] == value
