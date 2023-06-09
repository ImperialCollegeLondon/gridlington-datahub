"""Script for running Datahub API."""
from typing import Any, Hashable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import data as dt

app = FastAPI()


class OpalDictData(BaseModel):
    """Class for defining required key values for Opal data as a dict."""

    frame: int
    time: float
    total_gen: float
    total_dem: float
    total_offwind: float
    intra_trade: float
    intra_gen: float
    intra_dem: float
    intra_sto: float
    bm_gen: float
    bm_sto: float
    bm_dem: float
    offwind_exp: float
    offwind_real: float
    bat_gen: float
    inter_gen: float
    offwind_gen: float
    onwind_gen: float
    other_gen: float
    pump_gen: float
    pv_gen: float
    nc_gen: float
    hyd_gen: float
    gas_gen: float
    total_exp: float
    total_real: float
    bm_cost: float
    bm_accept: float
    exp_dem: float
    real_dem: float
    act_work: int
    act_study: int
    act_home: int
    act_pers: int
    act_shop: int
    act_leis: int
    act_sleep: int
    exp_ev: float
    real_ev: float
    ev_charge: int
    ev_travel: int
    ev_idle: int


class OpalArrayData(BaseModel):
    """Class for defining required key values for Opal data as an array."""

    array: list[float]


@app.post("/opal")
def create_opal_data(data: OpalDictData | OpalArrayData) -> dict[str, str]:
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
def get_opal_data() -> dict[str | Hashable, Any]:  # type: ignore[misc]
    """GET method function for getting Opal Dataframe as JSON.

    Returns:
        A Dict of the Opal Dataframe in JSON format
    """
    data = dt.opal_df.to_dict(orient="split")
    return data
