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
Contains the unit tests of the ConfigurationGroup class.
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
from murasame.configuration.configurationgroup import ConfigurationGroup
from murasame.configuration.configurationattribute import ConfigurationAttribute
from murasame.configuration.configurationlist import ConfigurationList

# Test data
SIMPLE_TEST_GROUP = \
{
    'stringvalue': 'test',
    'intvalue': 3,
    'floatvalue': 9.0
}

NESTED_GROUP = \
{
    'name': 'nested',
    'nest':
    {
        'nestedname': 'test2',
        'nestnest':
        {
            'testvalue': 'value'
        }
    }
}

NESTED_GROUP_WITH_LIST = \
{
    'name': 'nested',
    'nest':
    {
        'nestedname': 'test2'
    },
    'list':
    [
        1,2,3
    ]
}

GROUP_WITH_GROUP_LIST = \
{
    'list':
    [
        {
            'name': 'element1'
        },
        {
            'name': 'element2'
        }
    ]
}

SIMPLE_SUBGROUP = \
{
    'name': 'subgroup',
    'testattribute': 'testvalue',
    'test1':
    {
        'nestedattribute': 'nestedvalue'
    },
    'list1':
    [
        1,2,3
    ]
}

SIMPLE_SUBGROUP_2 = \
{
    'name': 'subgroup',
    'testattribute': 'testvalue',
    'testattribute2': 'testvalue2',
    'test1':
    {
        'nestedattribute': 'nestedvalue',
        'nestedattribute2': 'nestedvalue2'
    },
    'test2':
    {
        'nestedattribute3': 'nestedvalue3'
    },
    'list1':
    [
        1,2,3
    ],
    'list2':
    [
        9,10,11
    ]
}

