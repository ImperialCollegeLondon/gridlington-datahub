"""Script for running Datahub API."""

import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import ORJSONResponse

from . import data as dt
from . import log
from .dsr import dsr_headers, read_dsr_file, validate_dsr_data
from .opal import OpalArrayData, OpalModel, opal_headers
from .wesim import get_wesim

app = FastAPI(
    title="Gridlington DataHub",
)


@app.post("/opal")
def create_opal_data(data: OpalModel | OpalArrayData) -> dict[str, str]:
    """POST method function for appending data to Opal Dataframe.

    It takes the Opal data as a dictionary or list in JSON format and updates the data
    held in the datahub and returns a success message.

    \f

    Args:
        data: The raw opal data in either Dict or List format

    Returns:
        A Dict of the Opal data that has just been added to the Dataframe
    """  # noqa: D301
    log.info("Received Opal data.")

    raw_data = data.dict()

    if isinstance(data, OpalArrayData):
        log.info("Array format detected.")
        append_input = raw_data["array"]
        del append_input[5:8]

        if len(append_input) != len(opal_headers) + 1:
            message = (
                f"Array has invalid length. Expecting {len(opal_headers) + 4} items."
            )
            log.error(message)
            raise HTTPException(status_code=400, detail=message)

    else:
        log.info("Dict format detected.")
        append_input = raw_data

    log.info("Appending new data...")
    log.debug(f"Original Opal DataFrame:\n\n{dt.opal_df}")
    try:
        dt.opal_df.opal.append(append_input)
    except AssertionError:
        message = "Error with Opal data on server. Fails validation."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    log.debug(f"Updated Opal DataFrame:\n\n{dt.opal_df}")

    return {"message": "Data submitted successfully."}


