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
Contains the implementation of the basic exception class.
"""

# Runtime Imports
import logging
import inspect

# Murasame Imports
from murasame.constants import MURASAME_EXCEPTIONS_LOG_CHANNEL
from murasame.exceptions.errorcodes import ErrorCodes

class FrameworkError(Exception):

    """The base class for all Murasame framework errors.

    Attributes:
        errorcode (ErrorCodes): The platform error code that identifies the
            exact issue.

        errormessage (str): Custom error message specified by the user when
            raising the exception.

        package (str): Name of the package that raised the expcetion.

        file (str): Name of the source file where the exception was raised.

        line (int): The source line where the exception has been raised.

        function (str): The function that raised the exception.

        wrapped_exception (Exception): An exception that was asked to be
            wrapped within a framework exception.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 message: str = '',
                 errorcode: ErrorCodes = ErrorCodes.NOT_SET,
                 package: str = __package__,
                 file: str = '',
                 line: str = '',
                 function: str = '',
                 wrapped_exception: Exception = None,
                 inspect_caller: bool = True) -> None:

        """Creates a new FrameworkError instance.

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

        super().__init__(message)

        self.errorcode = errorcode
        self.errormessage = message
        self.package = package
        self.file = file
        self.line = line
        self.function = function
        self.wrapped_exception = wrapped_exception

        # When inspect_caller is set to True, then the caller function will be
        # inspected to retrieve the correct location of where the exception
        # was raised.
        if inspect_caller:
            self.file, self.function, self.line = self.inspect_exception()

        # Log the exception
        logger = logging.getLogger(MURASAME_EXCEPTIONS_LOG_CHANNEL)
        logger.error(f'Framework exception was raised. '
                     f'Type: {self.__class__.__name__}\n'
                     f'Error Code: {self.errorcode}\n'
                     f'Package: {self.package}\n'
                     f'Location: {self.file} (line {self.line})\n'
                     f'Function: {self.function}()\n'
                     f'Message: {self.errormessage}')

    @staticmethod
    def inspect_exception() -> tuple:

        """Inspects the caller frame of the expcetion to determine the location
        in the code where it has been called.

        This function should be called in the constructor of the top level
        of the derived exception to generate the proper location info.

        Returns:
            The function returns three values, the first is the filename where
            the exception constructor was called, the second is the function
            that called the exception constructor, and the third is the line
            number of the source file where the exception was created.

        Authors:
            Attila Kovacs
        """

        caller_frame_record = inspect.stack()[2]
        frame = caller_frame_record[0]
        info = inspect.getframeinfo(frame)

        filename = info.filename
        function = info.function
        line = info.lineno

        return filename, function, line
