"""This module defines the data structures for the MEDUSA Demand Simulator model."""
from typing import Any

import numpy as np
from pydantic import BaseModel, Field


class DSRModel(BaseModel):
    """Define required key values for Demand Side Response data."""

    amount: list = Field(alias="Amount", size=(13,))
    cost: list = Field(alias="Cost", size=(1440, 13))
    kwh_cost: list = Field(alias="kWh Cost", size=(2,))
    activities: list = Field(alias="Activities", size=(1440, 7))
    activities_outside_home: list = Field(
        alias="Activities Outside Home", size=(1440, 7)
    )
    activity_types: list = Field(alias="Activity Types", size=(7,))
    ev_id_matrix: list = Field(alias="EV ID Matrix", default=None, size=(1440, 4329))
    ev_dt: list = Field(alias="EV DT", size=(1440, 2))
    ev_locations: list = Field(alias="EV Locations", default=None, size=(1440, 4329))
    ev_battery: list = Field(alias="EV Battery", default=None, size=(1440, 4329))
    ev_state: list = Field(alias="EV State", size=(1440, 4329))
    ev_mask: list = Field(alias="EV Mask", default=None, size=(1440, 4329))
    baseline_ev: list = Field(alias="Baseline EV", size=(1440,))
    baseline_non_ev: list = Field(alias="Baseline Non-EV", size=(1440,))
    actual_ev: list = Field(alias="Actual EV", size=(1440,))
    actual_non_ev: list = Field(alias="Actual Non-EV", size=(1440,))
    name: str = Field(alias="Name", default="")
    warn: str = Field(alias="Warn", default="")

    class Config:
        """Allow the field variable names to be used in the API call."""

        allow_population_by_field_name = True


def validate_dsr_arrays(data: dict[str, Any]) -> list[str]:  # type: ignore[misc]
    """Validate the sizes of the arrays in the DSR data.

    Args:
        data: The dictionary representation of the DSR Data. The keys are field aliases.
            It is generated with the data.dict(by_alias=True) where data is a DSRModel.

    Returns:
        An empty list if there are no issues. A list of the failing fields if there are.
    """
    aliases = []
    for field in list(DSRModel.__fields__.values()):
        if field.annotation == list:
            array = np.array(data[field.alias])
            if (
                array.shape != field.field_info.extra["size"]
                or array.dtype != np.float64
            ):
                aliases.append(field.alias)
    return aliases
