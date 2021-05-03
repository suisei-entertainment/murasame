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

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.application import Application, BusinessLogic

TEST_FILE_1 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest1.txt'))
TEST_FILE_2 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest2.txt'))

class TestDaemon(BusinessLogic):

    @property
    def WorkingDirectory(self):
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon'))

    def main_loop(*argc, **argv):
        if os.path.isfile(TEST_FILE_1):
            with open(TEST_FILE_2, 'w') as file:
                file.write('test')
        else:
            with open(TEST_FILE_1, 'w') as file:
                file.write('test')

if __name__ == '__main__':
    app = Application(business_logic=TestDaemon())
    app.start()
    app.stop()
    app.restart()
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
    """

    @classmethod
    def setup_class(cls):

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/')))

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/config'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest/config')))

        if not os.path.isdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest2/'))):
            os.mkdir(os.path.abspath(os.path.expanduser('~/.murasame/testfiles/apptest2/')))

    def test_creation(self):

        """
        Tests that an application can be created.
        """

        # STEP #1 - Application with a valid business logic can be created
        sut = Application(business_logic=DummyBusinessLogic())

        # STEP #2 - Application cannot be created without business logic
        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=None)

        # STEP #3 - Application cannot be created without a valid working
        #           directory.
        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=DummyBusinessLogicInvalidWorkingDirectory())

        # STEP #4 - The working directory of the application must contain a
        #           config subdirectory.
        with pytest.raises(InvalidInputError):
            sut = Application(business_logic=DummyBusinessLogicNoConfig())

    def test_daemon_application(self):

        """
        Tests that the application can operate as a Unix daemon.
        """

        base_dir = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon'))

        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        else:
            if os.path.isfile(f'{base_dir}/daemontest1.txt'):
                os.remove(f'{base_dir}/daemontest1.txt')
            if os.path.isfile(f'{base_dir}/daemontest2.txt'):
                os.remove(f'{base_dir}/daemontest2.txt')

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
        assert os.path.isfile(f'{base_dir}/daemontest2.txt')

    def test_daemon_signals(self):

        """
        Tests that the daemon application can handle standard OS signals.
        """

        pass

    def test_execution(self):

        """
        Tests the basic execution logic of the application.
        """

        # STEP #1 - Test basic application return type
        sut = Application(business_logic=DummyBusinessLogic())
        assert sut.execute() == ApplicationReturnCodes.SUCCESS

        # STEP #2 - Test uncaught exception handling
        sut = Application(business_logic=DummyBusinessLogicThrowingException())
        assert sut.execute() == ApplicationReturnCodes.UNCAUGHT_EXCEPTION
