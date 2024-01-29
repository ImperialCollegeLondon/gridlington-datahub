"""This module defines the data structures for the WESIM model."""

import os

import pandas as pd

REGIONS_KEY = {
    "Scotland": "SCO",
    "North Eng&Wal": "NEW",
    "Midlands": "MID",
    "London": "LON",
    "South Eng&Wal": "SEW",
}

INTERCONNECTORS_KEY = {"SCO-IE", "NEW-NOR", "NEW-IE", "SEW-CE"}
WESIM_DATA_FILE = os.environ.get("WESIM_DATA_FILE", "../1_Wesim_GB_hourly_data.xlsx")


def read_wesim(wesim_data_file: str) -> dict[int | str, pd.DataFrame]:
    """Read the WESIM data from the excel file.

    Returns:
        pd.DataFrame: A Dictionary of DataFrames for each sheet in the file
    """
    with pd.ExcelFile(wesim_data_file) as xlsx:
        # Read first 4 Sheets
        excel = pd.read_excel(
            xlsx,
            sheet_name=xlsx.sheet_names[:4],
            header=[3, 4],
            index_col=1,
        )
        # Read Interconnectors sheet
        interconnectors = pd.read_excel(
            xlsx,
            sheet_name=xlsx.sheet_names[4],
            header=4,
            index_col=0,
            usecols="B:G",
        )
        interconnectors.columns = pd.MultiIndex.from_product(
            [["Interconnector"], interconnectors.columns]
        )
        excel[xlsx.sheet_names[4]] = interconnectors
        # Read Interconnector capacity from Interconnectors sheet
        excel["Interconnector Capacity"] = pd.read_excel(
            xlsx,
            sheet_name=xlsx.sheet_names[4],
            header=3,
            usecols="J:K",
            nrows=4,
        )

    return excel


def structure_wesim(df: pd.DataFrame) -> pd.DataFrame:
    """Structures the Regions and Interconnectors WESIM data.

    The final DataFrame will have columns: Hour, Code, and some usage data.

    Args:
        df: The unstructured wesim data

    Raises:
        ValueError: If the expected layout of the data is incorrect

    Returns:
        A structured DataFrame
    """
    df = df.dropna(axis="columns", how="all")

    # Select only the columns with Regions, Interconnectors or Total data
    df = df[
        [
            col
            for col in df.columns
            if col[1]
            in set(REGIONS_KEY.values()).union(INTERCONNECTORS_KEY).union({"Total"})
        ]
    ]

    # Change from multi-level columns headings to vertically-stacked columns
    stacked = df.stack()

    # Move the Hour and Code data from a multi-index to individual columns
    if isinstance(stacked, pd.DataFrame):
        df = stacked.reset_index(names=["Hour", "Code"])
        df.columns.name = None
    else:
        raise ValueError("Could not process input WESIM data")

    return df


def structure_capacity(df: pd.DataFrame) -> pd.DataFrame:
    """Structures the Capacity dataframe.

    Args:
        df: The DF as read from the excel file

    Returns:
        A structured Dataframe
    """
    df = df.dropna(axis="columns", how="all")

    # Select only the columns within the Region table and make Technologies the columns
    df = df[[col for col in df.columns if col[0] == "Region"]]
    df = df.transpose()
    df.index = df.index.droplevel(0)
    df.index.name = "Code"

    # Return with the a Region columns matching the regions keys
    return df.reset_index().replace({"Code": REGIONS_KEY})


def get_wesim() -> dict[str, dict]:  # type: ignore[type-arg]
    """Gets the WESIM data from disk and puts it into pandas dataframes.

    Returns:
        The WESIM data
    """
    excel = read_wesim(WESIM_DATA_FILE)

    capacity = structure_capacity(excel.pop("Capacity"))
    interconnectors = structure_wesim(excel.pop("Interconnector flows"))
    interconnector_capacity = excel.pop("Interconnector Capacity")

    # Combine the regions data from separate sheets into one DF
    regions = pd.DataFrame(columns=["Hour", "Code"])
    for df in excel.values():
        regions = regions.merge(structure_wesim(df), how="outer")

    return {
        "Capacity": capacity.to_dict(orient="split"),
        "Regions": regions.to_dict(orient="split"),
        "Interconnector Capacity": interconnector_capacity.to_dict(orient="split"),
        "Interconnectors": interconnectors.to_dict(orient="split"),
    }
