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
Contains the implementation of the FileLogTarget class.
"""

# Runtime Imports
import os
import logging
from logging.handlers import RotatingFileHandler

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.log.logtarget import LogTarget

class FileLogTarget(LogTarget):

    """Represents a log target that writes messages to a local file.

    Attributes:
        _filename (str): Name of the log file.

        _max_size (int): The maximum size of the log file in bytes.

        _backup_count (int): The amount of backup files to keep.

        _format_string (str): Optional format string to use for log to
            console.

        _date_format_string (str): Optional date format string to use for
            log to console.

        _handler (object): The actual log handler object.

    Authors:
        Attila Kovacs
    """

    def __init__(
        self,
        logger: 'Logger',
        configuration: dict,
        root_path: str) -> None:

        """Creates a new FileLogTarget entry.

        Args:
            logger (Logger): The logger object that will be used for log.

            configuration (dict): The configuration of the target in serialized
                format.

            root_path (str): Root path of the log system.

        Authors:
            Attila Kovacs
        """

        super().__init__(logger=logger)

        self._filename = None
        self._max_size = None
        self._backup_count = None
        self._format_string = None
        self._date_format_string = None
        self._handler = None

        # Parse the configuration
        self._load_configuration(configuration=configuration,
                                 root_path=root_path)

        # Apply the configuration to the logger.
        self._apply_configuration()

    def _load_configuration(
        self,
        configuration: dict,
        root_path: str) -> None:

        """Loads the configuration of the target from its serialized format.

        Args:
            configuration (dict): The configuration of the log target in
                serialized format.

            root_path (str): Root path of the log system.

        Authors:
            Attila Kovacs
        """

        filename = configuration['filename']

        # Load filename
        try:
            self._filename = os.path.abspath(
                os.path.expanduser(f'{root_path}/{filename}'))
        except KeyError as exception:
            raise InvalidInputError(
                'Filename is not found in the configuration when trying to '
                'configure logger.') from exception

        # Load max size
        try:
            self._max_size = int(configuration['maxsize']) * 1024 * 1024
        except KeyError:
            self._max_size = 1 * 1024 * 1024

        # Load backup count
        try:
            self._backup_count = int(configuration['backupcount'])
        except KeyError:
            self._backup_count = 2

        # Load log format
        try:
            self._format_string = configuration['format']
        except KeyError:
            self._format_string = '[%(asctime)s][%(levelname)s]: %(message)s'

        # Load date format
        try:
            self._date_format_string = configuration['dateformat']
        except KeyError:
            self._date_format_string = '%Y-%m-%d %H:%M:%S'

    def _apply_configuration(self) -> None:

        """Applies the configuration to the underlying logger object.

        Authors:
            Attila Kovacs
        """

        # Create the handler
        self._handler = RotatingFileHandler(
            filename=self._filename,
            mode='a',
            maxBytes=self._max_size,
            backupCount=self._backup_count)

        # Add the handler to the logger
        self.Logger.addHandler(self._handler)

        # Set formatter
        self._handler.setFormatter(logging.Formatter(
            fmt=self._format_string,
            datefmt=self._date_format_string))
