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
    excel = pd.read_excel(
        "../1_Wesim_GB_hourly_data.xlsx",
        sheet_name=None,
        header=[3, 4],
        index_col=1,
    )

    excel.pop("Sheet1", None)

    return excel


def structure_wesim(df: pd.DataFrame) -> pd.DataFrame:
    """Structures the WESIM data.

    The final DataFrame will have columns: Hour, Region Code, and some other data

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


def structure_capacity(df: pd.DataFrame) -> pd.DataFrame:
    """Structures the Capacity dataframe.

    TODO: This needs to be tidied.

    Args:
        df: The DF as read from the excel file

    Returns:
        A structured Dataframe
    """
    df = df.dropna(axis="columns", how="all")
    df = df[[col for col in df.columns if col[0] == "Region"]]
    df = df.transpose()
    df.index = df.index.droplevel(0)
    df.index.name = "Region"
    return df.reset_index().replace({"Region": REGIONS_KEY})


def structure_interconnectors(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Structures the Interconnectors and Interconnector capacities dataframes.

    TODO: This needs to be tidied.

    Args:
        df: The DF as read from the excel file

    Returns:
        Two structured Dataframes
    """
    df = df.dropna(axis="columns", how="all")
    interconnectors = structure_wesim(df[df.columns[:5]])

    interconnector_capacity = df[["Code", "Capacity (MW)"]].dropna().T.reset_index().T
    interconnector_capacity.rename(
        columns=dict(
            zip(interconnector_capacity.columns, interconnector_capacity.iloc[0])
        )
    )
    interconnector_capacity = interconnector_capacity.iloc[1:].reset_index(drop=True)

    return interconnectors, interconnector_capacity


def get_wesim() -> dict[str, pd.DataFrame]:
    """Gets the WESIM data from disk.

    Returns:
        The WESIM data
    """
    excel = read_wesim()

    capacity = structure_capacity(excel.pop("Capacity"))

    interconnectors, interconnector_capacity = structure_interconnectors(
        excel.pop("Interconnector flows")
    )

    regions = pd.DataFrame(columns=["Hour", "Region Code"])
    for df in excel.values():
        regions = regions.merge(structure_wesim(df), how="outer")

    return {
        "Capacity": capacity,
        "Regions": regions,
        "Interconnector Capacity": interconnector_capacity,
        "Interconnectors": interconnectors,
    }


if __name__ == "__main__":
    for name, df in get_wesim().items():
        print(name + ":")
        print(df)
        print("--------")
