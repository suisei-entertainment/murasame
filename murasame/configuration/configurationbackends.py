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
Contains the implementation of the ConfigurationBackends enum.
"""

# Platform Imports
from enum import IntEnum

class ConfigurationBackends(IntEnum):

    """Contains the list of supported configuration backends for storing the
    runtime configuration.

    Attributes:
        NOT_SET: Default value
        DICTIONARY: In-memory dictionary
        REDIS: Redis

    Authors:
            Attila Kovacs
    """

    NOT_SET = 0         # Default value

    DICTIONARY = 1      # In-memory dictionary
    REDIS = 2           # Redis
