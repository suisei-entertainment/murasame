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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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

    def test_simple_configuration_group_creation(self):

        """
        Tests the creation of a simple configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.Name == 'test'

    def test_nested_configuration_group_creation(self):

        """
        Tests that a nested configuration group can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.Name == 'nested'

    def test_nested_configuration_group_with_list_creation(self):

        """
        Tests that a nested configuration group containing a configuration list
        can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.Name == 'nested'

    def test_creating_configuration_group_without_name(self):

        """
        Tests that a configuration group can be created without a name.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(content=SIMPLE_TEST_GROUP)
        assert sut.Name == None

    def test_creating_empty_configuration_group(self):

        """
        Tests that an empty configuration group can be created.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(content={})
        assert sut.Name == None

    def test_simple_attribute_retrieval(self):

        """
        Tests that configuration attributes can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.get_attribute('stringvalue').Value == 'test'
        assert sut.get_attribute('intvalue').Value == 3
        assert sut.get_attribute('floatvalue').Value == 9.0
        assert sut.Attributes is not None
        assert sut.Groups is not None
        assert sut.Lists is not None

    def test_attribute_retrieval_from_nested_group(self):

        """
        Tests that configuration attributes can be retrieved from a nested
        configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_attribute('nest.nestedname').Value == 'test2'

    def test_retrieving_non_existent_attribute(self):

        """
        Tests that retrieval of a non-existend configuration attribute.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.get_attribute('nonexistent') is None

    def test_retrieving_invalid_attribute(self):

        """
        Tests retrieval of a configuration attribute with invalid name from a
        configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        assert sut.get_attribute('') is None
        assert sut.get_attribute(None) is None

    def test_simple_group_retrieval(self):

        """
        Tests that configuration groups can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nest').Name == 'nest'

    def test_group_retrieval_from_nested_group(self):

        """
        Tests that nested configuration group can be retrieved from the
        configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nest.nestnest').Name == 'nestnest'

    def test_retrieval_of_non_existent_group(self):

        """
        Tests retrieval of non-existend configuration group from a
        configuration group/

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('nonexistent') is None

    def test_retrieval_of_group_with_invalid_name(self):

        """
        Tests retrieval of a group with invalid name from a configuration
        group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP)
        assert sut.get_group('') is None
        assert sut.get_group(None) is None

    def test_simple_list_retrieval(self):

        """
        Tests that configuration lists can be retrieved from the group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.get_list('list').get_value(0) == 1

    def test_retrieving_group_list(self):

        """
        Tests retrieving a configuration list containing configuration groups
        from a configuration gorup.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=GROUP_WITH_GROUP_LIST)
        assert sut.get_list('list').get_content()['element1'].Name == 'element1'

    def test_retrieving_non_existent_list(self):

        """
        Tests retrieval of non-existent configuration list from a configuration
        group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
        assert sut.get_group('nonexistent') is None

    def test_retrieval_of_invalid_list_name(self):

        """
        Tests retrieval of a configuration list with invalid name from a
        configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=NESTED_GROUP_WITH_LIST)
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

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        subgroup = ConfigurationGroup(name='subgroup', content=SIMPLE_SUBGROUP)
        sut.add_group(subgroup)
        assert sut.get_group('subgroup') is not None

    def test_adding_invalid_subgroup(self):

        """
        Tests adding an invalid subgroup to a configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        current_num = sut.NumGroups
        sut.add_group(None)
        assert current_num == sut.NumGroups

    def test_adding_subgroup_with_same_name(self):

        """
        Tests that adding a group with the same name as a subgroup results in
        a merge.

        Authors:
            Attila Kovacs
        """

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

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        sut.add_list(ConfigurationList(name='test', content=[1,2,3]))
        assert sut.get_list('test') is not None

    def test_adding_invalid_list(self):

        """
        Tests that invalid configuration list cannot be added to a
        configuration group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_TEST_GROUP)
        current_num = sut.NumLists
        sut.add_list(None)
        assert current_num == sut.NumLists

    def test_adding_list_with_same_name(self):

        """
        Tests that adding a list with the same name as an existing sublist
        results in a merge.

        Authors:
            Attila Kovacs
        """

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

        sut = ConfigurationGroup(name='test', content=SIMPLE_SUBGROUP)
        sut.merge_with(ConfigurationGroup(name='test',
                                          content=SIMPLE_SUBGROUP_2))
        assert sut.get_attribute('testattribute2') is not None

    def test_merging_with_invalid_group(self):

        """
        Tests that configuration group cannot be merged with an invalid group.

        Authors:
            Attila Kovacs
        """

        sut = ConfigurationGroup(name='test', content=SIMPLE_SUBGROUP)
        current_attr_num = sut.NumAttributes
        current_group_num = sut.NumGroups
        current_list_num = sut.NumLists
        sut.merge_with(None)
        assert current_attr_num == sut.NumAttributes
        assert current_group_num == sut.NumGroups
        assert current_list_num == sut.NumLists

    def test_merging_groups_with_different_names(self):

        """
        Tests merging configuration groups with different names.

        Authors:
            Attila Kovacs
        """

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
