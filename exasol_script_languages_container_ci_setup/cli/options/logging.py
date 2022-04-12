import logging

import click

SUPPORTED_LOG_LEVELS = { "normal": logging.WARNING, "info": logging.INFO, "debug": logging.DEBUG }

logging_options = [
    click.option('--log-level', type=click.Choice(SUPPORTED_LOG_LEVELS.keys()), default="normal",
                 help="Level of information printed out. "
                      "'Normal' prints only necessary information. "
                      "'Info' prints also internal status info. 'Debug' prints detailed information."),
]


def set_log_level(level: str):
   try:
      return SUPPORTED_LOG_LEVELS[level]
   except KeyError as ex:
      raise ValueError(f"log level {level} is not supported!") from ex
