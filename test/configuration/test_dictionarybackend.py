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
Contains the unit tests of the DictionaryBackend class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.configuration.dictionarybackend import DictionaryBackend
from murasame.configuration.configurationgroup import ConfigurationGroup
from murasame.configuration.configurationlist import ConfigurationList
from murasame.configuration.configurationattribute import ConfigurationAttribute

TEST_CONFIGURATION_GROUP = \
{

}

TEST_CONFIGURATION_LIST = \
[

]

class TestDictionaryBackend:

    """Test suite for the DictionaryBackend class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a dictionary backend can be created.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        assert sut is not None

    def test_adding_groups(self) -> None:

        """Tests that configuration groups can be added to the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        assert sut.has_group(group_name='testgroup')

    def test_adding_subgroups(self) -> None:

        """Tests that subgroups can be added to the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        group2 = ConfigurationGroup(name='testgroup2',
                                    content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent='testgroup', group=group2)
        assert sut.has_group('testgroup.testgroup2')

    def test_adding_lists(self) -> None:

        """Tests that configuration lists can be added to the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        config_list = ConfigurationList(name='testlist',
                                        content=TEST_CONFIGURATION_LIST)
        sut.add_list(parent='testgroup', config_list=config_list)
        assert sut.has_list(list_name='testgroup.testlist')

    def test_adding_attributes(self) -> None:

        """Tests that configuration attributes can be added to the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        attr = ConfigurationAttribute(name='testattr',
                                      value='testvalue',
                                      data_type='STRING')
        sut.add_attribute(parent='testgroup', attribute=attr)
        assert sut.has_attribute(attribute_name='testgroup.testattr')

    def test_retrieving_attributes(self) -> None:

        """Tests that configuration attributes can be retrieved from the
        backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        attr = ConfigurationAttribute(name='testattr',
                                      value='testvalue',
                                      data_type='STRING')
        sut.add_attribute(parent='testgroup', attribute=attr)

        assert sut.get_attribute(attribute_name='testgroup.testattr') == attr
        assert sut.get_value(attribute_name='testgroup.testattr') == 'testvalue'

    def test_retrieving_attributes_through_get(self) -> None:

        """Tests that a configuration attribute can be retrieved through get().

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        attr = ConfigurationAttribute(name='testattr',
                                      value='testvalue',
                                      data_type='STRING')
        sut.add_attribute(parent='testgroup', attribute=attr)

        assert sut.get(entry_name='testgroup.testattr') == attr

    def test_retrieving_groups(self) -> None:

        """Tests that configuration groups can be retrieved from the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)

        assert sut.get_group(group_name='testgroup') == group

    def test_retrieving_groups_through_get(self) -> None:

        """Tests that configuration groups can be retrieved from the backend
        through get.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)

        assert sut.get(entry_name='testgroup') == group

    def test_retrieving_lists(self) -> None:

        """Tests that configuration lists can be retrieved from the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        config_list = ConfigurationList(name='testlist',
                                        content=TEST_CONFIGURATION_LIST)
        sut.add_list(parent='testgroup', config_list=config_list)

        assert sut.get_list(list_name='testgroup.testlist') == config_list

    def test_retrieving_lists_through_get(self) -> None:

        """Tests that configuration lists can be retrieved from the backend
        through get().

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        config_list = ConfigurationList(name='testlist',
                                        content=TEST_CONFIGURATION_LIST)
        sut.add_list(parent='testgroup', config_list=config_list)

        assert sut.get(entry_name='testgroup.testlist') == config_list

    def test_retrieving_non_existent_element(self) -> None:

        """Tests the retrieval of a non-existent configuration element.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        assert sut.get(entry_name='nonexistent.nonexistent') is None

    def test_setting_attributes(self) -> None:

        """Tests that configuration attributes can be set through the backend.

        Authors:
            Attila Kovacs
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        attr = ConfigurationAttribute(name='testattr',
                                      value='testvalue',
                                      data_type='STRING')
        sut.add_attribute(parent='testgroup', attribute=attr)
        sut.set(attribute='testgroup.testattr', value='newvalue')

        assert sut.get_value('testgroup.testattr') == 'newvalue'
