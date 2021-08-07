## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2020, Suisei Entertainment
## ============================================================================
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## ============================================================================

"""
Contains the implementation of the ConsoleLogTarget class.
"""

# Runtime Imports
import logging

# Dependency Imports
import coloredlogs

# Murasame Imports
from murasame.log.logtarget import LogTarget

class ConsoleLogTarget(LogTarget):

    """Represents a log target that writes messages to the system console.

    Attributes:
        _colored_logs (bool): Whether or not console log should be colored.

        _format_string (str): Optional format string to use for log to
            console.

        _date_format_string (str): Optional date format string to use for
            log to console.

        _handler (object): The actual log handler object.

    Authors:
        Attila Kovacs
    """

    def __init__(self, logger: 'Logger', configuration: dict) -> None:

        """Creates a new ConsoleLogTarget entry.

        Args:
            logger (Logger): The logger object that will be used for log.

            configuration (dict): The configuration of the target in serialized
                format.

        Authors:
            Attila Kovacs
        """

        super().__init__(logger=logger)

        self._colored_logs = False
        self._format_string = None
        self._date_format_string = None
        self._handler = None

        # Parse the configuration data
        self._load_configuration(configuration=configuration)

        # Apply the configuration to the logger
        self._apply_configuration()

    def _load_configuration(self, configuration: dict) -> None:

        """Loads the configuration of the target from its serialized format.

        Args:
            configuration (dict): The configuration of the log target in
                serialized format.

        Authors:
            Attila Kovacs
        """

        # Load log coloring
        colored_logs = None
        try:
            colored_logs = configuration['coloredlogs']
        except KeyError:
            colored_logs = 'False'

        if colored_logs.lower() == 'true':
            self._colored_logs = True
        else:
            self._colored_logs = False

        # Load console log format
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
        self._handler = logging.StreamHandler()

        # Add the handler to the logger
        self.Logger.addHandler(self._handler)

        # Set formatter
        self._handler.setFormatter(logging.Formatter(
            fmt=self._format_string,
            datefmt=self._date_format_string))

        # Enable colored logs
        if self._colored_logs:
            coloredlogs.install(level=logging.DEBUG, logger=self.Logger)
