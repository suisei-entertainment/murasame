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
Contains implementation of the LogChannel class.
"""

# Runtime Imports
import logging

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.log.loglevels import LogLevels, LOG_LEVEL_CONVERSION_MAP
from murasame.log.logentry import LogEntry
from murasame.log.consolelogtarget import ConsoleLogTarget
from murasame.log.filelogtarget import FileLogTarget

class LogChannel:

    """Represents a single log channel.

    Attributes:

        _name (str): The name of the channel.

        _default_log_level (LogLevels): The default log level for the channel.

        _targets (list): List of log targets this channel is writing to.

        _logger (Logger)

    Authors:
        Attila Kovacs
    """

    @property
    def Name(self) -> str:

        """The name of the channel.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def DefaultLogLevel(self) -> LogLevels:

        """The default log level of the channel.

        Authors:
            Attila Kovacs
        """

        return self._default_log_level

    def __init__(self, configuration: dict) -> None:

        """Creates a new log channel instance.

        Args:
            configuration (dict): The configuration of the channel.

        Authors:
            Attila Kovacs
        """

        self._name = None
        self._default_log_level = None
        self._targets = []

        self._load_configuration(configuration)

        # Get a reference to the wrapped Python logger object.
        self._logger = logging.getLogger(self._name)

        # Set the log level to DEBUG, so all log messages would be written to
        # the logger by default. Actual log level will be controlled by the
        # writers.
        self._logger.setLevel(logging.DEBUG)

        self._load_targets(configuration)

    def write(self, entry: LogEntry) -> None:

        """Writes a new log entry to the channel.

        Args:
            entry (LogEntry): The log entry to write.

        Authors:
            Attila Kovacs
        """

        # Send the message to the central logger
        if entry.LogLevel in (LogLevels.TRACE, LogLevels.DEBUG):
            self._logger.debug(entry.Message)
        elif entry.LogLevel in (LogLevels.INFO, LogLevels.NOTICE):
            self._logger.info(entry.Message)
        elif entry.LogLevel == LogLevels.NOTICE:
            self._logger.info(entry.Message)
        elif entry.LogLevel == LogLevels.WARNING:
            self._logger.warning(entry.Message)
        elif entry.LogLevel == LogLevels.ERROR:
            self._logger.error(entry.Message)
        elif entry.LogLevel in (LogLevels.CRITICAL, LogLevels.ALERT, LogLevels.EMERGENCY):
            self._logger.fatal(entry.Message)

        # Send the message to all targets
        for target in self._targets:
            target.write(entry=entry)

    def _load_configuration(self, configuration: dict) -> None:

        """Loads the configuration of the channel from its serialized version.

        Args:
            configuration (dict): The configuration of the channel.

        Raises:
            InvalidInputError: Raised when there is no channel name found in
                the configuration.

        Authors:
            Attila Kovacs
        """

        # Load channel name
        try:
            self._name = configuration['name']
        except KeyError as exception:
            raise InvalidInputError(
                'No channel name found while trying to load the '
                'configuration of a log channel.') from exception

        # Load default log level
        try:
            self._default_log_level = \
                LOG_LEVEL_CONVERSION_MAP[configuration['defaultloglevel']]
        except KeyError:
            # Use the default value if there is none specified in the
            # configuraiton.
            self._default_log_level = LogLevels.INFO

    def _load_targets(self, configuration: dict) -> None:

        """Loads the log targets of the channel from its serialized version.

        Args:
            configuration (dict): The configuration of the channel.

        Authors:
            Attila Kovacs
        """

        # Remove all existing log handlers
        self._logger.handlers = []

        targets = []

        # Load targets
        try:
            targets = configuration['targets']
        except KeyError as exception:
            raise InvalidInputError(
                f'No log targets were found for channel '
                f'{self._name}') from exception

        for target in targets:

            # Determine target type
            target_type = None
            try:
                target_type = target['type']
            except KeyError:
                # Jump to the next target if there is no type specified for
                # the current one.
                continue

            log_target = None

            # Load the target based on type
            try:
                if target_type == 'console':
                    log_target = ConsoleLogTarget(logger=self._logger,
                                                  configuration=target)
                elif target_type == 'file':
                    log_target = FileLogTarget(
                        logger=self._logger,
                        configuration=target,
                        root_path=configuration['__log_root_path__'])

            except InvalidInputError:
                # Don't fail if the configuration of a target is wrong.
                continue

            if log_target is not None:
                self._targets.append(log_target)
