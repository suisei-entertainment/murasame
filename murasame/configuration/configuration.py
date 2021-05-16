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
Contains the implementation of the Configuration class.
"""

# Runtime Imports
from typing import Callable, Any

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.logging import LogWriter
from murasame.configuration.configurationbackends import ConfigurationBackends
from murasame.configuration.dictionarybackend import DictionaryBackend
from murasame.configuration.vfsconfigurationsource import VFSConfigurationSource

class ConfigurationAPI:

    """
    System definition for the configuration system.

    Authors:
        Attila Kovacs
    """

    def initialize(self, cb_retrieve_key: Callable = None) -> None:

        """
        Initializes the configuration system.

        Args:
            cb_retrieve_key:        A callback function to call when the
                                    configuration needs the decryption key to
                                    the configuration files.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del cb_retrieve_key

    def get(self, attribute: str) -> Any:

        """
        Retrieves the value of a single configuration attribute from the
        configuration tree.

        Args:
            attribute:      Name of the attribute to retrieve.

        Returns:
            The value of the attribute, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute

    def set(self, attribute: str, value: Any) -> None:

        """
        Sets the value of a given configuration attribute.

        Args:
            attribute:      Name of the attribute to set.
            value:          The new value of the attribute.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute
        del value

    def load(self) -> None:

        """
        Loads the configuration to memory.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        return

    def save(self) -> None:

        """
        Saves the current configuration.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        return

class Configuration(LogWriter):

    """
    Main class of the configuration system.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new Configuration instance.
        """

        super().__init__(channel_name='murasame.configuration',
                         cache_entries=True)

        self._backend = None
        """
        The configuration backend to use to store the configuration at runtime.
        """

        self._sources = []
        """
        List of configuration sources.
        """

        self._cb_config_key = None
        """
        The callback function to be used to retrieve the password required to
        decrypt the configuration.
        """

    def initialize(
            self,
            backend_type: ConfigurationBackends = ConfigurationBackends.DICTIONARY,
            cb_retrieve_key: Callable = None) -> None:

        """
        Initializes the configuration system.

        This function will add the configuration node from VFS as a
        configuration source.

        Args:
            backend_type:           The type of configuration backend to use.
            cb_retrieve_key:        A callback function to call when the
                                    configuration needs the decryption key to
                                    the configuration files.

        Raises:
            RuntimeError:           Raised if no VFS provider can be retrieved.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        # Store the config decryption key callback
        if cb_retrieve_key is not None:
            self._cb_config_key = cb_retrieve_key

        # Create the configuration backend
        if backend_type == ConfigurationBackends.DICTIONARY:
            self._backend = DictionaryBackend()
        else:
            raise InvalidInputError(
                f'Unsupported configuration backend: {backend_type}')

        self._sources.append(VFSConfigurationSource(path='/configuration'))

        # Load the configuration to memory
        self.load()

    def get(self, attribute: str) -> Any:

        """
        Retrieves the value of a single configuration attribute from the
        configuration tree.

        Args:
            attribute:      Name of the attribute to retrieve.

        Raises:
            RuntimeError:       Raised when no valid configuration backend is
                                set.

        Returns:
            The value of the attribute, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        if not self._backend:
            raise RuntimeError('No configuration backend has been specified, '
                               'cannot retrieve attributes.')

        attr = self._backend.get_attribute(attribute_name=attribute)
        if attr:
            return attr.Value

        return None

    def set(self, attribute: str, value: Any) -> None:

        """
        Sets the value of a given configuration attribute.

        Args:
            attribute:      Name of the attribute to set.
            value:          The new value of the attribute.

        Raises:
            RuntimeError:       Raised when no valid configuration backend is
                                set.
            InvalidInputError:  Raised when trying to set the value of a
                                non-existing attribute.

        Authors:
            Attila Kovacs
        """

        if not self._backend:
            raise RuntimeError('No configuration backend has been specified, '
                               'cannot set configuration attributes.')

        attr = self._backend.get_attribute(attribute_name=attribute)
        if attr:
            attr.Value = value
        else:
            raise InvalidInputError(
                f'Trying to set the value for non-existing attribute '
                f'{attribute}.')

    def load(self) -> None:

        """
        Loads the configuration to memory.

        Authors:
            Attila Kovacs
        """

        for source in self._sources:
            source.load()

    def save(self) -> None:

        """
        Saves the current configuration.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        for source in self._sources:
            source.save()
