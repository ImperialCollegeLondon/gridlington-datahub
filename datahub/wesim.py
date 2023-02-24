"""This module defines the data structures for the WESIM model."""
import pandas as pd

REGIONS_KEY = {
    "SCO": "Scotland",
    "NEW": "North Engl&Wal",
    "MID": "Midlands",
    "LON": "London",
    "SEW": "South Eng&Wal",
}

header = pd.MultiIndex.from_product(
    [["Onshore wind", "Offshore wind"], ["SCO", "NEW", "MID"]],
)

data = [[3142, 1947, 998, 1509, 13425, 767], [2642, 1586, 925, 1377, 12666, 699]]

df = pd.DataFrame(data, columns=header)
print(df)

output = df.stack().reset_index(names=["Hour", "Region Code"])
print(output)


header = pd.MultiIndex.from_product(
    [["Interconnector"], ["SCO-IE", "NEW-NOR", "NEW-IE", "SEW-CE"]],
)

inter_data = [[491, -1238, 491, -1170], [491, -1022, 491, 1682]]
inter_df = pd.DataFrame(inter_data, columns=header)
print(inter_df)

interconnectors = inter_df.stack().reset_index(names=["Hour", "Region Code"])
print(interconnectors)

print(pd.concat([output, interconnectors], ignore_index=True).sort_values(by="Hour"))

columns = [
    "Technology",
    "Scotland",
    "North Eng&Wal",
    "Midlands",
    "London",
    "South Eng&Wal",
]
data = [
    ["Onshore wind", 16472, 3297, 1062, 0, 3773],  # type: ignore[list-item]
    ["Offshore wind", 2770, 13744, 1427, 0, 17398],  # type: ignore[list-item]
]

df = pd.DataFrame(data, columns=columns).set_index("Technology").transpose()


print(df)
