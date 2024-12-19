import logging.config

import yaml

def setup_logger() -> None:
    with open('utils/logging_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    logging.config.dictConfig(config)
