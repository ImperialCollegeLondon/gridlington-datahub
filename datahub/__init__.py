"""The main module for datahub."""
import logging
import logging.config

from .core.log_config import logging_dict_config

logging.config.dictConfig(logging_dict_config)

log = logging.getLogger("api_logger")
log.debug("Logging is configured.")
log.info("Datahub API is running...")
