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
Contains the implementation of the SocketMessageTransformer class.
"""

# Runtime Imports
from typing import Any

# Murasame Imports
from murasame.logging import LogWriter
from murasame.pal.networking.constants import SOCKET_LOG_CHANNEL

class SocketMessageTransformer(LogWriter):

    """
    Utility class used to transform messages sent or received through a socket.

    Users need to supply their own transformer implementations.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new SocketMessageTransformer object.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=SOCKET_LOG_CHANNEL,
                         cache_entries=True)

    def transform(self, message: Any) -> bytes:

        """
        Transformation function used to transform all messages sent or received
        through a socket.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'SocketMessageTransformer.transform() has to be implemented in '
            f'{self.__class__.__name__}.')
