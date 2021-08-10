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
Contains the implementation of the ClientThread class.
"""

# Runtime Imports
import socket
from threading import Thread
from typing import Any

# Murasame Imports
from murasame.constants import MURASAME_SOCKET_LOG_CHANNEL
from murasame.log import LogWriter

class ClientThread(Thread):

    """Prototype for the thread that is created for each client connection.

    Attributes:

        _parent_socket (ClientSocket): The parent socket this thread belongs
            to.

        _connection (Connection): The connection object to the client.

        _ip_address (str): The IP address of the client.

        _port (int): The port the client is connected from.

        _transformer (SocketMessageTransformer): The message transformer object
            to use.

        _handler_running (bool): Whether or not the connection handler thread
            should run.

        _receive_buffer_size (int): Size of the receive buffer.

        _logger (LogWriter): The log writer object to use when writing logs.

    Authors:
        Attila Kovacs
    """

    @property
    def Connection(self) -> object:

        """The connection object to the client.

        Authors:
            Attila Kovacs
        """

        return self._connection

    @property
    def IPAddress(self) -> str:

        """The IP address of the client.

        Authors:
            Attila Kovacs
        """

        return self._ip_address

    @property
    def Port(self) -> int:

        """The port the client connected from.

        Authors:
            Attila Kovacs
        """

        return self._port

    @property
    def IsRunning(self) -> bool:

        """Returns whether or not the main loop of the handler should be
        running.

        Authors:
            Attila Kovacs
        """

        return self._handler_running

    def __init__(
        self,
        parent_socket: 'ServerSocket',
        connection: object,
        ip_address: str,
        port: int,
        receive_buffer_size: int = 4096,
        transformer: 'SocketMessageTransformer' = None) -> None:

        """Creates a new ClientThread instance.

        Args:
            parent_socket (ServerSocket): The server socket this thread belongs
                to.

            connection (object): The connection object to the client.

            ip_address (str): The IP address of the client.

            port (int): The port the client connected from.

            receive_buffer_size (int): Size of the receive buffer of the
                socket.

            transformer (SocketMessageTransformer): The message transformer
                object to use.

        Authors:
            Attila Kovacs
        """

        super().__init__(name=f'ClientThread-{ip_address}:{port}', daemon=True)

        self._parent_socket = parent_socket
        self._connection = connection
        self._ip_address = ip_address
        self._port = port
        self._transformer = transformer
        self._handler_running = True
        self._receive_buffer_size = receive_buffer_size
        self._logger = LogWriter(
            channel_name=MURASAME_SOCKET_LOG_CHANNEL,
            cache_entries=True)

        self._logger.debug(
            f'Created client handler for {self.IPAddress}:{self.Port}.')

    def abort(self) -> None:

        """Aborts the main loop of the thread on the next execution if needed.

        Authors:
            Attila Kovacs
        """

        self._handler_running = False

    def run(self) -> None:

        """Main socket connection handler function.

        Authors:
            Attila Kovacs
        """

        self.on_handler_start()

        while self.IsRunning:

            # Read from the socket
            try:
                raw_data = self.Connection.recv(4096)
                print(f'RAW data received: {raw_data}')
                message_size = len(raw_data)
                self._parent_socket.increase_bytes_received(
                    bytes_received=message_size)
                self._logger.debug(
                    f'Received data from {self.IPAddress}:{self.Port}. '
                    f'Raw data: {str(raw_data)} ({message_size} bytes)')
            except socket.error as socket_error:
                self._logger.error(
                    f'Failed to receive message from client '
                    f'{self.IPAddress}:{self.Port}. Error: {socket_error}.')

            # Handle connection closure
            if not raw_data:
                self.abort()
                self._logger.debug(
                    f'Connection to {self.IPAddress}:{self.Port} has been '
                    f'closed.')
                self.on_abort()
                return

            # Transform the received_data
            data = raw_data
            if self._transformer is not None:
                data = self._transformer.deserialize(message=raw_data)

            self.handle_message(message=data)

    def send(self, message: Any) -> None:

        """Sends a message to the connected client.

        Args:
            message (Any): The message to send in the application's format.

        Authors:
            Attila Kovacs
        """

        raw_message = None

        if self._transformer:
            raw_message = self._transformer.serialize(message=message)
        else:
            raw_message = message

        message_size = len(raw_message)

        try:
            self.Connection.sendall(raw_message, message_size)
            self._parent_socket.increase_bytes_sent(message_size)
            self._logger.debug(
                f'Sending message {raw_message}  ({message_size} bytes) over '
                f'socket {self._parent_socket.Name}.')
        except socket.error:
            self._logger.error(
                f'Failed to send message {str(raw_message)} over socket '
                f'{self._parent_socket.Name}.')

    def handle_message(self, message: Any) -> None:

        """Message handler function that has to be implemented by all client
        handler objects.

        Args:
            message (Any): The message that was received on the socket.

        Raises:
            NotImplementedError: Raised if the function is not implemented by
                the derived class.

        Authors:
            Attila Kovacs
        """

        del message

        raise NotImplementedError(
            f'ClientThread.handle_message() has to be implemented in '
            f'{self.__class__.__name__}.')

    def on_handler_start(self) -> None:

        """Handler function that can be implemented by derived classes to
        execute logic just before the client handler loop starts.

        Authors:
            Attila Kovacs
        """

        # Disable no self use warning as this is only an interface definition
        #pylint: disable=no-self-use

    def on_abort(self) -> None:

        """Handler function that can be implemented by derived classes to
        execute logic when the connection is closed.

        Authors:
            Attila Kovacs
        """

        # Disable no self use warning as this is only an interface definition
        #pylint: disable=no-self-use
