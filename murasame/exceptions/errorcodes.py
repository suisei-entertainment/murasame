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
Contains the list of error codes supported by the framework.
"""

# Runtime Imports
from enum import IntEnum

class ErrorCodes(IntEnum):

    """Contains the list of error codes supported by the framework.

    Arguments:
        NOT_SET: Default value when an exact error code is not set.

        INPUT_ERROR: Indicates an error in the input values.

        PERMISSION_ERROR: Indicates a permission violation error.

        RUNTIME_ERROR: Indicates a runtime error.

        ALREADY_REGISTERED: Indicates that something has already been
            registered.

        ALREADY_EXISTS: Indicates that something already exists.

        NOT_REGISTERED: Indicates that something is not registered.

        UNCAUGHT_EXCEPTION: Indicates that an exception is not handled
            properly.

        MISSING_REQUIREMENT: Indicates that a required component is missing.

        INSTALL_FAILED: Indicates that installation of a required component has
            failed.

        LICENSE_ERROR: Indicates an invalid license key.

        DATABASE_ERROR: Indicates a database operation error.

    Authors:
        Attila Kovacs
    """

    NOT_SET = 0
    INPUT_ERROR = 1
    PERMISSION_ERROR = 2
    RUNTIME_ERROR = 3
    ALREADY_REGISTERED = 4
    ALREADY_EXISTS = 5
    NOT_REGISTERED = 6
    UNCAUGHT_EXCEPTION = 7
    MISSING_REQUIREMENT = 8
    INSTALL_FAILED = 9
    LICENSE_ERROR = 10
    DATABASE_ERROR = 11
