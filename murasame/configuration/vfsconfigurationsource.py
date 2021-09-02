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

    def load(self, backend: 'ConfigurationBackend') -> None:

        """Loads the configuration from this configuration source.

        Args:
            backend (ConfigurationBackend): The backend to add the the
                configuration to.

        Raises:
            InvalidInputError: Raised when trying to load the configuration
                without providing a valid configuration backend.

            RuntimeError: Raised if no VFS provider can be retrieved to load
                the configuration files.

            InvalidInputError: Raised if there is no VFS node corresponding to
                the configured path.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading configuration from VFS source {self._path}...')

        if not backend:
            raise InvalidInputError(
                'A valid configuration backend has to be provided to load the '
                'configuration.')

        # Pylint doesn't recognize the instance() member of Singleton.
        # pylint: disable=no-member
        vfs = SystemLocator.instance().get_provider(VFSAPI)

        if not vfs:
            raise RuntimeError(f'VFS provider cannot be retrieved, cannot '
                               f'load configuration from path {self._path}.')

        node = vfs.get_node(key=self._path)

        if not node:
            raise InvalidInputError(f'VFS path {self._path} does not exist.')

        # Get all configuration files from the VFS node
        config_files = node.get_all_files(recursive=True,
                                          filename_filter='.conf')

        # Load all configuration files individually
        for config_file in config_files:
            self.debug(f'Loading configuration from {config_file.Name} '
                       f'(v{config_file.get_resource().Version})...')
            resource = config_file.get_resource().Resource
            self._parse(content=resource, backend=backend)

        self.debug('Configuration has been loaded.')

    def save(self) -> None:

        """Saves the configuration to this configuration source.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(f'ConfigurationSource.save() has to be '
                                  f'implemented in {self.__class__.__name__}.')

    def _parse(self, content: dict, backend: 'ConfigurationBackend') -> None:

        """Parses the content of the provided dictionary.

        Args:
            content (dict): The content of the configuration file.

            backend (ConfigurationBackend): The backend to add the the
                configuration to.

        Authors:
            Attila Kovacs
        """

        for key, value in content.items():
            if isinstance(value, dict):
                self._parse_dictionary(key, value, backend)
            elif isinstance(value, list):
                self._parse_list(key, value, backend)
            else:
                raise InvalidInputError(
                    f'Invalid content encountered when trying to parse config '
                    f'file. Content: {content}')

    @staticmethod
    def _parse_dictionary(
        key: str,
        value: dict,
        backend: 'ConfigurationBackend') -> None:

        """Parse the configuration content as a configuration group.

        Args:
            key (str): The name of the configuration group.

            value (dict): The content of the configuration group.

            backend (ConfigurationBackend): The backend to add the the
                configuration to.

        Authors:
            Attila Kovacs
        """

        config_group = ConfigurationGroup(name=key, content=value)
        backend.add_group(parent=None, group=config_group)

    @staticmethod
    def _parse_list(
        key: str,
        value: list,
        backend: 'ConfigurationBackend') -> None:

        """Parse the configuration content as a configuration list.

        Args:
            key (str): The name of the configuration list.

            value (list): The content of the configuration list.

            backend (ConfigurationBackend): The backend to add the the
                configuration to.

        Authors:
            Attila Kovacs
        """

        config_list = ConfigurationList(name=key, content=value)
        backend.add_list(parent=None, config_list=config_list)
