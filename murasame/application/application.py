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
Contains the implementation of the Application class.
"""

# Runtime Imports
import sys
import os
import time
import signal
import errno
import platform
import atexit
from typing import Callable, Union

# Dependency Imports
import sentry_sdk

# Murasame Imports
from murasame.constants import MURASAME_APPLICATION_LOG_CHANNEL
from murasame.api import LoggingAPI, ConfigurationAPI, VFSAPI, ApplicationAPI
from murasame.exceptions import InvalidInputError, InvalidLicenseKeyError
from murasame.log import LogWriter, LoggingSystem
from murasame.licensing import LicenseValidator
from murasame.utils import SystemLocator
from murasame.application.applicationreturncodes import ApplicationReturnCodes
from murasame.application.businesslogic import BusinessLogic
from murasame.application.applicationtypes import ApplicationTypes
from murasame.configuration import Configuration
from murasame.pal.vfs import VFS

class Application(LogWriter):

    """Basic application implementation containing fundamental functionalities.

    The Unix daemon  implementation is based on the python-daemon
    implementation at https://github.com/serverdensity/python-daemon which is
    derived from http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/www.boxedice.com

    Attributes:

        _business_logic (BusinessLogic): The business logic of the application.

        _type (ApplicationTypes): The type of the application.

        _alive (bool): Whether or not the application is running. Only used for
            daemon applications.

    Authors:
        Attila Kovacs
    """

    @property
    def BusinessLogic(self) -> 'BusinessLogic':

        """The business logic of the application.

        Authors:
            Attila Kovacs
        """

        return self._business_logic

    @property
    def Type(self) -> 'ApplicationTypes':

        """The type of the application.

        Authors:
            Attila Kovacs
        """

        return  self._type

    def __init__(
        self,
        business_logic: 'BusinessLogic',
        application_type: 'ApplicationTypes' = ApplicationTypes.DAEMON_APPLICATION) -> None:

        """Creates a new Application instance.

        Args:
            business_logic (BusinessLogic): The business logic implementation
                of the application.

            application_type (ApplicationTypes): The type of application to
                create.

        Raises:
            InvalidInputError:  Raised if the provided business logic is
                invalid.

            InvalidInputError:  Raised if the working directory specified by
                the business logic doesn't exist.

            InvalidInputError:  Raised if the working directory specified by
                the business logic doesn't have a configuration subdirectory.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_APPLICATION_LOG_CHANNEL,
                         cache_entries=True)

        self._business_logic = business_logic
        self._type = application_type
        self._alive = False

        # Validate business logic
        self.debug('Validating business logic...')

        if not business_logic or not isinstance(business_logic, BusinessLogic):
            raise InvalidInputError('A valid business logic implementation '
                                    'has to be provided for an application.')

        root_directory = business_logic.WorkingDirectory

        if not os.path.isdir(root_directory):
            raise InvalidInputError(
                f'The provided working directory {root_directory} does not '
                f'exist.')

        if not os.path.isdir(f'{root_directory}/config'):
            raise InvalidInputError(
                f'The provided working directory {root_directory} does not '
                f'contain a configuration subdirectory.')

        self.info('Business logic has been validated successfully.')

        # Enter the specified working directory
        os.chdir(root_directory)

        # Validate license if required
        if business_logic.IsLicenseRequired:
            self._validate_license(
                public_key=business_logic.LicensePublicKey,
                license_file=business_logic.LicenseFile,
                cb_decryption_key_callback=business_logic.LicenseDecryptionKeyCallback)

        # Initialize Sentry.IO
        if business_logic.UseSentryIO:
            self.debug('Initializing Sentry SDK...')
            # False positive, Pylint thinks sentry_sdk.init() is an abstract
            # class.
            #pylint: disable=abstract-class-instantiated
            sentry_sdk.init(dsn=business_logic.SentryDSN,
                            before_send=business_logic.before_sentry_send)
            self.info('Sentry SDK has been initialized.')

        # Pylint doesn't recognize the instance() method of Singleton.
        #pylint: disable=no-member

        # Initialize the log system
        self.info('Initializing log system...')
        logging_system = LoggingSystem()
        SystemLocator.instance().register_provider(LoggingAPI, logging_system)

        if not business_logic.IsVFSDisabled:

           # Initialize the VFS
            self.debug('Initializing the virtual file system...')
            vfs = VFS()
            SystemLocator.instance().register_provider(VFSAPI, vfs)
            vfs.register_source(path=business_logic.WorkingDirectory)
            self.info('Virtual file system has been initialized.')

            # Load the configuration
            self.debug('Loading the configuration...')
            configuration = Configuration()
            SystemLocator.instance().register_provider(
                ConfigurationAPI, configuration)
            configuration.load()
            self.info('Configuration has been loaded.')

        else:
            self.info('The virtual file system has been disabled.')

        # Initialize systems
        self.debug('Initializing application systems...')
        business_logic.initialize_systems()
        self.info('Application systems initialized successfully.')

        # Publish the application in the system locator.
        SystemLocator.instance().register_provider(
            ApplicationAPI, self)

    def execute(self, *args: list, **kwargs: dict) -> int:

        """Contains the main execution logic of the application.

        Args:
            *args:          List of unnamed arguments.
            **kwargs:       List of named arguments.

        Returns:
            The overall return code of the application.

        Authors:
            Attila Kovacs
        """

        result = ApplicationReturnCodes.SUCCESS

        # Catching every uncaught exception here is intentional so that
        # the applications can react to it and to also set the proper
        # exit code of the application.
        #pylint: disable=broad-except

        try:
            result = self._business_logic.before_main_loop(args, kwargs)
            result = self._business_logic.main_loop(args, kwargs)
            result = self._business_logic.after_main_loop(args, kwargs)
        except SystemExit:
            # Delete the PID file of daemon applications before exiting
            # to avoid leftover files.
            if self._type == ApplicationTypes.DAEMON_APPLICATION:
                self.delete_pid()
            raise
        except Exception as error:
            self._business_logic.on_uncaught_exception(error)
            if self._business_logic.UseSentryIO:
                sentry_sdk.capture_exception(error)
            return ApplicationReturnCodes.UNCAUGHT_EXCEPTION

        if self._type == ApplicationTypes.DAEMON_APPLICATION:
            self.warning(
                'Leaving the main loop of a daemon application, cleaning up.')
            self.delete_pid()

        return result

    def start(self, *args: list, **kwargs: list) -> None:

        """Starts the application as a daemon.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Authors:
            Attila Kovacs
        """

        if self._type != ApplicationTypes.DAEMON_APPLICATION:
            return

        # Check the pid file to see if the daemon is already running.
        pid = self.get_pid()

        if pid:
            message = f'PID file {self._business_logic.PIDFile} already '\
                      f'exists. The daemon is already running?'
            sys.stderr.write(message)
            sys.exit(ApplicationReturnCodes.ALREADY_RUNNING)

        # Start the daemon
        self._daemonize()

        pid = self.get_pid()

        if not pid:
            message = 'No PID file was found, daemon has failed to start.'
            sys.stderr.write(message)
            sys.exit(ApplicationReturnCodes.NOT_RUNNING)

        message = f'Daemon created with PID {pid}'
        sys.stdout.write(message)

        self.execute(*args, **kwargs)

    def stop(self) -> None:

        """Stops the daemon.

        Authors:
            Attila Kovacs
        """

        if self._type != ApplicationTypes.DAEMON_APPLICATION:
            return

        print('Trying to stop the daemon...')

        pid = self.get_pid()

        if not pid:
            message = f'PID file {self._business_logic.PIDFile} does not '\
                      f'exist, The daemon is not running?'
            sys.stderr.write(message)
            sys.exit(ApplicationReturnCodes.NOT_RUNNING)

            # Just to be sure. A ValueError might occur if the PID file is
            # empty, but it actually exists
            print('Deleting pid...')
            self.delete_pid()

            # not an error during a restart
            return

        # Try killing the daemon process
        try:
            i = 0
            while 1:
                print('Sending SIGTERM...')
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1) # nosemgrep
                i = i + 1
                if i % 10 == 0:
                    print('Sending SIGHUP...')
                    os.kill(pid, signal.SIGHUP)
        except OSError as error:
            print(error)
            if error.errno == errno.ESRCH:
                print('Deleting PID...')
                self.delete_pid()
            else:
                print(str(error))
                sys.exit(ApplicationReturnCodes.PLATFORM_ERROR)

    def restart(self, *args: list, **kwargs: list) -> None:

        """Restarts the daemon.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Authors:
            Attila Kovacs
        """

        if self._type != ApplicationTypes.DAEMON_APPLICATION:
            return

        self.stop()
        self.start(*args, **kwargs)

    def get_pid(self) -> Union[int, None]:

        """Returns the PID of the running daemon process.

        Returns:
            int: The PID of the running daemon process.

        Authors:
            Attila Kovacs
        """

        if self._type != ApplicationTypes.DAEMON_APPLICATION:
            return None

        pid = None

        try:
            with open(self._business_logic.PIDFile, 'r') as pid_file:
                pid = int(pid_file.read().strip())
        except IOError:
            pid = None
        except SystemExit:
            pid = None
            raise

        return  pid

    def get_status(self) -> str:

        """Returns the current status of the daemon.

        Returns:
            str: A status string reflecting the current status of the daemon.

        Authors:
            Attila Kovacs
        """

        pid = self.get_pid()

        if pid is not None:
            return 'Daemon is running with PID {}'.format(pid)

        return 'Daemon is not running.'

    def is_running(self) -> bool:

        """Returns whether or not the daemon is running.

        Returns:
            bool: 'True' if the daemon process is running, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        pid = self.get_pid()

        if pid is None:
            # Process is stopped
            return False

        if os.path.exists(f'/proc/{pid}'):
            # Process is running
            return True

        # Process is killed
        return False

    def delete_pid(self) -> None:

        """Deletes the PID file.

        Authors:
            Attila Kovacs
        """

        try:
            # The process may fork itself again
            pid = int(open(self._business_logic.PIDFile, 'r').read().strip())
            if pid == os.getpid():
                os.remove(self._business_logic.PIDFile)
        except OSError as error:
            if error.errno == errno.ENOENT:
                pass
            else:
                raise OSError from error

    def _validate_license(
        self,
        public_key: str,
        license_file: str,
        cb_decryption_key_callback: Callable) -> None:

        """Validates the license key of the application.

        Args:
            public_key (str): Path to the public key of the license file.

            license_file (str): Path to the license file of the application.

            cb_decryption_key_callback (Callable): Callback function to
                retrieve the decryption key to the license file.

        Raises:
            InvalidLicenseKey: Raised if the license key is invalid.

        Authors:
            Attila Kovacs
        """

        self.debug('Validating application license...')

        # Create the validator
        validator = LicenseValidator(public_key_path=public_key)

        # Validate the license
        if not validator.validate(
                license_path=license_file,
                cb_retrieve_password=cb_decryption_key_callback):
            raise InvalidLicenseKeyError('License key cannot be verified.')

        self.info('License has been validated successfully.')

    def _daemonize(self) -> None:

        """Daemonizes the process using the Unix double-fork method.

        For details, see Stevens' "Advanced Programming in the UNIX
        Environment" (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16

        Authors:
            Attila Kovacs
        """

        # Daemonization only works on Unix systems, so don't attempt it on
        # Windows
        if platform.system().lower() == 'windows':
            return

        # Execute the first fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as error:
            print(error)
            sys.stderr.write(f'ERROR >> First fork failed. Errno: '
                             f'{error.errno} Error: {error.strerror}')
            sys.exit(1)

        # Decouple from the parent environment
        os.chdir(self.BusinessLogic.WorkingDirectory)
        os.setsid()
        os.umask(self.BusinessLogic.Umask)

        # Execute the second fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit the second fork
                sys.exit(0)
        except OSError as error:
            print(error)
            sys.stderr.write(f'ERROR >> Second fork failed. Errno: '
                             f'{error.errno} Error: {error.strerror}')
            sys.exit(1)

        # Redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()

        # Not closing the streams here is considered an error by Semgrep, but
        # it's a false positive. Pylint also throws a false warning about not
        # using with.

        #pylint: disable=consider-using-with

        std_in = open(self.BusinessLogic.StdIn, 'r') # nosemgrep
        std_out = open(self.BusinessLogic.StdOut, 'a+') # nosemgrep
        std_err = std_out

        if self.BusinessLogic.StdErr is not None:
            std_err = open(self.BusinessLogic.StdErr, 'a+', 1) # nosemgrep

        # Duplicate file descriptors
        os.dup2(std_in.fileno(), sys.stdin.fileno())
        os.dup2(std_out.fileno(), sys.stdout.fileno())
        os.dup2(std_err.fileno(), sys.stderr.fileno())

        # Register signals
        signal.signal(signal.SIGTERM, self.BusinessLogic.handle_sigterm)
        signal.signal(signal.SIGINT, self.BusinessLogic.handle_sigint)
        signal.signal(signal.SIGALRM, self.BusinessLogic.handle_sigalrm)
        signal.signal(signal.SIGUSR1, self.BusinessLogic.handle_sigusr1)
        signal.signal(signal.SIGUSR2, self.BusinessLogic.handle_sigusr2)

        # Make sure that the PID is removed at exit
        atexit.register(self.delete_pid)

        # Retrieve the PID
        pid = str(os.getpid())

        # Write the PID file
        open(self.BusinessLogic.PIDFile, 'w+').write('%s\n' % pid)
