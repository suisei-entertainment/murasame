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

# Framework Imports
from .errorcodes import ErrorCodes

class FrameworkError(Exception):

    """
    The base class for all Murasame framework errors.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 message: str = '',
                 errorcode: int = ErrorCodes.NOT_SET,
                 package: str = __package__,
                 file: str = '',
                 line: str = '',
                 function: str = '',
                 wrapped_exception: Exception = None,
                 inspect_caller: bool = True) -> None:

        """
        Creates a new Exception instance.

        Args:
            message:            The user message that clarifies the exception.
            errorcode:          The platform errorcode that identifies the
                                actual error.
            package:            Name of the Python package that raised the
                                exception.
            file:               Name of the source file where the exception was
                                raised.
            line:               The line number in the source code where the
                                exception was raised.
            function:           Name of the funtion that raised the exception.
            wrapped_exception:  Another, non-SEED exception that is wrapped
                                inside the SEED exception.
            inspect_caller:     Whether or not the caller should be inspected
                                to retrieve the raising location of the
                                exception. Should only be True in the topmost
                                exception in the inheritance tree, otherwise
                                should be passed down as False.

        Authors:
            Attila Kovacs
        """

        super().__init__(message)

        self.errorcode = errorcode
        """
        The platform error code that identifies the exact issue.
        """

        self.errormessage = message
        """
        Custom error message specified by the user when raising the exception.
        """

        self.package = package
        """
        Name of the package that raised the expcetion.
        """

        self.file = file
        """
        Name of the source file where the exception was raised.
        """

        self.line = line
        """
        The source line where the exception has been raised.
        """

        self.function = function
        """
        The function that raised the exception.
        """

        self.wrapped_exception = wrapped_exception
        """
        An exception that was asked to be wrapped within a SEED exception.
        """

        # When inspect_caller is set to True, then the caller function will be
        # inspected to retrieve the correct location of where the exception
        # was raised.
        if inspect_caller:
            self.file, self.function, self.line = self.inspect_exception()

        # Log the exception
        logger = logging.getLogger('murasame.exceptions')
        logger.error(f'Framework exception was raised. '
                     f'Type: {self.__class__.__name__}\n'
                     f'Error Code: {self.errorcode}\n'
                     f'Package: {self.package}\n'
                     f'Location: {self.file} (line {self.line})\n'
                     f'Function: {self.function}()\n'
                     f'Message: {self.errormessage}')

    @staticmethod
    def inspect_exception() -> tuple:

        """
        Inspects the caller frame of the expcetion to determine the location
        in the code where it has been called.

        This function should be called in the constructor of the top level
        of the derived exception to generate the proper location info.

        Returns:
            The function returns three values, the first is the filename where
            the exception constructor was called, the second is the function
            that called the exception constructor, and the third is the line
            number of the source file where the exception was created.
        """

        caller_frame_record = inspect.stack()[2]
        frame = caller_frame_record[0]
        info = inspect.getframeinfo(frame)

        filename = info.filename
        function = info.function
        line = info.lineno

        return filename, function, line
