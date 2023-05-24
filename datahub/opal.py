"""This module defines the data structures for the Opal model."""
import pandas as pd

OPAL_START_DATE = "2035-01-22 00:00"

opal_headers = {
    "Time": "time",
    "Total Generation": "total_gen",
    "Total Demand": "total_dem",
    "Total Offshore Generation": "total_offwind",
    "Intra-day Market Value": "intra_trade",
    "Intra-day Market Generation": "intra_gen",
    "Intra-day Market Demand": "intra_dem",
    "Intra-day Market Storage": "intra_sto",
    "Balancing Mechanism Generation": "bm_gen",
    "Balancing Mechanism Storage": "bm_sto",
    "Balancing Mechanism Demand": "bm_dem",
    "Exp. Offshore Wind Generation": "offwind_exp",
    "Real Offshore Wind Generation": "offwind_real",
    "Battery Generation": "bat_gen",
    "Interconnector Power": "inter_gen",
    "Offshore Wind Generation": "offwind_gen",
    "Onshore Wind Generation": "onwind_gen",
    "Other Generation": "other_gen",
    "Pump Generation": "pump_gen",
    "PV Generation": "pv_gen",
    "Nuclear Generation": "nc_gen",
    "Hydro Generation": "hyd_gen",
    "Gas Generation": "gas_gen",
    "Expected Demand": "total_exp",
    "Real Demand": "total_real",
    "Balancing Mechanism Value": "bm_cost",
    "Balancing Mechanism Accepted Power": "bm_accept",
    "Expected Gridlington Demand": "exp_dem",
    "Real Gridlington Demand": "real_dem",
    "Household Activity (Work)": "act_work",
    "Household Activity (Study)": "act_study",
    "Household Activity (Home Care)": "act_home",
    "Household Activity (Personal Care)": "act_pers",
    "Household Activity (Shopping)": "act_shop",
    "Household Activity (Leisure)": "act_leis",
    "Household Activity (Sleep)": "act_sleep",
    "Expected EV Charging Power": "exp_ev",
    "Real EV Charging Power": "real_ev",
    "EV Status (Charging)": "ev_charge",
    "EV Status (Travelling)": "ev_travel",
    "EV Status (Idle)": "ev_idle",
}


@pd.api.extensions.register_dataframe_accessor("opal")
class OpalAccessor:
    """Pandas custom accessor for appending new data to Opal dataframe."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        """Initialization of dataframe.

        TODO: Add validation function.
        """
        self._obj = pandas_obj

    def append(self, data: dict[str, float]) -> None:
        """Function to append new data to existing dataframe.

        Args:
            data: The raw opal data posted to the API
        """
        row = get_opal_row(data)
        self._obj.loc[data["frame"]] = row  # type: ignore[call-overload]


def create_opal_frame() -> pd.DataFrame:
    """Function that creates the initial pandas data frame for Opal data.

    Returns:
        An initial Dataframe for the opal data with key frame 0
    """
    df = pd.DataFrame(0, index=range(1), columns=list(opal_headers.keys()))
    df["Time"] = pd.Timestamp(OPAL_START_DATE)

    return df


def get_opal_row(data: dict[str, float]) -> pd.Series:  # type: ignore[type-arg]
    """Function that creates a new row of Opal data to be appended.

    Args:
        data: The raw opal data posted to the API

    Returns:
        A pandas Series containing the new data
    """
    data_array = []

    for item in opal_headers.values():
        if item in data:
            data_array.append(data[item])

    row = pd.Series(data_array, name=data["frame"], index=list(opal_headers.keys()))
    row["Time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(row["Time"], unit="S")

    return row
