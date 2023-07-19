"""Script for running Datahub API."""
from typing import Any, Hashable

import h5py
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from . import data as dt
from . import log
from .dsr import validate_dsr_data
from .opal import OpalModel
from .wesim import get_wesim

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
    log.info("Recieved Opal data.")

    raw_data = data.dict()

    if isinstance(data, OpalArrayData):
        log.info("Array format detected.")
        append_input = raw_data["array"]
    else:
        log.info("Dict format detected.")
        append_input = raw_data

    if isinstance(append_input, list) and not len(append_input) == 45:
        message = "Array has invalid length. Expecting 45 items."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    log.info("Appending new data...")
    log.debug(f"Original Opal DataFrame:\n\n{dt.opal_df}")
    dt.opal_df.opal.append(append_input)
    log.debug(f"Updated Opal DataFrame:\n\n{dt.opal_df}")

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
    log.info("Sending Opal data...")
    log.debug(f"Query parameters:\n\nstart={start}\nend={end}\n")
    if isinstance(end, int) and end < start:
        message = "End parameter cannot be less than Start parameter."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    log.info("Filtering data...")
    log.debug(f"Current Opal DataFrame:\n\n{dt.opal_df}")
    filtered_df = dt.opal_df.loc[start:end]
    log.debug(f"Filtered Opal DataFrame:\n\n{dt.opal_df}")

    data = filtered_df.to_dict(orient="split")
    return {"data": data}


@app.post("/dsr")
def upload_dsr(file: UploadFile) -> dict[str, str | None]:
    """POST method for appending data to the DSR list.

    This takes a HDF5 file as input. Data specification can be found at
    https://github.com/ImperialCollegeLondon/gridlington-datahub/wiki/Agent-model-data#output

    \f

    Args:
        file (UploadFile): A HDF5 file with the DSR data.

    Raises:
        HTTPException: If the data is invalid

    Returns:
        dict[str, str]: dictionary with the filename
    """  # noqa: D301
    log.info("Recieved Opal data.")
    with h5py.File(file.file, "r") as h5file:
        data = {key: value[...] for key, value in h5file.items()}

    validate_dsr_data(data)

    log.info("Appending new data...")
    log.debug(f"Current DSR data length: {len(dt.dsr_data)}")
    dt.dsr_data.append(data)
    log.debug(f"Updated DSR data length: {len(dt.dsr_data)}")

    return {"filename": file.filename}


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
    log.info("Sending DSR data...")
    log.debug(f"Query parameters:\n\nstart={start}\nend={end}\n")
    if isinstance(end, int) and end < start:
        message = "End parameter cannot be less than Start parameter."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    log.info("Filtering data...")
    log.debug(f"Current DSR data length:\n\n{len(dt.dsr_data)}")
    filtered_data = dt.dsr_data[start : end + 1 if end else end]
    log.debug(f"Filtered DSR data length:\n\n{len(dt.dsr_data)}")

    return {"data": filtered_data}


@app.get("/wesim")
def get_wesim_data() -> dict[Hashable, Any]:  # type: ignore[misc]
    """GET method function for getting Wesim data as JSON.

    Returns:
        A Dict containing the Wesim Dataframes
    """
    log.info("Sending Wesim data...")
    if dt.wesim_data == {}:
        log.debug("Wesim data empty! Creating Wesim data...")
        dt.wesim_data = get_wesim()

    return {"data": dt.wesim_data}
