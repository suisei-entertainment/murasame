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

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.application import Application, BusinessLogic, ApplicationReturnCodes

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

        pass

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
