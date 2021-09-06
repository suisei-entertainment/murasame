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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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

    """Test suite for the ConfgurationList class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_values(self) -> None:

        """Tests the creation of the configuration list from values.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.Name == 'test'
        assert sut.Type == 'VALUE'

    def test_creation_with_groups(self) -> None:

        """Tests the creation of the configuration list from configuration
        groups.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.Type == 'GROUP'

    def test_creation_of_empty_list(self) -> None:

        """Tests that an empty configuration list can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=EMPTY_LIST)
        assert sut.Type == 'EMPTY'

    def test_creation_with_duplicate_groups(self) -> None:

        """Tests that a configuration list with duplicate groups can be
        created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test',
                                content=GROUP_LIST_WITH_DUPLICATES)
        assert sut.Type == 'GROUP'
        assert sut.get_group('element1') is not None

    def test_creation_of_list_with_malformed_group(self) -> None:

        """Tests that a configuration list with a malformed group configuration
        can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test',
                                content=MALFORMED_GROUP_LIST)
        assert sut.Type == 'GROUP'
        assert sut.get_group('element1') is not None
        assert sut.get_group('element2') is None

    def test_value_retrieval_from_value_list(self) -> None:

        """Tests that values can be retrieved from the list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.get_value(1) == 2

    def test_group_cannot_be_retrieved_from_value_list(self) -> None:

        """Tests that a group cannot be retrieved from a value list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        with pytest.raises(RuntimeError):
            sut.get_group('test')

    def test_out_of_bounds_value_retrieval(self) -> None:

        """Tests that out of bounds values cannot be retrieved from a
        configuration list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        with pytest.raises(InvalidInputError):
            sut.get_value(999)

    def test_group_retrieval(self) -> None:

        """Tests that configuration groups can be retrieved from the list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.get_group('element1') is not None

    def test_values_cannot_be_retrieved_from_group_list(self) -> None:

        """Tests that values cannot be retrieved from the configuration list
        that contains groups.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        with pytest.raises(RuntimeError):
            sut.get_value(1)


    def test_retrieval_of_non_existing_groups_from_list(self) -> None:

        """Tests that non-existing groups cannot be retrieved from a
        configuration list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.get_group('Non-existing') is None

    def test_content_retrieval_from_value_list(self) -> None:

        """Tests that the raw content of a value list can be retrieved.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert sut.get_content() == SIMPLE_VALUE_LIST

    def test_content_retrieval_from_group_list(self) -> None:

        """Tests that the content of a configuration group can be retrieved
        from a group list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.get_content()['element1'].Name == 'element1'
        assert sut.Content['element2'].Name == 'element2'

    def test_content_retrieval_from_empty_list(self) -> None:

        """Tests that content can be retrieved from a configuration list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=EMPTY_LIST)
        assert sut.get_content() is None

    def test_merging_value_lists(self) -> None:

        """Tests that configuration lists containing values can be merged.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut.merge_with(ConfigurationList(name='test',
                                         content=SIMPLE_VALUE_LIST))
        assert sut.NumElements == 6

    def test_merging_group_lists(self) -> None:

        """Tests that configuration lists containing groups can be merged.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        assert sut.NumElements == 2
        sut.merge_with(ConfigurationList(name='test',
                                         content=SIMPLE_GROUP_LIST))
        assert sut.NumElements == 2

    def test_merging_with_invalid_list(self) -> None:

        """Tests that a configuration list cannot be merged with an invalid
        list.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut.merge_with(None)
        assert sut.NumElements == 3

    def test_merging_lists_with_different_types(self) -> None:

        """Tests that configuration lists with different types cannot be
        merged.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut2 = ConfigurationList(name='test', content=SIMPLE_GROUP_LIST)
        sut.merge_with(sut2)
        assert sut.NumElements == 3

    def test_merging_lists_with_different_name(self) -> None:

        """Tests that configuration lists with different names cannot be
        merged.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        sut2 = ConfigurationList(name='test2', content=SIMPLE_VALUE_LIST)
        sut.merge_with(sut2)
        assert sut.NumElements == 3

    def test_string_conversion(self) -> None:

        """Tests that groups has a correct string representation.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationList(name='test', content=SIMPLE_VALUE_LIST)
        assert str(sut) == 'test'
        assert sut.__repr__() == 'test'
