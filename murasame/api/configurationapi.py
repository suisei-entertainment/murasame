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
Contains the definition of the ConfigurationAPI.
"""

# Runtime Imports
from abc import ABC, abstractmethod
from typing import Callable, Any

class ConfigurationAPI (ABC):

    """System definition for the configuration system.

    Authors:
        Attila Kovacs
    """

    @abstractmethod
    def initialize(
            self,
            backend_type: 'ConfigurationBackends' = 'ConfigurationBackends.DICTIONARY',
            cb_retrieve_key: Callable = None) -> None:

        """Initializes the configuration system.

        This function will add the configuration node from VFS as a
        configuration source.

        Args:
            backend_type (ConfigurationBackends): The type of configuration
                backend to use.

            cb_retrieve_key (Callable): A callback function to call when the
                configuration needs the decryption key to the configuration
                files.

        Raises:
            RuntimeError:           Raised if no VFS provider can be retrieved.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del backend_type
        del cb_retrieve_key

    @abstractmethod
    def get(self, attribute: str) -> Any:

        """Retrieves the value of a single configuration attribute.

        Args:
            attribute (str): Name of the attribute to retrieve.

        Returns:
            Any: The value of the attribute, or 'None' if it was not found.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del attribute

    @abstractmethod
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

    @abstractmethod
    def load(self) -> None:

        """Loads the configuration to memory.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        return

    @abstractmethod
    def save(self) -> None:

        """Saves the current configuration.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        return
