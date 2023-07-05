"""This module defines the data structures for each of the models."""
from typing import Any, Hashable

from .opal import create_opal_frame

opal_data = [
    1,
    8.58,
    34.9085,
    34.9055,
    16.177,
    7.8868,
    15.1744,
    3.3549,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    16192.8871,
    16194.8348,
    -0.5713,
    -0.8467,
    16.2002,
    9.0618,
    0.2806,
    -2.1328,
    0,
    0.7931,
    0.0522,
    0.0522,
    34.8373,
    34.8343,
    0,
    0,
    30.801,
    30.801,
    28,
    5,
    63,
    72,
    0,
    303,
    7230,
    3.774,
    3.774,
    510,
    2,
    34,
]

opal_df = create_opal_frame()
dsr_data: list[dict[str, str | list]] = []  # type: ignore[type-arg]
wesim_data: dict[str, dict[Hashable, Any]] = {}  # type: ignore[misc]


if __name__ == "__main__":
    opal_df = create_opal_frame()
    print("Initial ---")
    print(opal_df)
    # opal_df = pd.concat([opal_df, append_opal_frame(opal_data)])
    # print("Append ---")
    # print(opal_df)
