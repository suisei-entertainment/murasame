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
Contains the implementation of the LoggingSystem class.
"""

# Runtime Imports
from typing import Union

class LoggingAPI:

    """
    Common interface for logging system implementations.

    Authors:
        Attila Kovacs
    """

    def has_channel(self, name: str) -> bool:

        """
        Returns whether or not a given log channel is registered in the
        logging system.

        Args:
            name:       The name of the log channel to check.

        Returns:
            'True' if the given log channel is registered, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return False

    def get_channel(self, name: str) -> 'LogChannel':

        """
        Returns a given log channel.

        Args:
            name:       Name of the channel to retrieve.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del name

class LoggingSystem:

    """
    Default logging system implementation.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new LoggingSystem instance.

        Authors:
            Attila Kovacs
        """

        self._channels = {}
        """
        The log channels registered in the logging system.
        """

    def has_channel(self, name: str) -> bool:

        """
        Returns whether or not a given log channel is registered in the
        logging system.

        Args:
            name:       The name of the log channel to check.

        Returns:
            'True' if the given log channel is registered, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return  name in self._channels

    def get_channel(self, name: str) -> Union['LogChannel', None]:

        """
        Returns a given log channel.

        Args:
            name:       Name of the channel to retrieve.

        Authors:
            Attila Kovacs
        """

        if self.has_channel(name):
            return self._channels[name]

        return None