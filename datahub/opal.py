"""This module defines the data structures for the Opal model."""
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

OPAL_START_DATE = "2035-01-22 00:00"


class OpalArrayData(BaseModel):
    """Class for defining required key values for Opal data as an array."""

    array: list[float]


class OpalModel(BaseModel):
    """Define required key values for Opal data."""

    frame: int
    time: float = Field(alias="Time")
    total_gen: float = Field(alias="Total Generation")
    total_dem: float = Field(alias="Total Demand")
    total_offwind: float = Field(alias="Total Offshore Generation")
    intra_trade: float = Field(alias="Intra-day Market Value")
    intra_gen: float = Field(alias="Intra-day Market Generation")
    intra_dem: float = Field(alias="Intra-day Market Demand")
    intra_sto: float = Field(alias="Intra-day Market Storage")
    bm_gen: float = Field(alias="Balancing Mechanism Generation")
    bm_sto: float = Field(alias="Balancing Mechanism Storage")
    bm_dem: float = Field(alias="Balancing Mechanism Demand")
    offwind_exp: float = Field(alias="Exp. Offshore Wind Generation")
    offwind_real: float = Field(alias="Real Offshore Wind Generation")
    bat_gen: float = Field(alias="Battery Generation")
    inter_gen: float = Field(alias="Interconnector Power")
    offwind_gen: float = Field(alias="Offshore Wind Generation")
    onwind_gen: float = Field(alias="Onshore Wind Generation")
    other_gen: float = Field(alias="Other Generation")
    pump_gen: float = Field(alias="Pump Generation")
    pv_gen: float = Field(alias="PV Generation")
    nc_gen: float = Field(alias="Nuclear Generation")
    hyd_gen: float = Field(alias="Hydro Generation")
    gas_gen: float = Field(alias="Gas Generation")
    total_exp: float = Field(alias="Expected Demand")
    total_real: float = Field(alias="Real Demand")
    bm_cost: float = Field(alias="Balancing Mechanism Value")
    bm_accept: float = Field(alias="Balancing Mechanism Accepted Power")
    exp_dem: float = Field(alias="Expected Gridlington Demand")
    real_dem: float = Field(alias="Real Gridlington Demand")
    act_work: int = Field(alias="Household Activity (Work)")
    act_study: int = Field(alias="Household Activity (Study)")
    act_home: int = Field(alias="Household Activity (Home Care)")
    act_pers: int = Field(alias="Household Activity (Personal Care)")
    act_shop: int = Field(alias="Household Activity (Shopping)")
    act_leis: int = Field(alias="Household Activity (Leisure)")
    act_sleep: int = Field(alias="Household Activity (Sleep)")
    exp_ev: float = Field(alias="Expected EV Charging Power")
    real_ev: float = Field(alias="Real EV Charging Power")
    ev_charge: int = Field(alias="EV Status (Charging)")
    ev_travel: int = Field(alias="EV Status (Travelling)")
    ev_idle: int = Field(alias="EV Status (Idle)")
    sys_freq: float = Field(alias="System Frequency")
    dsr_cost: float = Field(alias="DSR Cost")
    dsr_amount: float = Field(alias="Accepted DSR Amount")
    dsr_charging: float = Field(alias="DSR Charging")
    bm_cost_most: float = Field(alias="Balancing Market Cost (Most)")
    bm_cost_more: float = Field(alias="Balancing Market Cost (More)")
    bm_cost_current: float = Field(alias="Balancing Market Cost (Current)")
    bm_cost_less: float = Field(alias="Balancing Market Cost (Less)")
    bm_cost_least: float = Field(alias="Balancing Market Cost (Least)")
    bm_power_most: float = Field(alias="Balancing Market Power (Most)")
    bm_power_more: float = Field(alias="Balancing Market Power (More)")
    bm_power_current: float = Field(alias="Balancing Market Power (Current)")
    bm_power_less: float = Field(alias="Balancing Market Power (Less)")
    bm_power_least: float = Field(alias="Balancing Market Power (Least)")

    class Config:
        """Allow the field variable names to be used in the API call."""

        allow_population_by_field_name = True


opal_headers: dict[str, str] = {
    field["title"]: name
    for name, field in OpalModel.schema(by_alias=False)["properties"].items()
    if name != "frame"
}


@pd.api.extensions.register_dataframe_accessor("opal")
class OpalAccessor:
    """Pandas custom accessor for appending new data to Opal dataframe."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        """Initialization of dataframe."""
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(pandas_obj: pd.DataFrame) -> None:
        """Validates the DataFrame to ensure it is usable by this accessor.

        Raises:
            AssertionError if the Dataset fails the validation.
        """
        assert set(pandas_obj.columns) == set(opal_headers.keys())
        assert pd.api.types.is_datetime64_dtype(pandas_obj.get("Time", None))
        assert all(
            np.issubdtype(dtype, np.number)
            for column, dtype in pandas_obj.dtypes.items()
            if column != "Time"
        )

    def append(self, data: dict[str, int | float] | list[int | float]) -> None:
        """Function to append new data to existing dataframe.

        Args:
            data: The raw opal data posted to the API
        """
        row = get_opal_row(data)
        if isinstance(data, list):
            data_index = data[0]
        else:
            data_index = data["frame"]

        dtypes = self._obj.dtypes
        self._obj.loc[data_index] = row.loc[data_index]  # type: ignore[call-overload]
        self._obj[:] = self._obj.astype(dtypes)[:]
        self._obj[self._obj.columns] = self._obj.astype(dtypes)[self._obj.columns]


def create_opal_frame() -> pd.DataFrame:
    """Function that creates the initial pandas data frame for Opal data.

    Returns:
        An initial Dataframe for the opal data with key frame 0
    """
    dtypes = {
        field["title"]: ("int" if field["type"] == "integer" else "float")
        for name, field in OpalModel.schema(by_alias=False)["properties"].items()
        if name != "frame"
    }
    dtypes["Time"] = "datetime64[ns]"

    df = pd.DataFrame(0, index=range(0), columns=list(opal_headers.keys()))
    df = df.astype(dtypes)

    return df


def get_opal_row(data: dict[str, int | float] | list[int | float]) -> pd.DataFrame:
    """Function that creates a new row of Opal data to be appended.

    Args:
        data: The raw opal data posted to the API

    Returns:
        A pandas Series containing the new data
    """
    if isinstance(data, dict):
        data_index = data["frame"]
        data_array = [data[item] for item in opal_headers.values()]

    else:
        data_array = data.copy()
        data_index = data_array.pop(0)

    row = pd.DataFrame(
        [data_array], index=[data_index], columns=list(opal_headers.keys())
    )
    row["Time"] = pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(row["Time"], unit="S")

    return row
