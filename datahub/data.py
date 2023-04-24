"""This module defines the data structures for each of the models."""
import pandas as pd

from .opal import append_opal_frame, create_opal_frame

if __name__ == "__main__":
    opal_df = create_opal_frame()
    print("Initial ---")
    print(opal_df)
    opal_df = pd.concat([opal_df, append_opal_frame()])
    print("Append ---")
    print(opal_df)
