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
Contains the implementation of the ConfigurationBackend class.
"""

# Platform Imports
from typing import Any

# Murasame Imports
from murasame.constants import MURASAME_CONFIGURATION_LOG_CHANNEL
from murasame.log import LogWriter

class ConfigurationBackend(LogWriter):

    """Common base class for all configuration backend implementations.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new ConfigurationBackend instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_CONFIGURATION_LOG_CHANNEL,
                         cache_entries=True)

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

        del entry_name

    def get_value(self, attribute_name: str) -> Any:

        """Returns the value of a given configuration attribute.

        Configuration attributes are organized into configuration groups.

        Each configuration group can contain any number of configuration groups,
        lists and/or configuration attributes. A configuration group can
        contain further configuration groups and/or configuration attributes,
        forming a tree structure.

        A given configuration attribute can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].<attribute>

        Args:
            name (str): Full name of the configuration attribute.

        Returns:
            Any: The value of the configuration attribute if it exists, or
            'None', if it doesn't.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute_name

    def get_attribute(self, attribute_name: str) -> 'ConfigurationAttribute':

        """Returns the given configuration attribute.

        Configuration attributes are organized into configuration groups.

        Each configuration group can contain any number of configuration
        groups, lists and/or configuration attributes. A configuration group
        can contain further configuration groups and/or configuration
        attributes, forming a tree structure.

        A given configuration list can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>].<attribute>

        Args:
            attribute_name (str):     Full name of the configuration attribute.

        Returns:
            ConfigurationAttribute: The retrieved configuration attribute
                instance, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute_name

    def get_group(self, group_name: str) -> 'ConfigurationGroup':

        """Returns the given configuration group.

        Configuration groups are organized into configuration groups.

        Each configuration group can contain any number of configuration
        groups, lists and/or configuration attributes. A configuration group
        can contain further configuration groups and/or configuration
        attributes, forming a tree structure.

        A given configuration list can be accessed by specifying it's full
        name, which is formatted the following way:
            <group>.[<group>].[<group>]...[<group>]

        Args:
            group_name (str): Full name of the configuration group.

        Returns:
            ConfigurationGroup: The retrieved configuration group instance, or
                'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del group_name

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

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del list_name

    def has_group(self, group_name: str) -> bool:

        """Returns whether or not the backend has a group with the given name.

        Args:
            group_name (str): Name of the group to check.

        Returns:
            bool: 'True' if the given group exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del group_name
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

        #pylint: disable=no-self-use

        del list_name
        return False

    def has_attribute(self, attribute_name: str) -> bool:

        """ Returns whether or not the backend has a given attribute.

        Args:
            attribute_name (str): Name of the attribute to check.

        Returns:
            bool: 'True' if the given attribute exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute_name
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

        #pylint: disable=no-self-use

        del parent
        del group

    def add_list(self, parent: str, config_list: 'ConfigurationList') -> None:

        """Adds a new configuration list to the configuration tree.

        Args:
            parent (str): The full name of the parent object the list will be
                added to.
            config_list (ConfigurationList): The configuration list to add.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del parent
        del config_list

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

        #pylint: disable=no-self-use

        del parent
        del attribute

    def merge_group(self,
                    group_name: str,
                    other: 'ConfigurationGroup') -> None:

        """Merges the content of a configuration group with another one.

        Args:
            group_name (str): Name of the configuration group to merge into.
            group (ConfigurationGroup): The configuration group to merge.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del group_name
        del other

    def set(self, attribute: str, value: Any) -> None:

        """Sets the value of a given configuration attribute.

        Args:
            attribute (str): Name of the attribute to set.
            value (Any): The new value of the attribute.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute
        del value

    def can_set(self, attribute: str, value: Any) -> bool:

        """Returns whether or not the attribute can be set to the new value.

        Args:
            attribute (str): Name of the attribute to set.
            value (Any): The new value of the attribute.

        Returns:
            bool: 'True' if the given attribute can be set to the new value,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute
        del value
        return False
