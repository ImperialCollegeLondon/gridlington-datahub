"""The uvicorn server to run the Datahub API."""
import uvicorn

from datahub.core.log_config import logging_dict_config

if __name__ == "__main__":
    uvicorn.run(
        "datahub.main:app",
        port=8000,
        host="0.0.0.0",
        log_config=logging_dict_config,
    )
