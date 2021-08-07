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
Contains the implementation of the LogEntry class.
"""

class LogEntry:

    """Representation of a single log entry.

    Attributes:
        _level (LogLevels): The log level of the entry.

        _timestamp (datetime): The time when the entry has been created.

        _message (str): The actual log message.

        _classname (str): Name of the class that sent the message.

    Authors:
        Attila Kovacs
    """

    @property
    def LogLevel(self) -> 'LogLevels':

        """The log level of the entry.

        Authors:
            Attila Kovacs
        """

        return self._level

    @property
    def Timestamp(self) -> 'datetime':

        """The time when the entry has been created.

        Authors:
            Attila Kovacs
        """

        return self._timestamp

    @property
    def Message(self) -> str:

        """The actual log message.

        Authors:
            Attila Kovacs
        """

        return self._message

    @property
    def Classname(self) -> str:

        """Name of the class that created the log entry.

        Authors:
            Attila Kovacs
        """

        return self._classname

    def __init__(self,
                 level: 'LogLevels',
                 timestamp: 'datetime',
                 message: str,
                 classname: str) -> None:

        """Creates a new LogEntry instance.

        Args:
            level (LogLevels): The log level of the entry.

            timestamp (datetime): The time when the entry has been created.

            message (str): The actual log message.

            classname (str): Name of the class that created the log entry.

        Authors:
            Attila Kovacs
        """

        self._level = level
        self._timestamp = timestamp
        self._message = message
        self._classname = classname
