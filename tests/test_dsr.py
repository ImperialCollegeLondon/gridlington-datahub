import numpy as np
import pytest


def test_validate_dsr_data(dsr_data):
    """Tests the validate_dsr_arrays function."""
    from fastapi import HTTPException

    from datahub.dsr import validate_dsr_data

    # Confirm no errors are raised
    validate_dsr_data(dsr_data)

    # Check invalid array lengths raises an error
    dsr_data["Amount"] = np.append(dsr_data["Amount"], 1.0)
    dsr_data["Cost"] = dsr_data["Cost"][1:]

    with pytest.raises(HTTPException) as err:
        validate_dsr_data(dsr_data)
    assert err.value.detail == "Invalid size or data type for: Amount, Cost."

    dsr_data.pop("Amount")

    with pytest.raises(HTTPException) as err:
        validate_dsr_data(dsr_data)
    assert err.value.detail == "Missing required fields: Amount."
