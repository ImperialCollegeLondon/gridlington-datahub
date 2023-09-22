"""This module defines the data structures for the MEDUSA Demand Simulator model."""
from typing import BinaryIO

import h5py  # type: ignore
import numpy as np
from fastapi import HTTPException
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


dsr_headers = {
    field["title"]: name
    for name, field in DSRModel.schema(by_alias=False)["properties"].items()
    if name != "frame"
}


def validate_dsr_data(data: dict[str, NDArray | str]) -> None:
    """Validate the shapes of the arrays in the DSR data.

    Args:
        data: The dictionary representation of the DSR Data. The keys are field aliases.
            It is generated with the data.dict(by_alias=True) where data is a DSRModel.

    Raises:
        A HTTPException is there are mising failing fields if there are.
    """
    missing_fields = [
        field for field in DSRModel.schema()["required"] if field not in data.keys()
    ]
    if missing_fields:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required fields: {', '.join(missing_fields)}.",
        )

    aliases = []
    for alias, field in DSRModel.schema()["properties"].items():
        try:
            array = data[alias]
        except KeyError:
            if field:
                aliases.append(alias)
            continue
        if field["type"] == "array" and not isinstance(array, str):
            if array.shape != field["shape"] or not np.issubdtype(
                array.dtype, np.number
            ):
                aliases.append(alias)
    if aliases:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid size for: {', '.join(aliases)}.",
        )


def read_dsr_file(file: BinaryIO) -> dict[str, NDArray | str]:
    """Reads the HDF5 file that contains the DSR data into an in-memory dictionary.

    Args:
        file (BinaryIO): A binary file-like object referencing the HDF5 file

    Returns:
        The dictionary representation of the DSR Data.
    """
    with h5py.File(file, "r") as h5file:
        data = {
            key: (
                value[...] if key not in ["Name", "Warn"] else str(value.asstr()[...])
            )
            for key, value in h5file.items()
        }

    return data
