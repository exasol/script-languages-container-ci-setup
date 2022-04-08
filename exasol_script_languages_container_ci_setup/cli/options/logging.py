import logging

import click

_supported_log_levels = ["normal", "info", "debug"]

logging_options = [
    click.option('--log-level', type=click.Choice(_supported_log_levels), default="normal",
                 help="Level of information printed out. "
                      "'Normal' prints only necessary information. "
                      "'Info' prints also internal status info. 'Debug' prints detailed information."),
]


def set_log_level(level: str):
    if level == _supported_log_levels[0]:
        logging.basicConfig(level=logging.WARNING)
    elif level == _supported_log_levels[1]:
        logging.basicConfig(level=logging.INFO)
    elif level == _supported_log_levels[2]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        raise ValueError(f"log level {level} is not supported!")
