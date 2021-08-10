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
Contains the implementation of the ConfigurationList class.
"""

# Platform Imports
from typing import Any

# Murasame Imports
from murasame.constants import MURASAME_CONFIGURATION_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log import LogWriter

class ConfigurationList(LogWriter):

    """Representation of a configuration list.

    Attributes:
        _name (str): The name of the configuration list.
        _groups (dict): The configuration groups stored in the list.
        _values (list): The values stored in the list.

    Authors:
        Attila Kovacs
    """

    @property
    def Name(self) -> str:

        """The name of the configuration list.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def Type(self) -> str:

        """The type of data contained in the list.

        Authors:
            Attila Kovacs
        """

        return self._type

    @property
    def Content(self) -> Any:

        """Returns the content of the list.

        Authors:
            Attila Kovacs
        """

        if self.Type == 'VALUE':
            return self._values

        return self._groups

    @property
    def NumElements(self) -> int:

        """Returns the amount of elements in the list.

        Authors:
            Attila Kovacs
        """

        if self.Type == 'VALUE':
            if self._values:
                return len(self._values)
        elif self.Type == 'GROUP':
            if self._groups:
                return len(self._groups)

        return 0

    def __init__(self, name: str, content: list = None) -> None:

        """Creates a new ConfigurationList instance.

        Args:
            name (str): The name of the list.
            content (list): The content of the list.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_CONFIGURATION_LOG_CHANNEL,
                         cache_entries=True)

        self._name = name
        self._groups = {}
        self._values = []
        self._load_list(content)

    def __str__(self) -> str:

        """Returns the string representation of the object.

        Authors:
            Attila Kovacs
        """

        return self._name

    def __repr__(self) -> str:

        """Returns the string representation of the object.

        Authors:
            Attila Kovacs
        """

        return self._name

    def has_local_group(self, group_name: str) -> bool:

        """Returns whether or not a configuration group is present in the list.

        Args:
            group_name (str): The name of the group.

        Returns:
            bool: 'True' if the group is present, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if group_name in self._groups:
            return True

        return False

    def get_group(self, group_name: str) -> 'ConfigurationGroup':

        """Returns a configuration group from the list.

        Args:
            group_name (str): Name of the group to retrieve.

        Returns:
            ConfigurationGroup: The configuration group if it exists, or 'None'
                if it doesn't.

        Raises:
            RuntimeError: Thrown when trying to retrieve a group from a list
                that doesn't contain groups.

        Authors:
            Attila Kovacs
        """

        if self._type != 'GROUP':
            raise RuntimeError(
                f'Trying to retrieve configuration group {group_name} from '
                f'configuration list {self._name}, but list type is not '
                f'GROUP. Current list type: {self._type}')

        if self.has_local_group(group_name):
            return self._groups[group_name]

        self.error(f'Group {group_name} is not found in list {self._name}.')
        return None

    def get_value(self, index: int) -> object:

        """Returns a value from the list.

        Args:
            index (int): Index of the list element to retrieve.

        Returns:
            object: The retrieved element.

        Raises:
            RuntimeError: Raised when trying to retrieve a value from a list
                containing configuration groups.

            InvalidInputError: Raised when the requested index doesn't exist in
                the list.

        Authors:
            Attila Kovacs
        """

        if self._type != 'VALUE':
            raise RuntimeError(
                f'Trying to retrieve configuration value from configuration '
                f'list {self._name}, but list type is not VALUE. Current list '
                f'type: {self._type}')

        num_elements = len(self._values)
        if num_elements < index:
            raise InvalidInputError(
                f'Index is out of bounds. Trying to retrieve element {index} '
                f'from list {self._name}, but it only contains '
                f'{num_elements} elements.')

        return self._values[index]

    def get_content(self) -> str:

        """Returns the content of the list.

        Authors:
            Attila Kovacs
        """

        if self._type == 'VALUE':
            return self._values

        if self._type == 'GROUP':
            return self._groups

        return None

    def merge_with(self, other: 'ConfigurationList') -> None:

        """Merges the content of another configuration list into this one.

        Args:
            other (ConfigurationList): The other configuration list to merge
                into this one.

        Authors:
            Attila Kovacs
        """

        if other is None:
            self.error(f'Trying to merge configuration list {self.Name} with '
                       f'an invalid one.')
            return

        if self.Type != other.Type:
            self.error(f'Type mismatch when trying to merge configuration '
                       f'list {self.Name} (type: {self.Type}) with '
                       f'{other.Name} (type: {other.Type})')
            return

        if self.Name != other.Name:
            self.error(f'Name of the list {self.Name} and {other.Name} does '
                       f'not match, cannot merge.')
            return

        elements = other.Content

        if self.Type == 'VALUE':
            self.debug(f'Merging content to value list {self.Name}.')
            self._values = self._values + elements
        else:
            self.debug(f'Merging content of group list {self.Name}.')
            elements.update(self._groups)
            self._groups = elements

    def _load_list(self, content: list) -> None:

        """Loads the configuration list from the JSON content.

        Args:
            content (list): The JSON list containing the list elements.

        Raises:
            InvalidInputError: Raised if the specified list cannot be loaded as
                a configuration list.

        Authors:
            Attila Kovacs
        """

        # Avoiding circular dependency
        #pylint: disable=import-outside-toplevel
        from .configurationgroup import ConfigurationGroup

        self.debug(f'Parsing content of configuration list {self.Name}')

        self._type = self._identify_element_type(content)

        if self._type == 'EMPTY':
            self.debug(f'Empty list {self.Name} parsed successfully.')
            return

        for element in content:
            try:
                if self._type == 'GROUP':

                    if self.has_local_group(element['name'].lower()):
                        element_name = element['name']
                        self.warning(
                            f'The configuration group {element_name} '
                            f'is already part of list {self.Name}')
                        continue

                    group = ConfigurationGroup(name=element['name'].lower(),
                                               content=element)

                    self._groups[element['name'].lower()] = group

                elif self._type == 'VALUE':
                    self._values.append(element)

            except KeyError:
                self.error('The list contains a group, but at least one '
                           'element does not have a name attribute.')

            except Exception as error:
                raise InvalidInputError(f'Failed to load the contents of list '
                                        f'{self.Name}') from error

        self.debug(f'Configuration list {self.Name} parsed successfully.')

    @staticmethod
    def _identify_element_type(content: object) -> str:

        """Identify the type of the elements in the list.

        Args:
            content (object): The JSON content of the list.

        Returns:
            str: 'GROUP' if the list contains configuration groups, 'VALUE' if
                the list contains values, 'EMPTY' if the list is empty.

        Authors:
            Attila Kovacs
        """

        if not content:
            return 'EMPTY'

        if isinstance(content[0], dict):
            return 'GROUP'

        return 'VALUE'
