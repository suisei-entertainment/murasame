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
Contains the implementation of the AlreadyExistsError exception.
"""

# Framework Imports
from murasame.exceptions.errorcodes import ErrorCodes
from murasame.exceptions.exception import FrameworkError

class AlreadyExistsError(FrameworkError):

    """Exception raised when trying to add something twice to e.g. a list or
    dictionary.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 message: str = '',
                 errorcode: ErrorCodes = ErrorCodes.ALREADY_EXISTS,
                 package: str = __package__,
                 file: str = '',
                 line: str = '',
                 function: str = '',
                 wrapped_exception: Exception = None,
                 inspect_caller: bool = True) -> None:

        """Creates a new AlreadyExistsError instance.

        Args:
            message (str): The user message that clarifies the exception.

            errorcode (ErrorCodes): The platform error code that identifies the
                actual error.

            package (str): Name of the Python package that raised the
                exception.

            file (str): Name of the source file where the exception was raised.

            line (int): The line number in the source code where the exception
                was raised.

            function (str): Name of the function that raised the exception.

            wrapped_exception (Exception):  Another exception that is wrapped
                 inside the Murasame exception.

            inspect_caller (bool): Whether or not the caller should be
                inspected to retrieve the raising location of the exception.
                Should only be 'True' in the topmost exception in the
                inheritance tree, otherwise should be passed down as 'False'.

        Authors:
            Attila Kovacs
        """

        # Inspect the caller if requested
        if inspect_caller:
            file, function, line = self.inspect_exception()

        super().__init__(message=message,
                         errorcode=errorcode,
                         package=package,
                         file=file,
                         line=line,
                         function=function,
                         wrapped_exception=wrapped_exception,
                         inspect_caller=False)
