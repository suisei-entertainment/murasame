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
Contains the unit tests of the Singleton class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import Singleton

@Singleton
class TestSingletonObject:

    """
    Basic test singleton.

    Authors:
        Attila Kovacs
    """

    def __init__(self):

        self.testvalue = 'test'

    def testfunction(self):

        """
        Simple test function to test function calling on the singleton.

        Authors:
            Attila Kovacs
        """

        self.testvalue = 'modified'

class TestSingleton:

    """
    Test suite for the Singleton annotation.

    Authors:
        Attila Kovacs
    """

    def test_singleton_access_through_instance(self):

        """
        Test accessing the singleton through the instance method.

        Authors: Attila Kovacs
        """

        sut = TestSingletonObject.instance()
        assert sut.testvalue == 'test'

    def test_singleton_instance_outside_instance(self):

        """
        Tests accessing the singleton outside the instance method.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(TypeError):
            sut = TestSingletonObject()

    def test_singleton_function_call(self):

        """
        Test calling functions on the singleton.

        Authors:
            Attila Kovacs
        """

        sut = TestSingletonObject.instance()
        sut.testfunction()
        assert sut.testvalue == 'modified'

    def test_singleton_instance_check(self):

        """
        Test the instance check functionality of the Singleton.

        Authors:
            Attila Kovacs
        """

        sut = TestSingletonObject.instance()
        assert isinstance(sut, TestSingletonObject)
