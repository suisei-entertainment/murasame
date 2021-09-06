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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.configuration.configurationattribute import ConfigurationAttribute

class TestConfigurationAttribute:

    """Contains the unit tests of the ConfigurationAttribute class.

    Authors:
        Attila Kovacs
    """

    def test_string_attribute_creation(self) -> None:

        """Tests that a string type configuration attribute can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 'test', 'STRING')
        assert sut.Name == 'test'
        assert sut.Value == 'test'
        assert sut.Type == 'STRING'

    def test_integer_attribute_creation(self) -> None:

        """Tests that an integer type configuration attribute can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')
        assert sut.Name == 'test'
        assert sut.Value == 1
        assert sut.Type == 'INT'

    def test_float_attribute_creation(self) -> None:

        """Tests that a floating point type configuration attribute can be
        created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        assert sut.Name == 'test'
        assert sut.Value == 1.0
        assert sut.Type == 'FLOAT'

    def test_assigning_string_to_a_string_attribute(self) -> None:

        """Tests that a string can be assinged to a string type configuration
        attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 'test', 'STRING')
        sut.Value = 'testtest'
        assert sut.Value == 'testtest'

    def test_assigning_integer_to_a_string_attribute(self) -> None:

        """Tests that an integer value can be assigned to a string type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 'test', 'STRING')
        sut.Value = 1
        assert sut.Value == '1'

    def test_assigning_float_to_a_string_attribute(self) -> None:

        """Tests that a floating point value can be assigned to a string type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 'test', 'STRING')
        sut.Value = 1.0
        assert sut.Value == '1.0'

    def test_assigning_integer_to_an_integer_attribute(self) -> None:

        """Tests that an integer value can be assigned to an integer type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')
        sut.Value = 2
        assert sut.Value == 2

    def test_assigning_string_containing_integer_to_an_integer_attribute(self) -> None:

        """Tests that a string containing an integer value can be assigned to an
        integer type configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')
        sut.Value = '5'
        assert sut.Value == 5

    def test_assigning_string_containing_float_to_an_integer_attribute(self) -> None:

        """Tests that a string containing a floating point value can be
        assigned to an integer type configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')
        sut.Value = '7.5'
        assert sut.Value == 7

    def test_simple_string_cannot_be_assigned_to_an_integer_attribute(self) -> None:

        """Tests that a simple string cannot be assigned to an integer type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')
        with pytest.raises(InvalidInputError):
            sut.Value = 'test'

    def test_assigning_float_to_an_integer_attribute(self) -> None:

        """Tests that floating point attributes can be assigned to an integer
        type configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1, 'INT')

        sut.Value = 3.0
        assert sut.Value == 3

        sut.Value = 4.1
        assert sut.Value == 4

        sut.Value = 6.6
        assert sut.Value == 6

    def test_assigning_float_to_a_float_attribute(self) -> None:

        """Tests that floating point value can be assigned to a float type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        sut.Value = 2.0
        assert sut.Value == 2.0

    def test_assigning_string_containing_float_to_a_float_attribute(self) -> None:

        """Tests that a string containing a floating point value can be assigned
        to a float type configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        sut.Value = '5.0'
        assert sut.Value == 5.0

    def test_assigning_string_containing_int_to_a_float_attribute(self) -> None:

        """Tests that a string containing an integer value can be assigned to a
        float type configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        sut.Value = '7'
        assert sut.Value == 7.0

    def test_simple_string_cannot_be_assigned_to_a_float_attribute(self) -> None:

        """Tests that a simple string cannot be assigned to a float type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')

        with pytest.raises(InvalidInputError):
            sut.Value = 'test'

    def test_assigning_integer_value_to_a_float_attribute(self) -> None:

        """Tests that an integer value can be assigned to a float type
        configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 1.0, 'FLOAT')
        sut.Value = 5
        assert sut.Value == 5.0

    def test_string_conversion(self) -> None:

        """Tests converting the configuration attribute to its string
        representation.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationAttribute('test', 'test', 'STRING')
        text = '{}'.format(sut)
        assert text == 'test : STRING = test'
        text = '{}'.format(sut.__repr__())
        assert text == 'test : STRING = test'
