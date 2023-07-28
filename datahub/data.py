"""This module defines the data structures for each of the models."""
from typing import Any, Hashable

from .opal import create_opal_frame

opal_df = create_opal_frame()
dsr_data: list[dict[str, str | list]] = []  # type: ignore[type-arg]
wesim_data: dict[str, dict[Hashable, Any]] = {}  # type: ignore[misc]
