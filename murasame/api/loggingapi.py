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
Contains the definition of the LoggingAPI.
"""

# Runtime Imports
from abc import ABC, abstractmethod

class LoggingAPI(ABC):

    """Common interface for log system implementations.

    Authors:
        Attila Kovacs
    """

    @abstractmethod
    def has_channel(self, name: str) -> bool:

        """Returns whether or not a given log channel is registered in the
        log system.

        Args:
            name (str): The name of the log channel to check.

        Returns:
            bool: 'True' if the given log channel is registered, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del name
        return False

    @abstractmethod
    def get_channel(self, name: str) -> 'LogChannel':

        """Returns a given log channel.

        Args:
            name (str): Name of the channel to retrieve.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del name
