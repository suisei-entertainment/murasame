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
Contains the implementation of the LogTarget class.
"""

class LogTarget:

    """Common base class for log target implementations.

    Attributes:
        _logger (Logger): The logger object used by this target.

    Authors:
        Attila Kovacs
    """

    @property
    def Logger(self) -> 'Logger':

        """Provides access to the underlying logger object.

        Authors:
            Attila Kovacs
        """

        return self._logger

    def __init__(self, logger: 'Logger') -> None:

        """Creates a new ConsoleLogTarget entry.

        Args:
            logger (Logger): The logger object that will be used for
                logging.

        Authors:
            Attila Kovacs
        """

        self._logger = logger

    def write(self, entry: 'LogEntry') -> None:

        """Writes a log message to the target.

        This function does not do anything by default. It is here to provide a
        way for custom log target implementations to write their own log
        messages outside the Python log infrastructure.

        Args:
            entry (LogEntry): The log entry to write.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del entry
