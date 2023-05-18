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


def test_append_opal_data():
    """Tests appending new row of Opal data to Dataframe using custom accessor."""
    from datahub.opal import OPAL_START_DATE, create_opal_frame

    df = create_opal_frame()

    data = {
        "frame": 1,
        "time": 8.58,
        "total_gen": 34.9085,
        "total_dem": 34.9055,
        "total_offwind": 16.177,
        "intra_trade": 0,
        "intra_gen": 0,
        "intra_dem": 0,
        "intra_sto": 0,
        "bm_gen": 0,
        "bm_sto": 0,
        "bm_dem": 0,
        "offwind_exp": 16192.89,
        "offwind_real": 16194.83,
        "bat_gen": -0.5713,
        "inter_gen": -0.8467,
        "offwind_gen": 16.2002,
        "onwind_gen": 9.0618,
        "other_gen": 0.2806,
        "pump_gen": -2.1328,
        "pv_gen": 0,
        "nc_gen": 0.7931,
        "hyd_gen": 0.0522,
        "gas_gen": 0.0522,
        "total_exp": 34.8373,
        "total_real": 34.8343,
        "bm_cost": 0,
        "bm_accept": 0,
        "exp_dem": 30.801,
        "real_dem": 30.801,
        "act_work": 28,
        "act_study": 5,
        "act_home": 63,
        "act_pers": 72,
        "act_shop": 0,
        "act_leis": 303,
        "act_sleep": 7230,
        "exp_ev": 3.774,
        "real_ev": 3.774,
        "ev_charge": 510,
        "ev_travel": 2,
        "ev_idle": 34,
    }

    df.opal.append(data)

    """Checks that Dataframe has 41 columns and 2 rows."""
    assert len(df.columns) == 41
    assert len(df.index) == 2

    """Checks that data appended to Dataframe matches data input."""
    keys = []
    for key in data:
        keys.append(key)

    for x in range(1, 42):
        if x == 1:
            value = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(
                data[keys[x]], unit="S"
            )
        else:
            value = data[keys[x]]

        assert df.iloc[1][x - 1] == value