@app.get("/opal")
def get_opal_data(
    start: int = 0, end: int | None = None
) -> dict[str, dict]:  # type: ignore[type-arg]
    """GET method function for getting Opal Dataframe as JSON.

    It takes optional query parameters of:
    - `start`: Starting index for exported Dataframe
    - `end`: Last index that will be included in exported Dataframe

    And returns a dictionary containing the Opal Dataframe in JSON format.

    This can be converted back to a DataFrame using the following:
    `pd.DataFrame(**data)`

    \f

    Args:
        start: Starting index for exported Dataframe
        end: Last index that will be included in exported Dataframe

    Returns:
        A Dict containing the Opal DataFrame in JSON format
    """  # noqa: D301
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

    This takes a HDF5 file as input. This file has a flat structure, with each dataset
    available at the top level.

    The required fields (datasets) are:
    - Amount (13 x 1)
    - Cost (1440 x 13)
    - kWh Cost (2 x 1)
    - Activities (1440 x 7)
    - Activities Outside Home (1440 x 7)
    - Activity Types (7 x 1)
    - EV DT (1440 x 2)
    - EV State (1440 x 4329)
    - Baseline EV (1440 x 1)
    - Baseline Non-EV (1440 x 1)
    - Actual EV (1440 x 1)
    - Actual Non-EV (1440 x 1)

    The optional fields are:
    - EV ID Matrix (1440 x 4329)
    - EV Locations (1440 x 4329)
    - EV Battery (1440 x 4329)
    - EV Mask (1440 x 4329)
    - Name (str)
    - Warn (str)

    Further details for the DSR data specification can be found in
    [the GitHub wiki.](https://github.com/ImperialCollegeLondon/gridlington-datahub/wiki/Agent-model-data#output)

    \f

    Args:
        file (UploadFile): A HDF5 file with the DSR data.

    Raises:
        HTTPException: If the data is invalid

    Returns:
        dict[str, str]: dictionary with the filename
    """  # noqa: D301
    log.info("Received DSR data.")
    data = read_dsr_file(file.file)

    validate_dsr_data(data)

    log.info("Appending new data...")
    log.debug(f"Current DSR data length: {len(dt.dsr_data)}")
    dt.dsr_data.append(data)
    log.debug(f"Updated DSR data length: {len(dt.dsr_data)}")

    return {"filename": file.filename}


@app.get("/dsr", response_class=ORJSONResponse)
def get_dsr_data(
    start: int = -1, end: int | None = None, col: str | None = None
) -> ORJSONResponse:
    """GET method function for getting DSR data as JSON.

    It takes optional query parameters of:
    - `start`: Starting index for exported list. Defaults to -1 for the most recent
      entry only.
    - `end`: Last index that will be included in exported list.
    - `col`: A comma-separated list of which columns/keys within the data to get.
      These values are all lower-case and spaces are replaced by underscores.

    And returns a dictionary containing the DSR data in JSON format.

    This can be converted back to a DataFrame using the following:
    `pd.DataFrame(**data)`

    \f

    Args:
        start: Starting index for exported list
        end: Last index that will be included in exported list
        col: Column names to filter by, multiple values seperated by comma

    Returns:
        A Dict containing the DSR list
    """  # noqa: D301
    log.info("Sending DSR data...")
    log.debug(f"Query parameters:\n\nstart={start}\nend={end}\ncol={col}\n")
    if isinstance(end, int) and end < start:
        message = "End parameter cannot be less than Start parameter."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    log.info("Filtering data by index...")
    log.debug(f"Current DSR data length:\n\n{len(dt.dsr_data)}")
    data = dt.dsr_data.copy()
    filtered_index_data = data[start : end + 1 if end else end]
    log.debug(f"Filtered DSR data length:\n\n{len(dt.dsr_data)}")

    if isinstance(col, str):
        log.debug(f"Columns:\n\n{col.split(',')}\n")
        columns = col.lower().split(",")

        for col_name in columns:
            if col_name not in dsr_headers.values():
                message = "One or more of the specified columns are invalid."
                log.error(message)
                raise HTTPException(status_code=400, detail=message)
    else:
        columns = list(dsr_headers.values())

    log.info("Filtering data by column...")
    filtered_data = []
    for frame in filtered_index_data:
        filtered_keys = {}
        for key, value in frame.items():
            if dsr_headers[key.title()] not in columns:
                continue
            elif not isinstance(value, str) and np.issubdtype(
                value.dtype, np.character
            ):
                filtered_keys[key] = value.astype(str).tolist()
            else:
                filtered_keys[key] = value
        filtered_data.append(filtered_keys)

    return ORJSONResponse({"data": filtered_data})


@app.get("/wesim")
def get_wesim_data() -> dict[str, dict[str, dict]]:  # type: ignore[type-arg]
    """GET method function for getting Wesim data as JSON.

    It returns a dictionary with the WESIM data in JSON format containing the following
    4 DataFrames:
    - Capacity (6, 12)
    - Regions (30, 10)
    - Interconnector Capacity (4, 2)
    - Interconnectors (25, 3)

    \f

    Returns:
        A Dict containing the Wesim Dataframes
    """  # noqa: D301
    log.info("Sending Wesim data...")
    if dt.wesim_data == {}:
        log.debug("Wesim data empty! Creating Wesim data...")
        dt.wesim_data = get_wesim()

    return {"data": dt.wesim_data}


@app.post("/set_model_signals")
def set_model_signals(start: bool) -> str:
    """POST method function for setting start and stop model signals.

    It has the query parameter:
    - `start`: A boolean to indicate the model should start running or stop running.

    \f

    Args:
        start: A bool flag for if the model should start running or stop running.
            True to start the model, False to stop the model.

    Returns:
        A confirmation message
    """  # noqa: D301
    message = "Start signal received" if start else "Stop signal received"
    log.info(message)
    dt.model_running = start

    return message


@app.post("/model_ready")
def signal_model_ready(ready: bool) -> str:
    """POST method function for indicating when the model has reset and is ready to run.

    This will reset the data in the DataHub to it's initial (empty) values when the
    ready signal is received as True.

    It has the query parameter:
    - `ready`: A boolean to indicate the model has completed setup and is ready.

    \f

    Args:
        ready: A bool flag for if the model has completed setup and is ready.

    Returns:
        A confirmation message
    """  # noqa: D301
    message = "Ready signal received" if ready else "Not-Ready signal received"
    log.info(message)
    dt.model_resetting = not ready

    if ready:
        dt.reset_data()

    return message


@app.get("/start")
def get_start_signal() -> bool:
    """GET method function for getting start model signal.

    It returns a boolean: True for if the model should start running.

    \f

    Returns:
        A bool flag for if the model should start
    """  # noqa: D301
    log.info("Start signal requested")

    return dt.model_running and not dt.model_resetting


@app.get("/stop")
def get_stop_signal() -> bool:
    """GET method function for getting stop model signal.

    It returns a boolean: True for if the model should stop running.

    \f

    Returns:
        A bool flag for if the model should stop
    """  # noqa: D301
    log.info("Start signal requested")

    return not dt.model_running
