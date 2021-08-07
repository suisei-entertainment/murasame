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
Contains the implementation of the LogLevels class.
"""

# Runtime Imports
from enum import IntEnum, auto

class LogLevels(IntEnum):

    """Contains the list of supported log levels.

    This maps to log levels
    supported by syslog. For Python log, some log levels are merged
    according to the following table:

    Murasame Log Level | Syslog Log Level | Python Log Level
    =====================================================
     TRACE         |      DEBUG       |     DEBUG
     DEBUG         |      DEBUG       |     DEBUG
     INFO          |      INFO        |     INFO
     NOTICE        |      NOTICE      |     INFO
     WARNING       |      WARNING     |     WARNING
     ERROR         |      ERROR       |     ERROR
     CRITICAL      |      CRITICAL    |     FATAL
     ALERT         |      ALERT       |     FATAL
     EMERGENCY     |      EMERGENCY   |     FATAL

    Authors:
        Attila Kovacs
    """

    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    NOTICE = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    ALERT = auto()
    EMERGENCY = auto()

# Conversion map to use when reading the log level from a string.
LOG_LEVEL_CONVERSION_MAP = \
{
    'TRACE': LogLevels.TRACE,
    'DEBUG': LogLevels.DEBUG,
    'INFO': LogLevels.INFO,
    'NOTICE': LogLevels.NOTICE,
    'WARNING': LogLevels.WARNING,
    'ERROR': LogLevels.ERROR,
    'CRITICAL': LogLevels.CRITICAL,
    'ALERT': LogLevels.ALERT,
    'EMERGENCY': LogLevels.EMERGENCY
}
