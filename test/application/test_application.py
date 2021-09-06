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
Contains the unit tests for the Application class.
"""

# Platform Imports
import os
import sys
import subprocess
from string import Template

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
FRAMEWORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, FRAMEWORK_DIR)

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.application import Application, BusinessLogic, ApplicationReturnCodes, ApplicationTypes

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

class DummyBusinessLogic(BusinessLogic):

    @property
    def WorkingDirectory(self) -> str:
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/'))

class DummyBusinessLogicInvalidWorkingDirectory(BusinessLogic):

    @property
    def WorkingDirectory(self) -> str:
        return os.path.abspath(os.path.expanduser('/invalid/path'))

class DummyBusinessLogicNoConfig(BusinessLogic):

    @property
    def WorkingDirectory(self) -> str:
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest2/'))

class DummyBusinessLogicThrowingException(BusinessLogic):

    @property
    def WorkingDirectory(self) -> str:
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/'))

    def before_main_loop(self, *args, **kwargs) -> ApplicationReturnCodes:
        raise RuntimeError

class TestApplication:

    """Contains the unit tests of the Application class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_valid_business_logic(self) -> None:

        """Tests that an application can be created.

        Authors:
            Attila Kovacs
        """

        business_logic = DummyBusinessLogic()
        sut = Application(business_logic=business_logic)
        assert sut.BusinessLogic == business_logic
        assert sut.Type == ApplicationTypes.DAEMON_APPLICATION

    def test_creation_without_business_logic(self) -> None:

        """Tests that an application cannot be created without a valid business
        logic.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=None)

    def test_creation_without_working_directory(self) -> None:

        """Tests that an application cannot be created without a valid working
        directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(
                business_logic=DummyBusinessLogicInvalidWorkingDirectory())

    def test_creation_without_config_directory(self) -> None:

        """Tests that an application cannot be created without a valid config
        subdirectory in its working directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=DummyBusinessLogicNoConfig())

    def test_daemon_application(self) -> None:

        """Tests that the application can operate as a Unix daemon.

        Authors:
            Attila Kovacs
        """

        daemon_path = f'{TEST_FILES_DIRECTORY}/daemon'

        try:
            process = subprocess.run(f'python {daemon_path}/daemon.py',
                                    shell=True,
                                     check=False)
            if not process.returncode == ApplicationReturnCodes.SUCCESS:
                return False
        except subprocess.CalledProcessError:
           assert False

        assert os.path.isfile(f'{daemon_path}/daemontest1.txt')

    def test_daemon_sigterm_signals(self) -> None:

        """Tests that the daemon application can handle the SIGTERM signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigint_signals(self) -> None:

        """Tests that the daemon application can handle the SIGINT signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigalrm_signals(self) -> None:

        """Tests that the daemon application can handle the SIGALRM signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigusr1_signals(self) -> None:

        """Tests that the daemon application can handle the SIGUSR1 signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigusr2_signals(self) -> None:

        """Tests that the daemon application can handle the SIGUSR2 signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_return_code_after_successful_execution(self) -> None:

        """Tests that the application returns SUCCESS return code upon
        successful execution.

        Authors:
            Attila Kovacs
        """

        sut = Application(business_logic=DummyBusinessLogic())
        assert sut.execute() == ApplicationReturnCodes.SUCCESS

    def test_return_code_on_uncaught_exception(self) -> None:

        """Tests that the application returns UNCAUGHT_EXCEPTION return code
        when an unhandled exception is encountered.

        Authors:
            Attila Kovacs
        """

        sut = Application(business_logic=DummyBusinessLogicThrowingException())
        assert sut.execute() == ApplicationReturnCodes.UNCAUGHT_EXCEPTION
