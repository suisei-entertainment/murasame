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
Contains the implementation of the ConfigurationGroup class.
"""

# Murasame Imports
from murasame.constants import MURASAME_CONFIGURATION_LOG_CHANNEL
from murasame.exceptions import AlreadyExistsError, InvalidInputError
from murasame.log import LogWriter
from murasame.configuration.configurationattribute import ConfigurationAttribute
from murasame.configuration.configurationlist import ConfigurationList

class ConfigurationGroup(LogWriter):

    """Representation of a single configuration group.

    Attributes:
        _name (str):    The name of the configuration group.
        _groups (dict): Dictionary of child configuration groups.
        _lists  (dict): Dictionary of child configuration lists.
        _attributes (dict): Dictionary of configuration attributes.

    Authors:
        Attila Kovacs
    """

    @property
    def Name(self) -> str:

        """The name of the configuration group.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def Attributes(self) -> dict:

        """Provides access to the configuration attributes stored in the group.

        Authors:
            Attila Kovacs
        """

        return self._attributes

    @property
    def Groups(self) -> dict:

        """Provides access to the configuration groups stored in the group.

        Authors:
            Attila Kovacs
        """

        return self._groups

    @property
    def Lists(self) -> dict:

        """Provides access to the configuration lists stored in the group.

        Authors:
            Attila Kovacs
        """

        return self._lists

    @property
    def NumAttributes(self) -> int:

        """Returns the amount of configuration attributes in the group.

        Authors:
            Attila Kovacs
        """

        return len(self._attributes)

    @property
    def NumGroups(self) -> int:

        """Returns the amount of configuration groups in the group.

        Authors:
            Attila Kovacs
        """

        return len(self._groups)

    @property
    def NumLists(self) -> int:

        """Returns the amount of configuration lists in the group.

        Authors:
            Attila Kovacs
        """

        return len(self._lists)

    def __init__(self, name: str = None, content: dict = None) -> None:

        """Creates a new ConfigurationGroup instance.

        Args:
            name (str): The name of the configuration group. This will be
                overwritten if the content dictionary also contains a name for
                the configuration group.

            content (dict): The content of the configuration group.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_CONFIGURATION_LOG_CHANNEL,
                         cache_entries=True)

        self._name = name
        self._groups = {}
        self._lists = {}
        self._attributes = {}

        if content:
            self._load_group(content)

    def __str__(self) -> str:

        """The string representation of the object.

        Authors:
            Attila Kovacs
        """

        return self._name

    def __repr__(self) -> str:

        """The string representation of the object.

        Authors:
            Attila Kovacs
        """

        return self._name

    def get_attribute(self, attribute_name: str) -> 'ConfigurationAttribute':

        """Returns an attribute from this configuration file.

        Args:
            attribute_name (str): Full name of the attribute to retrieve
                without the filename part.

        Returns:
            ConfigurationAttribute: The attribute object if it was found,
                'None' if the attribute doesn't exist.

        Authors:
            Attila Kovacs
        """

        if attribute_name == '' or attribute_name is None:
            self.error(f'Trying to retrieve an attribute with an invalid '
                       f'name from configuration group {self.Name}.')
            return None

        if '.' not in attribute_name:

            # Looking for a top level attribute
            if self.has_top_level_attribute(attribute_name):
                return self._attributes[attribute_name]

        else:

            # Looking for an attribute in a subgroup.
            (top_group, remaining) = self._split_attribute_name(attribute_name)

            if self.has_top_level_group(top_group):
                return self._groups[top_group].get_attribute(remaining)

        self.error(f'Attribute {attribute_name} was not found in configuration '
                   f'group {self.Name}.')
        return None

    def get_group(self, group_name: str) -> 'ConfigurationGroup':

        """Returns a group from this configuration file.

        Args:
            name (str): Full name of the group to retrieve without the filename
                part.

        Returns:
            ConfigurationGroup: The group object if it was found, 'None' if the
                attribute doesn't exist.

        Authors:
            Attila Kovacs
        """

        if group_name == '' or group_name is None:
            self.error(f'Trying to retrieve a configuration group with an '
                       f'invalid name from configuration group {self.Name}.')
            return None

        if '.' not in group_name:

            # Looking for a top level group
            if self.has_top_level_group(group_name):
                return self._groups[group_name]

        else:

            # Looking for a subgroup
            (top_group, remaining) = self._split_attribute_name(group_name)

            if self.has_top_level_group(top_group):
                return self._groups[top_group].get_group(remaining)

        self.error(f'Group {group_name} was not found in configuration group '
                   f'{self.Name}.')
        return None

    def get_list(self, list_name: str) -> 'ConfigurationList':

        """Returns a list from this configuration group.

        Args:
            name (str): Full name of the list to retrieve without the filename
                part.

        Returns:
            ConfigurationList: The list object if it was found, 'None' if the
                list doesn't exist.

        Authors:
            Attila Kovacs
        """

        if list_name == '' or list_name is None:
            self.error(f'Trying to retrieve a configuration list with an '
                       f'invalid name from configuration group {self.Name}.')
            return None

        if '.' not in list_name:

            # Looking for a top level list
            if self.has_top_level_list(list_name):
                return self._lists[list_name]

        else:

            # Looking for a sublist
            (top_group, remaining) = self._split_attribute_name(list_name)

            if self.has_top_level_group(top_group):
                return self._groups[top_group].get_list(remaining)

        self.error(f'List {list_name} was not found in configuration group '
                   f'{self.Name}.')
        return None

    def has_top_level_attribute(self, attribute_name: str) -> bool:

        """Returns whether or not an attribute is a top level one in the file.

        Args:
            attribute_name (str): The name of the attribute to check.

        Returns:
            bool: 'True' if the attribute is present as a top level list,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if attribute_name in self._attributes:
            return True

        return False

    def has_top_level_list(self, list_name: str) -> bool:

        """Returns whether or not a list is a top level one in the file.

        Args:
            list_name (str): The name of the list to check.

        Returns:
            bool: 'True' if the list is present as a top level list, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if list_name in self._lists:
            return True

        return False

    def has_top_level_group(self, group_name: str) -> bool:

        """Returns whether or not a given group is a top level one in the file.

        Args:
            group_name (str): The name of the group to check.

        Returns:
            bool: 'True' if the group is present as a top level group, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if group_name in self._groups:
            return True

        return False

    def add_attribute(self, attribute: 'ConfigurationAttribute') -> None:

        """Adds a new configuration attribute to the group.

        Args:
            attribute (ConfigurationGroup): The new configuration attribute to
                add.

        Authors:
            Attila Kovacs
        """

        if attribute is None:
            self.error(f'Trying to add an invalid attribute to configuration '
                       f'group {self.Name}.')
            return

        if self.has_top_level_attribute(attribute.Name):
            self.error(f'Configuration attribute {attribute.Name} already '
                       f'exist in group {self.Name}, cannot add.')
            return

        self.debug(f'Adding configuration attribute {attribute.Name} to '
                   f'configuration group {self.Name}.')

        self._attributes[attribute.Name] = attribute

    def add_group(self, group: 'ConfigurationGroup') -> None:

        """Adds a new configuration group to the group.

        Args:
            group (ConfigurationGroup): The new configuration group to add.

        Authors:
            Attila Kovacs
        """

        if group is None:
            self.error(f'Trying to add an invalid group to configuration '
                       f'group {self.Name}.')
            return

        if self.has_top_level_group(group.Name):
            self.debug(f'Configuration group {self.Name} already has a group '
                       f'named {group.Name}, merging the two.')
            self._groups[group.Name].merge_with(group)
            return

        self.debug(f'Adding configuration group {group.Name} to group '
                   f'{self.Name}.')

        self._groups[group.Name] = group

    def add_list(self, config_list: 'ConfigurationList') -> None:

        """Adds a new configuration list to the group.

        Args:
            config_list (ConfigurationList): The new configuration list to add.

        Authors:
            Attila Kovacs
        """

        if config_list is None:
            self.error(f'Trying to add an invalid configuration list to '
                       f'configuration group {self.Name}.')
            return

        if self.has_top_level_list(config_list.Name):
            self.debug(f'Configuration group {self.Name} already has a list '
                       f'named {config_list.Name}, merging the two.')
            self._lists[config_list.Name].merge_with(config_list)
            return

        self.debug(f'Adding configuration list {config_list.Name} to group '
                   f'{self.Name}.')
        self._lists[config_list.Name] = config_list

    def merge_with(self, other: 'ConfigurationGroup') -> None:

        """Merges the content of the other configuration group into this one.

        Args:
            other (ConfigurationGroup): The other configuration group to merge
                into this one.

        Authors:
            Attila Kovacs
        """

        if other is None:
            self.error(f'Trying to merge an invalid configuration group into '
                       f'{self.Name}.')
            return

        if other.Name != self.Name:
            self.error(f'The name of the two configuration group {self.Name}, '
                       f'{other.Name} does not match, cannot merge.')
            return

        self.debug(f'Merging configuration group {other.Name} into '
                   f'{self.Name}.')

        # Merge attributes
        attributes = other.Attributes.items()
        for attribute in attributes:
            if self.has_top_level_attribute(attribute[0]):
                self.debug(f'Configuration group {self.Name} already has an '
                           f'attribute with name {attribute[0]}, won\'t merge,')
                continue

            self.add_attribute(attribute[1])

        # Merge groups
        groups = other.Groups.items()
        for group in groups:
            if self.has_top_level_group(group[0]):
                self.debug(f'Configuration group {self.Name} already has a '
                           f'sub-group with name {group[0]}, merging the two.')
                parent = self._groups[group[0]]
                parent.merge_with(group[1])
            else:
                self.debug(f'Configuration group {self.Name} does not have a '
                           f'sub-group with name {group[0]}, adding it as a '
                           f'new one.')
                self.add_group(group[1])

        # Merge lists
        lists = other.Lists.items()
        for clist in lists:
            if self.has_top_level_list(clist[0]):
                self.debug(f'Configuration group {self.Name} already has a '
                           f'list with name {clist[0]}, merging the two.')
                parent = self._lists[clist[0]]
                parent.merge_with(clist[1])
            else:
                self.debug(f'Configuration group {self.Name} does not have a '
                           f'list with name {clist[1]}, adding it as a new '
                           f'one.')
                self.add_list(clist[1])

    def _split_attribute_name(self, name: str) -> 'str, str':

        """ Splits the name to the top level group and the remaining part.

        Returns:
            str, str: The name of the configuration group is returned as the
                first return value, while the second value will contain the
                remainder of the name, thus the full attribute name.

        Raises:
            InvalidInputError: Raised when an empty string is provided as the
                attribute name.

        Authors:
            Attila Kovacs
        """

        split_name = str.split(name, '.', 1)

        self.debug(f'Input string {name} was split. Identified configuration '
                   f'group: {split_name[0]} Identified attribute: '
                   f'{split_name[1]}')

        return (split_name[0], split_name[1])

    def _load_group(self, content: dict) -> None:

        """Loads the configuration group from a JSON object.

        Args:
            content (dict): The JSON content of the group to parse.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Parsing configuration group {self.Name}')

        for entry_key, entry_content in content.items():

            try:
                entry_type = self._identify_entry_type(entry_content)
                if entry_type == 'GROUP':
                    self._process_entry_as_group(entry_key, entry_content)
                elif entry_type == 'LIST':
                    self._process_entry_as_list(entry_key, entry_content)
                elif entry_type == 'STRING' and entry_key == 'name':
                    self._name = entry_content
                elif entry_type in ['STRING', 'INT', 'FLOAT']:
                    self._process_entry_as_attribute(entry_key,
                                                     entry_content,
                                                     entry_type)
                else:
                    self.warning(f'Failed to identify entry, skipping '
                                 f'{entry_key}')
            except AlreadyExistsError:
                self.warning(f'Duplicate entry found for {entry_type}, '
                             f'ignoring.')
            except Exception as error:
                raise InvalidInputError(f'Failed to parse configuration group '
                                        f'{self.Name}.') from error

        self.debug(f'Configuration group {self.Name} parsed successfully.')

    def _identify_entry_type(self, content: object) -> str:

        """Returns the entry type of a JSON object.

        Args:
            content (object): The object to identify.

        Returns:
            str: The type of the object in string format, or 'UNKNOWN' if the
                type cannot be identified.

        Authors:
            Attila Kovacs
        """

        if isinstance(content, dict):
            self.debug('Entry is identified as a configuration group.')
            return 'GROUP'

        if isinstance(content, list):
            self.debug('Entry is identified as a list.')
            return 'LIST'

        if isinstance(content, str):
            self.debug('Entry is identified as a string attribute.')
            return 'STRING'

        if isinstance(content, int):
            self.debug('Entry is identified as an integer attribute.')
            return 'INT'

        if isinstance(content, float):
            self.debug('Entry is identified as a floating point attribute.')
            return 'FLOAT'

        return 'UNKNOWN'

    def _process_entry_as_group(self,
                                entry_key: str,
                                entry_content: dict) -> None:

        """Processes an entry in the file as a configuration group.

        Args:
            entry_key (str): The key of the entry.
            entry_content (dict): The content of the entry.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Processing configuration group {entry_key}')

        if self.has_top_level_group(entry_key):
            raise AlreadyExistsError(
                f'Configuration group {entry_key} already exists.')

        self._groups[entry_key] = ConfigurationGroup(name=entry_key,
                                                     content=entry_content)

        self.debug(f'New configuration group successfully added: {entry_key}')

    def _process_entry_as_list(self,
                               entry_key: str,
                               entry_content: dict) -> None:

        """Processes an entry in the file as a list of configuration entries.

        Args:
            entry_key (str): The key of the entry.
            entry_content (dict): The content of the entry.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Processing configuration entry list {entry_key}')

        if self.has_top_level_list(entry_key):
            raise AlreadyExistsError(
                f'Configuration list {entry_key} already exists')

        self._lists[entry_key] = ConfigurationList(name=entry_key,
                                                   content=entry_content)

        self.debug(f'New list successfully added: {entry_key}')

    def _process_entry_as_attribute(self,
                                    entry_key: str,
                                    entry_content: object,
                                    entry_type: str) -> None:

        """Processes an entry in the file as a configuration attribute.

        Args:
            entry_key (str): The key of the entry.
            entry_content (object): The content of the entry.
            entry_type (str): The identified type of the entry.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Processing configuration attribute {entry_key}')

        if self.has_top_level_attribute(entry_key):
            raise AlreadyExistsError(
                f'Configuration attribute {entry_key} already exists.')

        self._attributes[entry_key] = ConfigurationAttribute(
            name=entry_key, value=entry_content, data_type=entry_type)

        self.debug(f'New attribute successfully added: {entry_key}')
