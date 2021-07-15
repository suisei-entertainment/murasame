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
Contains the implementation of the ServerSocket class.
"""

# Runtime Imports
import socket
from threading import Thread

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.networking.basesocket import BaseSocket

class ServerSocket(BaseSocket):

    """Represents a socket running on the server side serving client
    connections.

    Arguments:
        _host (str): The local network interface to listen on.

        _port (int): The local port to listen on.

        _transformer (SocketMessageTransformer): The message transformer object
            to use.

        _client_handler (ClientHandler): The client handler class that will be
            created for each connecting client.

        _socket_thread (Thread): The thread that is running the listen loop of
            the socket.

        _client_threads (list): The list of client threads handling a client
            connection.

        _handler_running (bool): Whether or not the connection handler thread
            should run.

    Authors:
        Attila Kovacs
    """

    @property
    def Host(self) -> str:

        """The host the socket is listening on.

        Authors:
            Attila Kovacs
        """

        return self._host

    @property
    def Port(self) -> int:

        """The port the socket is listening on.

        Authors:
            Attila Kovacs
        """

        return self._port

    def __init__(self,
                 port: int,
                 host: str = '',
                 name: str = None,
                 transformer: 'SocketMessageTransformer' = None,
                 client_handler: 'ClientThread' = None,
                 ssl_protocol: BaseSocket.Protocols = BaseSocket.Protocols.UNENCRYPTED,
                 cert_file: str = None,
                 ca_list: str = None,
                 require_cert: bool = True) -> None:

        """Creates a new ServerSocket instance.

        Args:
            port (int): The network port to listen on.

            host (str): The network interface to listen on.

            name (str): The name of the socket.

            transformer (SocketMessageTransformer): The message transformer
                object.

            client_handler (ClientThread): A ClientThread class that will
                handle client connections.

            ssl_protocol (Protocols): The SSL protocol to use when setting up
                the socket.

            cert_file (str): The certificate file to use when establishing the
                connection.

            ca_list (str): The certificate authority to use when validating the
                SSL connection.

            require_cert (bool): Whether or not a valid certificate is required
                during authentication.

        Raises:
            RuntimeError: Raised when the socket cannot be created.

        Authors:
            Attila Kovacs
        """

        super().__init__(name=name,
                         ssl_protocol=ssl_protocol,
                         cert_file=cert_file,
                         ca_list=ca_list,
                         require_cert=require_cert,
                         purpose=BaseSocket.Purposes.CLIENT_AUTH)

        self._host = host
        self._port = port
        self._transformer = transformer
        self._client_handler = client_handler
        self._socket_thread = None
        self._client_threads = []
        self._handler_running = False

        self.debug(f'Creating server socket for {host}:{port}...')

        try:
            self._validate_port(port)
        except InvalidInputError as exception:
            self.error(
                f'Failed to create socket due to invalid port. '
                f'Reason: {exception.errormessage}')
            raise

        # Set socket options
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Start listening
        try:
            self._socket.bind((self._host, self._port))
            if self._client_handler:
                self._socket_thread = Thread(
                    target=self._main_loop,
                    name=f'Socket {self.Name} handler thread.',
                    daemon=True)
                self._handler_running = True
                self._socket_thread.start()
        except socket.error as socket_error:
            self.error(f'Failed to create server socket for {host}:{port}. '
                       f'Reason: {socket_error}')
            raise RuntimeError from socket_error

        self.debug('Server socket created.')

    def __del__(self) -> None:

        """Destructor. Makes sure that the socket is closed upon destruction.

        Authors:
            Attila Kovacs
        """

        if self._client_threads:
            for client in self._client_threads:
                client.abort()
                client.join()

        self._handler_running = False
        if self._socket_thread:
            self._socket_thread.join()

        self._socket.close()
        del self._socket
        del self._raw_socket

    def _validate_port(self, port: int) -> None:

        """Validates the given port.

        Args:
            port (int): The port number to validate.

        Raises:
            InvalidInputError: Raised when an invalid port number is provided.

        Authors:
            Attila Kovacs
        """

        # Convert port number to integer
        if not isinstance(port, int):
            try:
                self._port = int(port)
            except ValueError as exception:
                raise InvalidInputError(
                    f'Invalid port number format detected in '
                    f'socket. Port: {port}') from exception

        # Validate the port
        if self._port <=0 or self._port > 65535:
            raise InvalidInputError(
                f'Port number {self._port} is outside allowed range of '
                f'1-65535.')

    def _main_loop(self) -> None:

        """The main listening loop of the server socket.

        Authors:
            Attila Kovacs
        """

        while self._handler_running:
            self._socket.listen(5)
            (connection, (ip_address, port)) = self._socket.accept()
            connection_handler = self._client_handler(
                parent_socket=self,
                connection=connection,
                ip_address=ip_address,
                port=port,
                transformer=self._transformer)
            self._client_threads.append(connection_handler)
            connection_handler.start()
