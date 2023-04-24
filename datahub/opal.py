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

opal_data = [
    1,
    8.58,
    34.9085,
    34.9055,
    16.177,
    7.8868,
    15.1744,
    3.3549,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    16192.8871,
    16194.8348,
    -0.5713,
    -0.8467,
    16.2002,
    9.0618,
    0.2806,
    -2.1328,
    0,
    0.7931,
    0.0522,
    0.0522,
    34.8373,
    34.8343,
    0,
    0,
    30.801,
    30.801,
    28,
    5,
    63,
    72,
    0,
    303,
    7230,
    3.774,
    3.774,
    510,
    2,
    34,
]


def create_opal_frame() -> pd.DataFrame:
    """Function that creates the initial pandas data frame for Opal data."""
    df = pd.DataFrame(0, index=range(1), columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE)

    return df


def append_opal_frame() -> pd.DataFrame:
    """Function that creates pandas data frame for Opal data to be appended."""
    df = pd.DataFrame([opal_data], columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(df["Time"], unit="S")

    return df
