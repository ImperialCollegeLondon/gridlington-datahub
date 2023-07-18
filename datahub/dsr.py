"""This module defines the data structures for the MEDUSA Demand Simulator model."""
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, Field


class DSRModel(BaseModel):
    """Define required key values for Demand Side Response data."""

    amount: list = Field(alias="Amount", shape=(13,))
    cost: list = Field(alias="Cost", shape=(1440, 13))
    kwh_cost: list = Field(alias="kWh Cost", shape=(2,))
    activities: list = Field(alias="Activities", shape=(1440, 7))
    activities_outside_home: list = Field(
        alias="Activities Outside Home", shape=(1440, 7)
    )
    activity_types: list = Field(alias="Activity Types", shape=(7,))
    ev_id_matrix: list = Field(alias="EV ID Matrix", default=None, shape=(1440, 4329))
    ev_dt: list = Field(alias="EV DT", shape=(1440, 2))
    ev_locations: list = Field(alias="EV Locations", default=None, shape=(1440, 4329))
    ev_battery: list = Field(alias="EV Battery", default=None, shape=(1440, 4329))
    ev_state: list = Field(alias="EV State", shape=(1440, 4329))
    ev_mask: list = Field(alias="EV Mask", default=None, shape=(1440, 4329))
    baseline_ev: list = Field(alias="Baseline EV", shape=(1440,))
    baseline_non_ev: list = Field(alias="Baseline Non-EV", shape=(1440,))
    actual_ev: list = Field(alias="Actual EV", shape=(1440,))
    actual_non_ev: list = Field(alias="Actual Non-EV", shape=(1440,))
    name: str = Field(alias="Name", default="")
    warn: str = Field(alias="Warn", default="")

    class Config:
        """Allow the field variable names to be used in the API call."""

        allow_population_by_field_name = True


def validate_dsr_arrays(data: dict[str, str | NDArray]) -> list[str]:
    """Validate the shapes of the arrays in the DSR data.

    Args:
        data: The dictionary representation of the DSR Data. The keys are field aliases.
            It is generated with the data.dict(by_alias=True) where data is a DSRModel.

    Returns:
        An empty list if there are no issues. A list of the failing fields if there are.
    """
    aliases = []
    for alias, field in DSRModel.schema()["properties"].items():
        try:
            element = data[alias]
        except ValueError:
            aliases.append(alias)
            continue
        if isinstance(element, np.ndarray):
            if element.shape != field["shape"] or not np.issubdtype(
                element.dtype, np.number
            ):
                aliases.append(alias)
    return aliases
