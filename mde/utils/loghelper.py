## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

"""
Contains utility functions used for logging.
"""

# Runtime Imports
import logging

# MDE Imports
from mde.constants import MDE_LOGGER_NAME, LOG_FILE_PATH

STRING_TO_LOG_LEVEL = \
{
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

LOG_LEVEL_TO_STRING = \
{
    logging.DEBUG: 'DEBUG',
    logging.INFO: 'INFO',
    logging.WARNING: 'WARNING',
    logging.ERROR: 'ERROR',
    logging.CRITICAL: 'CRITICAL'
}

def enable_coloredlogs(log_level: int) -> None:

    """Enables colored logs, if the coloredlogs package is available.

    Args:
        log_level (int): The log level that is configured for the logging
            system.

    Authors:
        Attila Kovacs
    """

    try:
        import coloredlogs
        coloredlogs.install(level=LOG_LEVEL_TO_STRING[log_level])
    except ImportError:
        pass

def initialize_logging(log_level: str = 'DEBUG') -> None:

    """Initializes the logging of MDE.

    Authors:
        Attila Kovacs
    """

    invalid_log_level = None

    try:
        invalid_log_level = log_level
        log_level = STRING_TO_LOG_LEVEL[log_level.upper()]
        invalid_log_level = None
    except KeyError:
        # Specified log level not found, use default debug
        log_level = logging.DEBUG

    logger = logging.getLogger()
    logging.basicConfig(filename=LOG_FILE_PATH, level=log_level)
    enable_coloredlogs(log_level=log_level)

    if invalid_log_level is not None:
        logger.error(f'Invalid log level was specified: {invalid_log_level}. '
                     f'Log level is set to DEBUG.')
    logger.debug(f'Log level is set to {LOG_LEVEL_TO_STRING[log_level]}.')
