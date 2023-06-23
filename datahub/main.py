"""Script for running Datahub API."""
from typing import Any, Hashable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import data as dt
from .dsr import DSRModel, validate_dsr_arrays
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
def get_opal_data() -> dict[Hashable, Any]:  # type: ignore[misc]
    """GET method function for getting Opal Dataframe as JSON.

    Returns:
        A Dict of the Opal Dataframe in JSON format.

        This can be converted back to a Dataframe using the following:
        pd.DataFrame(**data)
    """
    data = dt.opal_df.to_dict(orient="split")
    return data


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
    if alias := validate_dsr_arrays(data_dict):
        raise HTTPException(
            status_code=400, detail=f"Invalid size for: {', '.join(alias)}."
        )
    dt.dsr_data.append(data_dict)

    return {"message": "Data submitted successfully."}
