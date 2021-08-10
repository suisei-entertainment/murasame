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
from murasame.constants import MURASAME_SOCKET_LOG_CHANNEL
from murasame.log import LogWriter

class SocketMessageTransformer(LogWriter):

    """Utility class used to transform messages sent or received through a
    socket.

    Users need to supply their own transformer implementations.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new SocketMessageTransformer object.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_SOCKET_LOG_CHANNEL,
                         cache_entries=True)

    def serialize(self, message: Any) -> bytes:

        """Transformation function used to transform all messages sent
        through a socket.

        Args:
            message (Any): The message to send in the application's format.

        Returns:
            bytes: The message transformed to a byte array.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'SocketMessageTransformer.serialize() has to be implemented in '
            f'{self.__class__.__name__}.')

    def deserialize(self, message: bytes) -> Any:

        """Transformation function used to transform all messages received
        through a socket.

        Args:
            message (bytes): The message that has been received.

        Returns:
            Any: The messages transformed to the application's format.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'SocketMessageTransformer.deserialize() has to be implemented in '
            f'{self.__class__.__name__}.')
