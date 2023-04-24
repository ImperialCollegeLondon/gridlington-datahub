"""This module defines the data structures for the WESIM model."""

import pandas as pd

REGIONS_KEY = {
    "Scotland": "SCO",
    "North Engl&Wal": "NEW",
    "Midlands": "MID",
    "London": "LON",
    "South Eng&Wal": "SEW",
}

INTERCONNECTORS_KEY = {"SCO-IE", "NEW-NOR", "NEW-IE", "SEW-CE"}


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
            if col[1]
            in set(REGIONS_KEY.values()).union(INTERCONNECTORS_KEY).union({"Total"})
        ]
    ]
    stacked = df.stack()

    if isinstance(stacked, pd.DataFrame):
        df = stacked.reset_index(names=["Hour", "Region Code"])
        df.columns.name = None
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
    capacity = capacity.reset_index().replace({"Region": REGIONS_KEY})

    print(capacity)

    df = excel["Interconnector flows"].dropna(axis="columns", how="all")
    interconnectors = df[df.columns[:5]]

    interconnectors = structure_wesim(interconnectors)

    print(interconnectors)

    interconnector_capacity = df[["Code", "Capacity (MW)"]].dropna().T.reset_index().T
    interconnector_capacity.rename(
        columns=dict(
            zip(interconnector_capacity.columns, interconnector_capacity.iloc[0])
        )
    )
    interconnector_capacity = interconnector_capacity.iloc[1:].reset_index(drop=True)
    print(interconnector_capacity)

    return structure_wesim(excel["RES output"])


if __name__ == "__main__":
    print(get_wesim())
