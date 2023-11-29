"""This module defines the data structures for each of the models."""
import pandas as pd
from numpy.typing import NDArray

from .opal import create_opal_frame

opal_df: pd.DataFrame = create_opal_frame()
dsr_data: list[dict[str, NDArray | str]] = []  # type: ignore[type-arg]
wesim_data: dict[str, dict] = {}  # type: ignore[type-arg]

model_running: bool = False
model_resetting: bool = False
