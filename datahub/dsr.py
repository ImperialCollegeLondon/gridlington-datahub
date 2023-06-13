"""This module defines the data structures for the MEDUSA Demand Simulator model."""
from pydantic import BaseModel, Field


class DSR(BaseModel):
    """Define required key values for Demand Side Response data."""

    amount: list[float] = Field(alias="Amount")
    cost: list[list[float]] = Field(alias="Cost")
    kwh_cost: list[float] = Field(alias="kWh Cost")
    activities: list[list[float]] = Field(alias="Activities")
    activities_outside_home: list[list[float]] = Field(alias="Activities Outside Home")
    activity_types: list[float] = Field(alias="Activity Types")
    ev_id_matrix: list[list[float]] = Field(alias="EV ID Matrix", default=None)
    ev_dt: list[list[float]] = Field(alias="EV DT")
    ev_locations: list[list[float]] = Field(alias="EV Locations", default=None)
    ev_battery: list[list[float]] = Field(alias="EV Battery", default=None)
    ev_state: list[list[float]] = Field(alias="EV State")
    ev_mask: list[list[float]] = Field(alias="EV Mask", default=None)
    baseline_ev: list[float] = Field(alias="Baseline EV")
    baseline_non_ev: list[float] = Field(alias="Baseline Non-EV")
    actual_ev: list[float] = Field(alias="Actual EV")
    actual_non_ev: list[float] = Field(alias="Actual Non-EV")
    name: str = Field(alias="Name", default="")
    warn: str = Field(alias="Warn", default="")

    class Config:
        """Allow the field variable names to be used in the API call."""

        allow_population_by_field_name = True
