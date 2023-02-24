"""This module defines the data structures for each of the models."""
import pandas as pd

REGIONS_KEY = {
    "SCO": "Scotland",
    "NEW": "North England and Wales",
    "MID": "Midlands",
    "LON": "London",
    "SEW": "South England and Wales",
}

header = pd.MultiIndex.from_product(
    [["Onshore wind", "Offshore wind"], ["SCO", "NEW", "MID"]],
    names=["Hour", "Region"],
)

data = [[3142, 1947, 998, 1509, 13425, 767], [2642, 1586, 925, 1377, 12666, 699]]

df = pd.DataFrame(data, columns=header)
print(df)

wesim_data = df.stack().reset_index(level=["Region"])
print(wesim_data)
