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
Contains the implementation of the ApplicationReturnCodes enum.
"""

# Runtime Imports
from enum import IntEnum

class ApplicationReturnCodes(IntEnum):

    """
    Contains the list of application exit codes supported by Murasame.

    Authors:
        Attila Kovacs
    """

    # Application execution finished successfully.
    SUCCESS = 0

    # Daemon application is already running.
    ALREADY_RUNNING = 1

    # Daemon application is not running.
    NOT_RUNNING = 2

    # Application error originating from the underlying platform.
    PLATFORM_ERROR = 3

    # Uncaught exception was triggered.
    UNCAUGHT_EXCEPTION = 666
