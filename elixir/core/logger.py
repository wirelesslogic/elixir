import json
import logging
import logging.config
from pathlib import Path

import yaml


def create_logger(default_level=logging.INFO, logger_name="app"):
    try:
        path = Path("config/logging.yml")
        config_file = path.read_text()
        yaml_config = yaml.safe_load(config_file)
        logging.config.dictConfig(yaml_config)
    except Exception as e:
        print(e)
        print("Error in Logging Configuration. Using default configs.")
        logging.basicConfig(level=default_level)

    logger = logging.getLogger(logger_name)

    def create_custom_log_function(original_log_function):
        def custom_log_function(msg, *args, **kwargs):
            if isinstance(msg, dict):
                original_log_function(
                    f"\n{json.dumps(msg, indent=4)}", *args, **kwargs, stacklevel=2
                )
            else:
                original_log_function(msg, *args, **kwargs, stacklevel=2)

        return custom_log_function

    # Extend logger to pretty-print if input is a dictionary
    logger.debug = create_custom_log_function(logger.debug)
    logger.info = create_custom_log_function(logger.info)
    logger.warning = create_custom_log_function(logger.warning)
    logger.error = create_custom_log_function(logger.error)

    return logger


log = create_logger()
