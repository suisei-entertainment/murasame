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
FRAMEWORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, FRAMEWORK_DIR)

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.application import Application, BusinessLogic, ApplicationReturnCodes

TEST_DAEMON = \
"""
#!$shebang

import os
import sys
import time
import logging

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.application import Application, BusinessLogic
from murasame.logging import LogLevels

TEST_FILE_1 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest1.txt'))
TEST_FILE_2 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest2.txt'))

class TestDaemon(BusinessLogic):

    @property
    def WorkingDirectory(self):
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon'))

    def main_loop(*argc, **argv):
        with open(TEST_FILE_1, 'w') as file:
            file.write('test')

if __name__ == '__main__':
    print('Creating application...')
    app = Application(business_logic=TestDaemon())
    app.overwrite_log_level(new_log_level=LogLevels.DEBUG)
    print('Starting application...')
    for entry in app._cache:
        print(entry.Message)
    app.start()
    print('Stopping application...')
    for entry in app._cache:
        print(entry.Message)
    app.stop()
    print('Restarting application...')
    for entry in app._cache:
        print(entry.Message)
    app.restart()
    print('Application logs:')
    for entry in app._cache:
        print(entry.Message)
"""

TEST_DAEMON = Template(TEST_DAEMON).substitute(
    shebang=os.path.abspath(os.path.expanduser('~/.murasame/.env/bin/python')),
    framework_dir=FRAMEWORK_DIR)

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

    """
    Contains the unit tests of the Application class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/')))

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/config'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/config')))

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest2/'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest2/')))

    @classmethod
    def teardown_class(cls):

        return

    def test_creation_with_valid_business_logic(self):

        """
        Tests that an application can be created.

        Authors:
            Attila Kovacs
        """

        sut = Application(business_logic=DummyBusinessLogic())

    def test_creation_without_business_logic(self):

        """
        Tests that an application cannot be created without a valid business
        logic.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=None)

    def test_creation_without_working_directory(self):

        """
        Tests that an application cannot be created without a valid working
        directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=DummyBusinessLogicInvalidWorkingDirectory())

    def test_creation_without_config_directory(self):

        """
        Tests that an application cannot be created without a valid config
        subdirectory in its working directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=DummyBusinessLogicNoConfig())

    def test_daemon_application(self):

        """
        Tests that the application can operate as a Unix daemon.

        Authors:
            Attila Kovacs
        """

        base_dir = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon'))

        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        else:
            if os.path.isfile(f'{base_dir}/daemontest1.txt'):
                os.remove(f'{base_dir}/daemontest1.txt')

        if not os.path.isdir(f'{base_dir}/config'):
            os.mkdir(f'{base_dir}/config')

        with open(f'{base_dir}/daemon.py', 'w') as file:
            file.write(TEST_DAEMON)
            os.chmod(f'{base_dir}/daemon.py', 0o777)

        current_dir = os.getcwd()
        os.chdir(base_dir)
        try:
            process = subprocess.run(f'python daemon.py', shell=True, check=False)
            if not process.returncode == ApplicationReturnCodes.SUCCESS:
                return False
        except subprocess.CalledProcessError:
           assert False

        os.chdir(current_dir)

        assert os.path.isfile(f'{base_dir}/daemontest1.txt')

    def test_daemon_sigterm_signals(self):

        """
        Tests that the daemon application can handle the SIGTERM signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigint_signals(self):

        """
        Tests that the daemon application can handle the SIGINT signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigalrm_signals(self):

        """
        Tests that the daemon application can handle the SIGALRM signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigusr1_signals(self):

        """
        Tests that the daemon application can handle the SIGUSR1 signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_daemon_sigusr2_signals(self):

        """
        Tests that the daemon application can handle the SIGUSR2 signal.

        Authors:
            Attila Kovacs
        """

        # TODO

        pass

    def test_return_code_after_successful_execution(self):

        """
        Tests that the application returns SUCCESS return code upon successful
        execution.

        Authors:
            Attila Kovacs
        """

        sut = Application(business_logic=DummyBusinessLogic())
        assert sut.execute() == ApplicationReturnCodes.SUCCESS

    def test_return_code_on_uncaught_exception(self):

        """
        Tests that the application returns UNCAUGHT_EXCEPTION return code
        when an unhandled exception is encountered.

        Authors:
            Attila Kovacs
        """

        sut = Application(business_logic=DummyBusinessLogicThrowingException())
        assert sut.execute() == ApplicationReturnCodes.UNCAUGHT_EXCEPTION
