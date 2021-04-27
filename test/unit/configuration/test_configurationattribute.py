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
Contains the unit tests for the ConfigurationAttribute class.
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
from murasame.configuration.configurationattribute import ConfigurationAttribute

class TestConfigurationAttribute:

    """
    Contains the unit tests of the ConfigurationAttribute class.
    """

    def test_creation(self):

        """
        Tests the creation of the configuration attribute.

        Authors:
            Attila Kovacs
        """

        # STEP 1 - Test creating a string type attribute
        sut = ConfigurationAttribute('test', 'test', 'STRING')
        assert sut.Name == 'test'
        assert sut.Value == 'test'
        assert sut.Type == 'STRING'

        # STEP 2 - Test creating an integer attribute
        sut = ConfigurationAttribute('test', 1, 'INT')
        assert sut.Name == 'test'
        assert sut.Value == 1
        assert sut.Type == 'INT'

        # STEP 3 - Test creating a floating point attribute
        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        assert sut.Name == 'test'
        assert sut.Value == 1.0
        assert sut.Type == 'FLOAT'

    def test_assignment(self):

        """
        Tests assigning values to the configuration attribute.

        Authors:
            Attila Kovacs
        """

        # STEP 1 - Test assigning value to a string attribute
        sut = ConfigurationAttribute('test', 'test', 'STRING')
        sut.Value = 'testtest'
        assert sut.Value == 'testtest'

        # STEP 2 - Test assigning integer to a string attribute
        sut.Value = 1
        assert sut.Value == '1'

        # STEP 3 - Test assigning float to a string attribute
        sut.Value = 1.0
        assert sut.Value == '1.0'

        # STEP 4 - Test assigning value to an integer attribute
        sut = ConfigurationAttribute('test', 1, 'INT')
        sut.Value = 2
        assert sut.Value == 2

        # STEP 5 - Test assigning string to an integer attribute
        sut.Value = '5'
        assert sut.Value == 5

        sut.Value = '7.5'
        assert sut.Value == 7

        with pytest.raises(InvalidInputError):
            sut.Value = 'test'

        # STEP 6 - Test assigning a float to an integer attribute
        sut.Value = 3.0
        assert sut.Value == 3

        sut.Value = 4.1
        assert sut.Value == 4

        sut.Value = 6.6
        assert sut.Value == 6

        # STEP 7 - Test assigning value to a float attribute
        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        sut.Value = 2.0
        assert sut.Value == 2.0

        # STEP 8 - Test assigning string to a float attribute
        sut.Value = '5.0'
        assert sut.Value == 5.0

        sut.Value = '7'
        assert sut.Value == 7.0

        with pytest.raises(InvalidInputError):
            sut.Value = 'test'

        # STEP 9 - Test assigning integer to a float value
        sut.Value = 5
        assert sut.Value == 5.0

    def test_string_conversion(self):

        """
        Tests converting the configuration attribute to its string
        representation.

        Authors:
            Attila Kovacs
        """

        # STEP 1 - Test string conversion
        sut = ConfigurationAttribute('test', 'test', 'STRING')
        text = '{}'.format(sut)
        assert text == 'test : STRING = test'
        text = '{}'.format(sut.__repr__())
        assert text == 'test : STRING = test'
