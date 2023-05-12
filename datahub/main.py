"""Script for running Datahub API."""

from fastapi import FastAPI
from pydantic import BaseModel

from . import data as dt

app = FastAPI()


class OpalData(BaseModel):
    """Class for defining required key values for Opal data."""

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


@app.post("/opal")
def create_data(data: OpalData) -> dict[str, float]:
    """Post method function for appending data to Opal dataframe."""
    raw_data = {
        "frame": data.frame,
        "time": data.time,
        "total_gen": data.total_gen,
        "total_dem": data.total_dem,
        "total_offwind": data.total_offwind,
        "intra_trade": data.intra_trade,
        "intra_gen": data.intra_gen,
        "intra_dem": data.intra_dem,
        "intra_sto": data.intra_sto,
        "bm_gen": data.bm_gen,
        "bm_sto": data.bm_sto,
        "bm_dem": data.bm_dem,
        "offwind_exp": data.offwind_exp,
        "offwind_real": data.offwind_real,
        "bat_gen": data.bat_gen,
        "inter_gen": data.inter_gen,
        "offwind_gen": data.offwind_gen,
        "onwind_gen": data.onwind_gen,
        "other_gen": data.other_gen,
        "pump_gen": data.pump_gen,
        "pv_gen": data.pv_gen,
        "nc_gen": data.nc_gen,
        "hyd_gen": data.hyd_gen,
        "gas_gen": data.gas_gen,
        "total_exp": data.total_exp,
        "total_real": data.total_real,
        "bm_cost": data.bm_cost,
        "bm_accept": data.bm_accept,
        "exp_dem": data.exp_dem,
        "real_dem": data.real_dem,
        "act_work": data.act_work,
        "act_study": data.act_study,
        "act_home": data.act_home,
        "act_pers": data.act_pers,
        "act_shop": data.act_shop,
        "act_leis": data.act_leis,
        "act_sleep": data.act_sleep,
        "exp_ev": data.exp_ev,
        "real_ev": data.real_ev,
        "ev_charge": data.ev_charge,
        "ev_travel": data.ev_travel,
        "ev_idle": data.ev_idle,
    }

    print(dt.opal_df)
    dt.opal_df.opal.append(raw_data)
    print(dt.opal_df)

    return raw_data
