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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

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

    """
    Test suite for the DictionaryBackend class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a dictionary backend can be created.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Simple creation test
        sut = DictionaryBackend()
        assert sut is not None

    def test_adding_groups(self):

        """
        Tests that configuration groups can be added to the backend.
        """

        # STEP #1 - Test simple group addition
        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        assert sut.has_group(group_name='testgroup')

        # STEP #2 - Test adding subgroups
        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        group2 = ConfigurationGroup(name='testgroup2',
                                    content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent='testgroup', group=group2)
        assert sut.has_group('testgroup.testgroup2')

    def test_adding_lists(self):

        """
        Tests that configuration lists can be added to the backend.
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        config_list = ConfigurationList(name='testlist',
                                        content=TEST_CONFIGURATION_LIST)
        sut.add_list(parent='testgroup', config_list=config_list)
        assert sut.has_list(list_name='testgroup.testlist')

    def test_adding_attributes(self):

        """
        Tests that configuration attributes can be added to the backend.
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

    def test_retrieving_attributes(self):

        """
        Tests that configuration attributes can be retrieved from the backend.
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

    def test_retrieving_groups(self):

        """
        Tests that configuration groups can be retrieved from the backend.
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)

        assert sut.get_group(group_name='testgroup') == group

    def test_retrieving_lists(self):

        """
        Tests that configuration lists can be retrieved from the backend.
        """

        sut = DictionaryBackend()
        group = ConfigurationGroup(name='testgroup',
                                   content=TEST_CONFIGURATION_GROUP)
        sut.add_group(parent=None, group=group)
        config_list = ConfigurationList(name='testlist',
                                        content=TEST_CONFIGURATION_LIST)
        sut.add_list(parent='testgroup', config_list=config_list)

        assert sut.get_list(list_name='testgroup.testlist') == config_list

    def test_setting_attributes(self):

        """
        Tests that configuration attributes can be set through the backend.
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
