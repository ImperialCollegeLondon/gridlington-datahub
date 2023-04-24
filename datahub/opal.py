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


def create_opal_frame() -> pd.DataFrame:
    """Function that creates the initial pandas data frame for Opal data."""
    df = pd.DataFrame(0, index=range(1), columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE)

    return df


def append_opal_frame(data: list[float]) -> pd.DataFrame:
    """Function that creates pandas data frame for Opal data to be appended."""
    df = pd.DataFrame([data], columns=opal_header)
    df["Time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(df["Time"], unit="S")

    return df
