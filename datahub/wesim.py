"""This module defines the data structures for the WESIM model."""

import pandas as pd

REGIONS_KEY = {
    "SCO": "Scotland",
    "NEW": "North Engl&Wal",
    "MID": "Midlands",
    "LON": "London",
    "SEW": "South Eng&Wal",
}

# header = pd.MultiIndex.from_product(
#     [["Interconnector"], ["SCO-IE", "NEW-NOR", "NEW-IE", "SEW-CE"]],
# )

# inter_data = [[491, -1238, 491, -1170], [491, -1022, 491, 1682]]
# inter_df = pd.DataFrame(inter_data, columns=header)
# print(inter_df)

# interconnectors = inter_df.stack().reset_index(names=["Hour", "Region Code"])
# print(interconnectors)

# print(pd.concat([output, interconnectors], ignore_index=True).sort_values(by="Hour"))


def read_wesim() -> dict[int | str, pd.DataFrame]:
    """Read the WESIM data from the excel file.

    Returns:
        pd.DataFrame: A Dictionary of DataFrames for each sheet in the file
    """
    return pd.read_excel(
        "../1_Wesim_GB_hourly_data.xlsx",
        sheet_name=None,
        header=[3, 4],
        index_col=1,
    )


def structure_wesim(df: pd.DataFrame) -> pd.DataFrame:
    """Structures the WESIM data.

    The final structure of the DataFrame will be

    Args:
        df: The unstructured wesim data

    Raises:
        ValueError: If the expected layout of the data is incorrect

    Returns:
        A structured DataFrame
    """
    df = df.dropna(axis="columns", how="all")

    df = df[
        [
            col
            for col in df.columns
            if col[1] in set(REGIONS_KEY.keys()).union({"Total"})
        ]
    ]
    stacked = df.stack()

    if isinstance(stacked, pd.DataFrame):
        df = stacked.reset_index(names=["Hour", "Region Code"])
    else:
        raise ValueError("Could not process input WESIM data")

    return df


def get_wesim() -> pd.DataFrame:
    """Gets the WESIM data from disk.

    Returns:
        The WESIM data
    """
    excel = read_wesim()

    capacity = excel["Capacity"].dropna(axis="columns", how="all")
    capacity = capacity[[col for col in capacity.columns if col[0] == "Region"]]
    capacity = capacity.transpose()
    capacity.index = capacity.index.droplevel(0)
    capacity.index.name = "Region"

    return structure_wesim(excel["RES output"])


if __name__ == "__main__":
    print(get_wesim())