class TestConfigurationGroup:

    """
    Test suite for the ConfgurationGroup class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests the creation of the configuration group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Create simple configuration group
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.Name == 'test'

        # STEP #2 - Create nested configuration group
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.Name == 'nested'

        # STEP #3 - Create configuration group with a list
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.Name == 'nested'

        # STEP #4 - Create configuration group without a name
        sut = ConfigurationGroup(content=SIMPLE_TEST_GROUP)
        assert sut.Name == None

        # STEP #5 - Create an empty configuration group
        sut = ConfigurationGroup(content={})
        assert sut.Name == None

    def test_attribute_retrieval(self):

        """
        Tests that configuration attributes can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Test simple attribute retrieval
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.get_attribute('stringvalue').Value == 'test'
        assert sut.get_attribute('intvalue').Value == 3
        assert sut.get_attribute('floatvalue').Value == 9.0
        assert sut.Attributes is not None
        assert sut.Groups is not None
        assert sut.Lists is not None

        # STEP #2 - Test retrieval from a nested group
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_attribute('nest.nestedname').Value == 'test2'

        # STEP #3 - Test retrieval of non-existing attribute
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.get_attribute('nonexistent') is None

        # STEP #4 - Test retrieval of invalid attribute name
        assert sut.get_attribute('') is None
        assert sut.get_attribute(None) is None

    def test_group_retrieval(self):

        """
        Tests that configuration groups can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Test simple group retrieval
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nest').Name == 'nest'

        # STEP #2 - Test retrieval from a nested group
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nest.nestnest').Name == 'nestnest'

        # STEP #3 - Test retrieval of non-existing group
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nonexistent') is None

        # STEP #4 - Test retrieval of invalid group name
        assert sut.get_group('') is None
        assert sut.get_group(None) is None

    def test_list_retrieval(self):

        """
        Tests that configuration lists can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Test simple list retrieval
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.get_list('list').get_value(0) == 1

        # STEP #2 - Test group list retrieval
        sut = ConfigurationGroup(name='test', content=GROUP_WITH_GROUP_LIST)
        assert sut.get_list('list').get_content()['element1'].Name == 'element1'

        # STEP #3 - Test retrieval of non-existing list
        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.get_group('nonexistent') is None

        # STEP #4 - Test retrieval of invalid list name
        assert sut.get_list('') is None
        assert sut.get_list(None) is None

    def test_adding_attribute(self):

        """
        Tests that an attribute can be added to the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - New attribute can be added to an existing group
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        sut.add_attribute(ConfigurationAttribute(name='newattribute',
                                                 value='testvalue',
                                                 data_type='STRING'))
        assert sut.get_attribute('newattribute').Value =='testvalue'

        # STEP #2 - Invalid attribute cannot be added
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        current_num = sut.NumAttributes
        sut.add_attribute(None)
        assert current_num == sut.NumAttributes

        # STEP #3 - Attribute duplication is prevented
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        sut.add_attribute(ConfigurationAttribute(name='newattribute',
                                                 value='testvalue',
                                                 data_type='STRING'))
        sut.add_attribute(ConfigurationAttribute(name='newattribute',
                                                 value='testvalue2',
                                                 data_type='STRING'))
        assert sut.get_attribute('newattribute').Value == 'testvalue'

    def test_adding_subgroup(self):

        """
        Tests that a subgroup can be added to the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - New subgroup can be added to an existing group
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        subgroup = ConfigurationGroup(name='subgroup', content=SIMPLE_SUBGROUP)
        sut.add_group(subgroup)
        assert sut.get_group('subgroup') is not None

        # STEP #2 - Invalid group cannot be added
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        current_num = sut.NumGroups
        sut.add_group(None)
        assert current_num == sut.NumGroups

        # STEP #3 - Adding a group with the same name as a subgroup results in
        #           a merge
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        subgroup = ConfigurationGroup(name='subgroup', content=SIMPLE_SUBGROUP)
        sut.add_group(subgroup)
        subgroup2 = ConfigurationGroup(name='subgroup',
                                       content=SIMPLE_SUBGROUP_2)
        sut.add_group(subgroup2)
        group = sut.get_group('subgroup')
        assert group.get_attribute('testattribute').Value == 'testvalue'
        assert group.get_attribute('testattribute2').Value == 'testvalue2'

    def test_adding_sublist(self):

        """
        Tests that a sublist can be added to the group.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - New list can be added to an existing group
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        sut.add_list(ConfigurationList(name='test', content=[1,2,3]))
        assert sut.get_list('test') is not None

        # STEP #2 - Invalid list cannot be added
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        current_num = sut.NumLists
        sut.add_list(None)
        assert current_num == sut.NumLists

        # STEP #3 - Adding a list with the same name as an existing sublist
        #           results in a merge
        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        sut.add_list(ConfigurationList(name='test', content=[1,2,3]))
        current_num = sut.NumLists
        sut.add_list(ConfigurationList(name='test', content=[5,6,7]))
        assert current_num == sut.NumLists
        current_list = sut.get_list('test').Content
        assert len(current_list) == 6

    def test_merging_groups(self):

        """
        Tests that two configuration groups can be merged together.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Configuration groups can be merged.
        sut = ConfigurationGroup(name='test', content=SIMPLE_SUBGROUP)
        sut.merge_with(ConfigurationGroup(name='test',
                                          content=SIMPLE_SUBGROUP_2))
        assert sut.get_attribute('testattribute2') is not None

        # STEP #2 - Test merging with an invalid group
        sut = ConfigurationGroup(name='test', content=SIMPLE_SUBGROUP)
        current_attr_num = sut.NumAttributes
        current_group_num = sut.NumGroups
        current_list_num = sut.NumLists
        sut.merge_with(None)
        assert current_attr_num == sut.NumAttributes
        assert current_group_num == sut.NumGroups
        assert current_list_num == sut.NumLists

        # STEP #3 - Test merging groups with different names
        sut = ConfigurationGroup(name='test', content=SIMPLE_SUBGROUP)
        sut2 = ConfigurationGroup(name='test', content=GROUP_WITH_GROUP_LIST)
        current_attr_num = sut.NumAttributes
        current_group_num = sut.NumGroups
        current_list_num = sut.NumLists
        sut.merge_with(sut2)
        assert current_attr_num == sut.NumAttributes
        assert current_group_num == sut.NumGroups
        assert current_list_num == sut.NumLists

    def test_string_conversion(self):

        """
        Tests that groups has a correct string representation.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert str(sut) == 'test'
        assert sut.__repr__() == 'test'
