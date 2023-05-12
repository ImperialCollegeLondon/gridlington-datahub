"""This module defines the data structures for the Opal model."""

import pandas as pd

OPAL_START_DATE = "2035-01-22 00:00"

opal_header = [
    "Data Frame",
    "Time",
    "Total Generation",
    "Total Demand",
    "Total Offshore Generation",
    "N/A",
    "N/A",
    "N/A",
    "Intra-day Market Value",
    "Intra-day Market Generation",
    "Intra-day Market Demand",
    "Intra-day Market Storage",
    "Balancing Mechanism Generation",
    "Balancing Mechanism Storage",
    "Balancing Mechanism Demand",
    "Exp. Offshore Wind Generation",
    "Real Offshore Wind Generation",
    "Battery Generation",
    "Interconnector Power",
    "Offshore Wind Generation",
    "Onshore Wind Generation",
    "Other Generation",
    "Pump Generation",
    "PV Generation",
    "Nuclear Generation",
    "Hydro Generation",
    "Gas Generation",
    "Expected Demand",
    "Real Demand",
    "Balancing Mechanism Value",
    "Balancing Mechanism Accepted Power",
    "Expected Gridlington Demand",
    "Real Gridlington Demand",
    "Household Activity (Work)",
    "Household Activity (Study)",
    "Household Activity (Home Care)",
    "Household Activity (Personal Care)",
    "Household Activity (Shopping)",
    "Household Activity (Leisure)",
    "Household Activity (Sleep)",
    "Expected EV Charging Power",
    "Real EV Charging Power",
    "EV Status (Charging)",
    "EV Status (Travelling)",
    "EV Status (Idle)",
]

key_headers = [
    "frame",
    "time",
    "total_gen",
    "total_dem",
    "total_offwind",
    "N/A",
    "N/A",
    "N/A",
    "intra_trade",
    "intra_gen",
    "intra_dem",
    "intra_sto",
    "bm_gen",
    "bm_sto",
    "bm_dem",
    "offwind_exp",
    "offwind_real",
    "bat_gen",
    "inter_gen",
    "offwind_gen",
    "onwind_gen",
    "other_gen",
    "pump_gen",
    "pv_gen",
    "nc_gen",
    "hyd_gen",
    "gas_gen",
    "total_exp",
    "total_real",
    "bm_cost",
    "bm_accept",
    "exp_dem",
    "real_dem",
    "act_work",
    "act_study",
    "act_home",
    "act_pers",
    "act_shop",
    "act_leis",
    "act_sleep",
    "exp_ev",
    "real_ev",
    "ev_charge",
    "ev_travel",
    "ev_idle",
]


def create_opal_frame() -> pd.DataFrame:
    """Function that creates the initial pandas data frame for Opal data."""
    df = pd.DataFrame(0, index=range(1), columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE)

    return df


def append_opal_frame(data: dict[str, float]) -> pd.DataFrame:
    """Function that creates pandas data frame for Opal data to be appended."""
    data_array = []

    for item in key_headers:
        if item in data:
            data_array.append(data[item])
        elif item == "N/A":
            data_array.append(0)

    df = pd.DataFrame([data_array], columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(df["Time"], unit="S")

    return df
