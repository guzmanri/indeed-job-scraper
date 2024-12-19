import logging.config

import yaml

def setup_logger() -> None:
    with open('logging_config/logging_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    logging.config.dictConfig(config)
