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
Contains the implementation of the VFSConfigurationSource class.
"""

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import SystemLocator
from murasame.api import VFSAPI
from murasame.configuration.configurationsource import ConfigurationSource
from murasame.configuration.configurationgroup import ConfigurationGroup
from murasame.configuration.configurationlist import ConfigurationList
from murasame.configuration.configurationattribute import ConfigurationAttribute

class VFSConfigurationSource(ConfigurationSource):

    """Configuration source that uses a VFS directory as the source.

    Attributes:
        _path (str): Path to the VFS directory to use as configuration source.

    Authors:
        Attila Kovacs
    """

    def __init__(self, path: str) -> None:

        """Creates a new VFSConfigurationSource instance.

        Args:
            path (str): Path to the VFS directory to use as configuration
                source.

        Authors:
            Attila Kovacs
        """

        super().__init__()

        self._path = path

    def load(self) -> None:

        """Loads the configuration from this configuration source.

        Raises:
            RuntimeError: Raised if no VFS provider can be retrieved to load
                the configuration files.

            InvalidInputError: Raised if there is no VFS node corresponding to
                the configured path.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading configuration from VFS source {self._path}...')

        # Pylint doesn't recognize the instance() member of Singleton.
        # pylint: disable=no-member
        vfs = SystemLocator.instance().get_provicer(VFSAPI)

        if not vfs:
            raise RuntimeError(f'VFS provider cannot be retrieved, cannot '
                               f'load configuration from path {self._path}.')

        node = vfs.get_node(key=self._path)

        if not node:
            raise InvalidInputError(f'VFS path {self._path} does not exist.')

        # Get all configuration files from the VFS node
        config_files = node.get_all_files(recursive=True, filter='.conf')

        # Load all configuration files individually
        for config_file in config_files:
            self.debug(f'Loading configuration from {config_file.Name} '
                       f'(v{config_file.get_resource().Version})...')
            resource = config_file.get_resource().Resource
            self._parse(content=resource)

        self.debug('Configuration has been loaded.')

    def save(self) -> None:

        """Saves the configuration to this configuration source.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(f'ConfigurationSource.save() has to be '
                                  f'implemented in {self.__class__.__name__}.')

    def _parse(self, content: dict) -> None:

        """Parses the content of the provided dictionary.

        Args:
            content (dict): The content of the configuration file.

        Authors:
            Attila Kovacs
        """

        for key, value in content.items():
            if isinstance(value, dict):
                self._parse_dictionary(key, value)
            elif isinstance(value, list):
                self._parse_list(key, value)
            else:
                self._parse_attribute(key, value)

    def _parse_dictionary(self, key: str , value: dict) -> None:

        """Parse the configuration content as a configuration group.

        Args:
            key (str): The name of the configuration group.
            value (dict): The content of the configuration group.

        Authors:
            Attila Kovacs
        """

        dummy = ConfigurationGroup(name=key, content=value)

    def _parse_list(self, key: str, value: list) -> None:

        """Parse the configuration content as a configuration list.

        Args:
            key (str): The name of the configuration list.
            value (list): The content of the configuration list.

        Authors:
            Attila Kovacs
        """

        dummy = ConfigurationList(name=key, content=value)

    def _parse_attribute(self, key: str, value: object) -> None:

        """Parse the configuration content as a configuration attribute.

        Args:
            key (str): The name of the configuration attribute.
            value (object): The content of the configuration attribute.

        Raises:
            InvalidInputError: Raised when unsupported datatype is detected for
                the the attribute value.

        Authors:
            Attila Kovacs
        """

        data_type = None

        if isinstance(value, str):
            data_type  = 'STRING'
        elif isinstance(value, int):
            data_type = 'INT'
        elif isinstance(value, float):
            data_type = 'FLOAT'
        else:
            raise InvalidInputError(
                f'Unsupported data type when trying to parse configuration '
                f'attribute {key}:{value}.')

        dummy = ConfigurationAttribute(name=key,
                                       value=value,
                                       data_type=data_type)
