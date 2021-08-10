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
Contains the implementation of the BusinessLogic class.
"""

# Runtime Imports
import os
from typing import Callable, Union

# Murasame Imports
from murasame.application.applicationreturncodes import ApplicationReturnCodes

class BusinessLogic:

    """Common base class for business logic implementations.

    Authors:
        Attila Kovacs
    """

    @property
    def IsLicenseRequired(self) -> bool:

        """Whether or not a valid license is required to start the application.

        Authors:
            Attila Kovacs
        """

        return False

    @property
    def LicensePublicKey(self) -> Union[str, None]:

        """Path to the public key used to validate the license.

        Authors:
            Attila Kovacs
        """

        return None

    @property
    def LicenseFile(self) -> Union[str, None]:

        """Path to the license file.

        Authors:
            Attila Kovacs
        """

        return None

    @property
    def LicenseDecryptionKeyCallback(self) -> Union[Callable, None]:

        """Callback to be used when accessing the key to the license file.

        Authors:
            Attila Kovacs
        """

        return None

    @property
    def UseSentryIO(self) -> bool:

        """Whether or not Sentry.IO is used by the application.

        Authors:
            Attila Kovacs
        """

        return False

    @property
    def SentryDSN(self) -> Union[str, None]:

        """The Sentry DSN to use when sending reports to Sentry.IO.

        Authors:
            Attila Kovacs
        """

        return None

    @property
    def PIDFile(self) -> str:

        """The PID file used by the application.

        Only used for daemon type applications.

        Authors:
            Attila Kovacs
        """

        return 'murasame.pid'

    @property
    def WorkingDirectory(self) -> str:

        """The working directory of the application.

        Authors:
            Attila Kovacs
        """

        return os.getcwd()

    @property
    def Umask(self) -> int:

        """The file mask to be used by files created by the application.

        Only used for daemon type applications.

        Authors:
            Attila Kovacs
        """

        return 0o22

    @property
    def StdIn(self) -> object:

        """The input stream to be used by the application.

        Only used for daemon type applications.

        Authors:
            Attila Kovacs
        """

        return os.devnull

    @property
    def StdOut(self) -> object:

        """The output stream to be used by the application.

        Only used for daemon type applications.

        Authors:
            Attila Kovacs
        """

        return os.devnull

    @property
    def StdErr(self) -> object:

        """The error stream to be used by the application.

        Only used for daemon type applications.

        Authors:
            Attila Kovacs
        """

        return os.devnull

    @property
    def IsVFSDisabled(self) -> bool:

        """Returns whether or not the usage of the VFS has been disabled.

        Authors:
            Attila Kovacs
        """

        return False

    def main_loop(self, *args, **kwargs) -> ApplicationReturnCodes:

        """Implements the main loop of the application.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Returns:
            ApplicationReturnCodes: The overall return code of the application.

            ApplicationReturnCodes.SUCCESS for successful execution, or an
            integer value to indicate issues.

            If the return code is not ApplicationReturnCodes.SUCCESS, then the
            application will quit with this return code.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs
        return ApplicationReturnCodes.SUCCESS

    def before_main_loop(self, *args, **kwargs) -> ApplicationReturnCodes:

        """Function that is called before the application enters its main loop.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Returns:
            ApplicationReturnCodes: Result of the execution of the function.

            If the execution was successful then this function should return
            ApplicationReturnCodes.SUCCESS, otherwise a supported error code.

            If the function return an error, then the application execution
            will not continue, the application will quit with this return code.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs
        return ApplicationReturnCodes.SUCCESS

    def after_main_loop(self, *args, **kwargs) -> ApplicationReturnCodes:

        """Function that is called after the application exited the main loop.

        This function is only called if the application exits the main loop
        with an ApplicationReturnCodes.SUCCESS return code, otherwise the
        application execution will stop and the application will quit the error
        code from the main loop.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs
        return ApplicationReturnCodes.SUCCESS

    def initialize_systems(self) -> None:

        """Initializes the systems used by the application.

        It is called by the application upon initialization.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        return

    def on_uncaught_exception(self, exception: Exception) -> None:

        """Handler function for uncaught exceptions.

        This function will be called every time the application encounters an
        unhandled exception.

        Args:
            exception (Exception): The exception that was not handled properly.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del exception

    def handle_sigterm(self, signum: int, frame: object) -> None:

        """Handler function that is called when SIGTERM is received.

        This function can be overwritten by custom business logic
        implementation of daemon applications to implement some custom logic
        for this signal.

        Args:
            signum (int): The actual signam number that was received.
            frame (object): The current stack frame.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del signum
        del frame

    def handle_sigint(self, signum: int, frame: object) -> None:

        """Handler function that is called when SIGTERM is received.

        This function can be overwritten by custom business logic
        implementation of daemon applications to implement some custom logic
        for this signal.

        Args:
            signum (int): The actual signam number that was received.
            frame (object): The current stack frame.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del signum
        del frame

    def handle_sigalrm(self, signum: int, frame: object) -> None:

        """Handler function that is called when SIGALRM is received.

        This function can be overwritten by custom business logic
        implementation of daemon applications to implement some custom logic
        for this signal.

        Args:
            signum (int): The actual signam number that was received.
            frame (object): The current stack frame.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del signum
        del frame

    def handle_sigusr1(self, signum: int, frame: object) -> None:

        """Handler function that is called when SIGUSR1 is received.

        This function can be overwritten by custom business logic
        implementation of daemon applications to implement some custom logic
        for this signal.

        Args:
            signum (int): The actual signam number that was received.
            frame (object): The current stack frame.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del signum
        del frame

    def handle_sigusr2(self, signum: int, frame: object) -> None:

        """Handler function that is called when SIGUSR2 is received.

        This function can be overwritten by custom business logic
        implementation of daemon applications to implement some custom logic
        for this signal.

        Args:
            signum (int): The actual signam number that was received.
            frame (object): The current stack frame.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del signum
        del frame

    def before_sentry_send(self, event: object, hint: object) -> object:

        """Handler function called before a Sentry report is sent.

        Args:
            event (object): The event that is being captured.
            hint (object): Additional hint data.

        Returns:
            The modified event.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del hint
        return event
