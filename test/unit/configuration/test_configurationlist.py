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
Contains the unit tests of the ConfigurationList class.
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
from murasame.configuration.configurationlist import ConfigurationList

# Test data
SIMPLE_VALUE_LIST = \
[
    1,2,3
]

SIMPLE_GROUP_LIST = \
[
    {
        'name': 'element1'
    },
    {
        'name': 'element2'
    }
]

EMPTY_LIST = []

GROUP_LIST_WITH_DUPLICATES = \
[
    {
        'name': 'element1'
    },
    {
        'name': 'element1'
    }
]

MALFORMED_GROUP_LIST = \
[
    {
        'name': 'element1'
    },
    {
        'test': 'element2'
    }
]

class TestConfigurationList:

    """
    Test suite for the ConfgurationList class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests the creation of the configuration list.

        Authors:
            Attila
        """

        # STEP #1 - List with values can be created
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.Name == 'test'
        assert sut.Type == 'VALUE'

        # STEP #2 - List with groups can be created
        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.Type == 'GROUP'

        # STEP #3 - Empty list can be created
        sut = ConfigurationList(name='test', content=EMPTY_LIST)
        assert sut.Type == 'EMPTY'

        # STEP #4 - List with duplicate groups can be created
        sut = ConfigurationList(name='test',
                                content=GROUP_LIST_WITH_DUPLICATES)
        assert sut.Type == 'GROUP'
        assert sut.get_group('element1') is not None

        # STEP #5 - Malformed group list can be created
        sut = ConfigurationList(name='test',
                                content=MALFORMED_GROUP_LIST)
        assert sut.Type == 'GROUP'
        assert sut.get_group('element1') is not None
        assert sut.get_group('element2') is None

    def test_value_retrieval(self):

        """
        Tests that values can be retrieved from the list.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Values can be retrieved from a value list
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.get_value(1) == 2

        # STEP #2 - Groups cannot be retrieved from a value list
        with pytest.raises(RuntimeError):
            sut.get_group('test')

        # STEP #3 - Out of bounds values cannot be retrieved
        with pytest.raises(InvalidInputError):
            sut.get_value(999)

    def test_group_retrieval(self):

        """
        Tests that configuration groups can be retrieved from the list.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Groups can be retrieved from a group list
        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.get_group('element1') is not None

        # STEP #2 - Values cannot be retrieved from a group list
        with pytest.raises(RuntimeError):
            sut.get_value(1)

        # STEP #3 - Non-existing groups cannot be retrieved
        assert sut.get_group('Non-existing') is None

    def test_content_retrieval(self):

        """
        Tests that the raw content of the list can be retrieved

        Authors:
            Attila Kovacs
        """

        # STEP #1 - The content of a value list can be retrieved
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.get_content() == SIMPLE_VALUE_LIST

        # STEP #2 - The content of a group list can be retrieved
        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.get_content()['element1'].Name == 'element1'
        assert sut.Content['element2'].Name == 'element2'

        # STEP #3 - The content of an empty list can be retrieved
        sut = ConfigurationList(name='test', content=EMPTY_LIST)
        assert sut.get_content() is None

    def test_merging_lists(self):

        """
        Tests that configuration lists can be merged.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Value lists can be merged
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut.merge_with(ConfigurationList(name='test',
                                         content=SIMPLE_VALUE_LIST))
        assert sut.NumElements == 6

        # STEP #2 - Group lists can be merged
        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.NumElements == 2
        sut.merge_with(ConfigurationList(name='test',
                                         content=SIMPLE_GROUP_LIST))
        assert sut.NumElements == 2

        # STEP #3 - List cannot be merged with an invalid list
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut.merge_with(None)
        assert sut.NumElements == 3

        # STEP #4 - List cannot be merged with a list of a different type
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut2 = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        sut.merge_with(sut2)
        assert sut.NumElements == 3

        # STEP #5 - List cannot be merged with a list with different name
        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut2 = ConfigurationList(name='test2', content=SIMPLE_VALUE_LIST)
        sut.merge_with(sut2)
        assert sut.NumElements == 3

    def test_string_conversion(self):

        """
        Tests that groups has a correct string representation.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert str(sut) == 'test'
        assert sut.__repr__() == 'test'
