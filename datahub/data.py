"""This module defines the data structures for each of the models."""
import opal
import pandas as pd

if __name__ == "__main__":
    opal_df = opal.create_opal_frame()
    print("Initial ---")
    print(opal_df)
    opal_df = pd.concat([opal_df, opal.append_opal_frame()])
    print("Append ---")
    print(opal_df)
