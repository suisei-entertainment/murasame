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
Contains the implementation of the ConfigurationSource class.
"""

# Murasame Imports
from murasame.constants import MURASAME_CONFIGURATION_LOG_CHANNEL
from murasame.log import LogWriter

class ConfigurationSource(LogWriter):

    """Base class for configuration sources.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new ConfigurationSource instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_CONFIGURATION_LOG_CHANNEL,
                         cache_entries=True)

    def load(self) -> None:

        """Loads the configuration from this configuration source.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(f'ConfigurationSource.load() has to be '
                                  f'implemented in {self.__class__.__name__}.')

    def save(self) -> None:

        """Saves the configuration to this configuration source.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(f'ConfigurationSource.save() has to be '
                                  f'implemented in {self.__class__.__name__}.')
