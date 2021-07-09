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
Contains the implementation of the DictionaryBackend class.
"""

# Platform Imports
from typing import Any

# Murasame Imports
from .configurationbackend import ConfigurationBackend

class DictionaryBackend(ConfigurationBackend):

    """Implements a backend that stores the configuration in a dictionary.

    Attributes:
        _data (dict): The dictionary storing the configuration data.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new DictionaryBackend instance.

        Authors:
            Attila Kovacs
        """

        super().__init__()

        self._data = {}

    def get(self, entry_name: str) -> Any:

        """Retrieves the value of a single configuration object.

        Args:
            entry_name (str): Name of the object to retrieve.

        Returns:
            Any: The object, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        if self.has_group(group_name=entry_name):
            return  self.get_group(group_name=entry_name)

        if self.has_list(list_name=entry_name):
            return  self.get_list(list_name=entry_name)

        if self.has_attribute(attribute_name=entry_name):
            return  self.get_attribute(attribute_name=entry_name)

        return  None

    def get_value(self, attribute_name: str) -> Any:

        """Returns the value of a given configuration attribute.

        Configuration attributes are organized into configuration groups.

        Each configuration group can contain any number of configuration
        groups, lists and/or configuration attributes. A configuration group
        can contain further configuration groups and/or configuration
        attributes, forming a tree structure.

        A given configuration attribute can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].<attribute>

        Args:
            attribute_name (str): Full name of the configuration attribute.

        Returns:
            Any: The value of the requested configuration attribute, or 'None',
                if it was not found.

        Authors:
            Attila Kovacs
        """

        if attribute_name == '' or attribute_name is None:
            self.error('Trying to retrieve an attribute value with an '
                       'invalid name.')
            return None

        self.debug(f'Retrieving value for attribute {attribute_name}...')

        attribute = self.get_attribute(attribute_name)

        if attribute:
            self.debug(f'Value of attribute {attribute_name} is '
                       f'{attribute.Value}')
            return attribute.Value

        self.warning(f'Attribute {attribute_name} was not found in the '
                     f'configuration.')
        return None

    def get_attribute(self, attribute_name: str) -> 'ConfigurationAttribute':

        """Returns the given configuration attribute.

        Configuration attributes are organized into configuration groups.

        Each configuration group can contain any number of configuration groups
        and/or configuration attributes. A configuration group can contain
        further configuration groups and/or configuration lists or attributes,
        forming a tree structure.

        A given configuration attribute can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].<attribute>

        Args:
            attribute_name (str): Full name of the configuration attribute.

        Returns:
            ConfigurationAttribute: The requested configuration attribute
                instance, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        if attribute_name == '' or attribute_name is None:
            self.error('Trying to retrieve an attribute with an invalid '
                       'name.')
            return None

        self.debug(f'Retrieving configuration attribute {attribute_name}...')

        # Figure out the group to retrieve from
        (group_name, remaining) = self._split_attribute_name(attribute_name)

        if not group_name in self._data:
            self.warning(f'Configuration attribute {attribute_name} does not '
                         f'exist in the configuration.')
            return None

        attribute = self._data[group_name].get_attribute(remaining)

        if attribute:
            self.debug(f'Attribute {attribute_name} was retrieved '
                       f'successfully.')
        else:
            self.warning(f'Attribute {attribute_name} was not found in the '
                         f'configuration.')

        return attribute

    def get_group(self, group_name: str) -> 'ConfigurationGroup':

        """Returns the given configuration group.

        Configuration groups are organized into configuration groups.

        Each configuration group can contain any number of configuration
        groups, lists and/or configuration attributes. A configuration group
        can contain further configuration groups and/or configuration
        attributes, forming a tree structure.

        A given configuration group can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].[<group>]

        Args:
            group_name (str): Full name of the configuration group.

        Returns:
            ConfigurationGroup: The requested configuration group instance, or
                'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        if group_name == '' or group_name is None:
            self.error('Trying to retrieve a group with an invalid name.')
            return None

        self.debug(f'Retrieving configuration group {group_name}...')

        if '.' in group_name:

            # Retrieving a sub-group

            # Figure out the top level group to retrieve from
            (top_level, remaining) = self._split_attribute_name(group_name)

            # Get the sub-group
            if top_level in self._data:

                group = self._data[top_level].get_group(remaining)

                if group:
                    self.debug(f'Configuration group {group_name} was '
                               f'retrieved.')
                    return group

        else:

            # Retrieving a top level group.
            if group_name in self._data:
                self.debug(f'Top level configuration group {group_name} was '
                           f'retrieved.')
                return self._data[group_name]

        self.warning(f'Configuration group {group_name} does not exist in the '
                     f'configuration.')

        return None

    def get_list(self, list_name: str) -> 'ConfigurationList':

        """Returns the given configuration list.

        Configuration lists are organized into configuration groups.

        Each configuration group can contain any number of configuration
        groups, lists and/or configuration attributes. A configuration group
        can contain further configuration groups and/or configuration
        attributes, forming a tree structure.

        A given configuration list can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].<list>

        Args:
            list_name (str): The full name of the list to retrieve.

        Returns:
            ConfigurationList: The requested configuration list instance, or
                'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        if list_name == '' or list_name is None:
            self.error('Trying to retrieve a configuration list with an '
                       'invalid name.')
            return None

        self.debug(f'Retrieving configuration list {list_name}...')

        if '.' in list_name:

            # Retrieving a sub-list

            # Figure out the top level group to retrieve from
            (top_level, remaining) = self._split_attribute_name(list_name)

            # Get the sub-group
            if top_level in self._data:

                config_list = self._data[top_level].get_list(remaining)

                if config_list:
                    self.debug(f'Configuration list {list_name} was '
                               f'retrieved.')
                    return config_list

        self.warning(f'Configuration list {list_name} does not exist in the '
                     f'configuration.')

        return None

    def has_group(self, group_name: str) -> bool:

        """Returns whether or not the backend has a group with the given name.

        Args:
            group_name (str): Name of the group to check.

        Returns:
            bool: 'True' if the given group exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if group_name == '' or group_name is None:
            self.error('Trying to check a group with an invalid name.')
            return False

        group = self.get_group(group_name)

        if group:
            return True

        return False

    def has_list(self, list_name: str) -> bool:

        """Returns whether or not the backend has a list with the given name.

        Args:
            list_name (str): Name of the group to check.

        Returns:
            bool: 'True' if the given list exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if list_name == '' or list_name is None:
            self.error('Trying to check a list with an invalid name.')
            return False

        config_list = self.get_list(list_name)

        if config_list:
            return True

        return False

    def has_attribute(self, attribute_name: str) -> bool:

        """Returns whether or not the backend has a given attribute.

        Args:
            attribute_name (str): Name of the attribute to check.

        Returns:
            bool: 'True' if the given attribute exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if attribute_name == '' or attribute_name is None:
            self.error('Trying to check an attribute with an invalid name.')
            return False

        attribute = self.get_attribute(attribute_name)

        if attribute:
            return True

        return False

    def add_group(self, parent: str, group: 'ConfigurationGroup') -> None:

        """Adds a new configuration group to the configuration tree.

        Args:
            parent (str): The full name of the parent object the group will be
                added to.
            group (ConfigurationGroup): The configuration group object to add.

        Authors:
            Attila Kovacs
        """

        if group is None:
            self.error(f'Trying to add invalid configuration group under'
                       f'parent {parent}.')
            return

        if parent is None:
            if not self.has_group(group.Name):
                self._data[group.Name] = group
                self.debug(f'New top level configuration group ({group.Name}) '
                           f'has been added.')
            else:
                self.debug(f'Top level configuration group {group.Name} '
                           f'already exist, merging...')
                self.merge_group(group.Name, group)

            return

        # Does the parent exist
        if not self.has_group(parent):
            self.error(f'Cannot add configuration group {group.Name} to '
                       f'non-existent parent {parent}.')
            return

        parent_group = self.get_group(parent)
        parent_group.add_group(group)

        self.debug(f'Configuration group {group.Name} added under parent '
                   f'{parent}.')

    def add_list(self, parent: str, config_list: 'ConfigurationList') -> None:

        """Adds a new configuration list to the configuration tree.

        Args:
            parent (str): The full name of the parent object the list will be
                added to.
            config_list (ConfigurationList): The configuration list to add.

        Authors:
            Attila Kovacs
        """

        if config_list is None:
            self.error(f'Trying to add invalid configuration list under'
                       f'parent {parent}.')
            return

        if parent is None:
            self.error(f'No parent specified when trying to add configuration '
                       f'list {config_list.Name}, cannot add.')
            return

        # Does the parent exist
        if not self.has_group(parent):
            self.error(f'Cannot add configuration list {config_list.Name} to '
                       f'non-existent parent {parent}.')
            return

        group = self.get_group(parent)
        group.add_list(config_list)

        self.debug(f'Configuration list {config_list.Name} added under parent '
                   f'{parent}.')

    def add_attribute(self,
                      parent: str,
                      attribute: 'ConfigurationAttribute') -> None:

        """Adds a new configuration attribute to the configuration tree.

        Args:
            parent (str): The full name of the parent object the list will be
                added to.
            attribute (ConfigurationAttribute): The configuration attribute to
                add.

        Authors:
            Attila Kovacs
        """

        if attribute is None:
            self.error(f'Trying to add invalid configuration attribute under'
                       f'parent {parent}.')
            return

        if parent is None:
            self.error(f'No parent specified when trying to add configuration '
                       f'attribute {attribute.Name}, cannot add.')
            return

        # Does the parent exist
        if not self.has_group(parent):
            self.error(f'Cannot add configuration attribute {attribute.Name} '
                       f'to non-existent parent {parent}.')
            return

        group = self.get_group(parent)
        group.add_attribute(attribute)

        self.debug(f'Configuration attribute {attribute.Name} added under '
                   f'parent {parent}.')

    def merge_group(self,
                    group_name: str,
                    other: 'ConfigurationGroup') -> None:

        """Merges the content of a configuration group with another one.

        Args:
            group_name (str): Name of the configuration group to merge into.
            other (ConfigurationGroup): The configuration group to merge.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Merging configuration group {other.Name} into '
                   f'{group_name}.')

        existing_group = self.get_group(group_name)

        if not existing_group:
            self.debug(f'Target group {group_name} does not exist.')

            # Get the parent group
            parent, last = group_name.rsplit('.')

            if last == other.Name:
                parent_group = self.get_group(parent)
                if parent_group:
                    parent_group.add_group(other)
            else:
                self.error(f'Name of the target group ({last}) and the new group '
                           f'({other.Name}) does not match, cannot merge.')
                return

        if existing_group.Name != other.Name:
            self.error(f'Name of the target group ({existing_group}) and the '
                       f'new group ({other.Name}) does not match, cannot '
                       f'merge.')
            return

        existing_group.merge_with(other)

    def set(self, attribute: str, value: Any) -> None:

        """Sets the value of a given configuration attribute.

        Args:
            attribute (str): Name of the attribute to set.
            value (Any): The new value of the attribute.

        Authors:
            Attila Kovacs
        """

        if not self.has_attribute(attribute):
            return

        if self.can_set(attribute, value):
            self._do_set(attribute, value)

    def can_set(self, attribute: str, value: Any) -> bool:

        """Returns whether or not the given attribute can be set to a new value.

        Args:
            attribute (str): Name of the attribute to set.
            value (Any): The new value of the attribute.

        Returns:
            bool: 'True' if the given attribute can be set to the new value,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not self.has_attribute(attribute):
            self.warning(f'Attribute {attribute} does not exist, cannot set.')
            return False

        attribute_obj = self.get_attribute(attribute)

        if isinstance(value, int) and attribute_obj.Type != 'INT':
            self.warning(f'Attribute type mismatch when trying to set '
                         f'{attribute}. Trying to set an integer value, but '
                         f'attribute type is {attribute_obj.Type}.')
            return False

        if isinstance(value, float) and attribute_obj.Type != 'FLOAT':
            self.warning(f'Attribute type mismatch when trying to set '
                         f'{attribute}. Trying to set a float value, but '
                         f'attribute type is {attribute_obj.Type}.')
            return False

        if isinstance(value, str) and attribute_obj.Type != 'STRING':
            self.warning(f'Attribute type mismatch when trying to set '
                         f'{attribute}. Trying to set a string value, but '
                         f'attribute type is {attribute_obj.Type}.')
            return False

        self.debug(f'Attribute {attribute} can be set to {value}.')
        return True

    def _do_set(self, attribute: str, value: Any) -> None:

        """Contains the actual setter logic of the backend.

        Args:
            attribute (str): Name of the attribute to set.
            value (Any): The new value of the attribute.

        Authors:
            Attila Kovacs
        """

        attribute_obj = self.get_attribute(attribute)
        if attribute_obj:
            attribute_obj.Value = value

    def _split_attribute_name(self, name: str) -> 'str, str':

        """Splits the attribute name to the group_name and the remaining part.

        Returns:
            str, str: The name of the configuration group is returned as the
                first return value, while the second value will contain the
                remainder of the name, thus the full attribute name.

        Authors:
            Attila Kovacs
        """

        split_name = str.split(name, '.', 1)

        self.debug(f'Input string {name} was split. Identified top level '
                   f'group: {split_name[0]} Identified attribute: '
                   f'{split_name[1]}')

        return (split_name[0], split_name[1])
