"""Script for running Datahub API."""
from typing import Any, Hashable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import data as dt
from .dsr import DSRModel, validate_dsr_sizes
from .opal import OpalModel

app = FastAPI()


class OpalArrayData(BaseModel):
    """Class for defining required key values for Opal data as an array."""

    array: list[float]


@app.post("/opal")
def create_opal_data(data: OpalModel | OpalArrayData) -> dict[str, str]:
    """POST method function for appending data to Opal Dataframe.

    Args:
        data: The raw opal data in either Dict or List format

    Returns:
        A Dict of the Opal data that has just been added to the Dataframe
    """
    raw_data = data.dict()

    if isinstance(data, OpalArrayData):
        append_input = raw_data["array"]
    else:
        append_input = raw_data

    # TODO: Change print statements to more formal logging
    print(dt.opal_df)

    if isinstance(append_input, list) and not len(append_input) == 45:
        raise HTTPException(
            status_code=400, detail="Array has invalid length. Expecting 45 items."
        )

    dt.opal_df.opal.append(append_input)

    print(dt.opal_df)

    return {"message": "Data submitted successfully."}


# TODO: Fix return typing annotation
@app.get("/opal")
def get_opal_data(  # type: ignore[misc]
    start: int = 0, end: int | None = None
) -> dict[Hashable, Any]:
    """GET method function for getting Opal Dataframe as JSON.

    Args:
        start: Starting index for exported Dataframe

        end: Last index that will be included in exported Dataframe

    Returns:
        A Dict containing the Opal Dataframe in JSON format

        This can be converted back to a Dataframe using the following:
        pd.DataFrame(**data)
    """
    if isinstance(end, int) and end < start:
        raise HTTPException(
            status_code=400, detail="End parameter cannot be less than Start parameter."
        )

    filtered_df = dt.opal_df.loc[start:end]

    data = filtered_df.to_dict(orient="split")
    return {"data": data}


@app.post("/dsr")
def update_dsr_data(data: DSRModel) -> dict[str, str]:
    """POST method function for appending data to the DSR list.

    Args:
        data: The DSR Data

    Returns:
        A dictionary with a success message

    Raises:
        A HTTPException if the data is invalid
    """
    data_dict = data.dict(by_alias=True)
    if alias := validate_dsr_sizes(data_dict):
        raise HTTPException(
            status_code=400, detail=f"Invalid size for: {', '.join(alias)}."
        )
    dt.dsr_data.append(data_dict)

    return {"message": "Data submitted successfully."}


@app.get("/dsr")
def get_dsr_data(  # type: ignore[misc]
    start: int = 0, end: int | None = None
) -> dict[Hashable, Any]:
    """GET method function for getting DSR data as JSON.

    Args:
        start: Starting index for exported list

        end: Last index that will be included in exported list

    Returns:
        A Dict containing the DSR list
    """
    filtered_data = dt.dsr_data[start : end + 1 if end else end]

    return {"data": filtered_data}
