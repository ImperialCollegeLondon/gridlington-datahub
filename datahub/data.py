"""This module defines the data structures for each of the models."""
from opal import create_opal_frame

if __name__ == "__main__":
    opal_df = create_opal_frame()
    print(opal_df)
    print(type(opal_df))
