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
Contains the socket wrappers of the framework.
"""

# Runtime Imports
import socket
import ssl

from threading import Thread
from enum import IntEnum
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError, MissingRequirementError
from murasame.logging import LogWriter

SOCKET_LOG_CHANNEL = 'murasame.pal.networking.socket'
"""
Name of the log channel all socket implementations should use.
"""

class BaseSocket(LogWriter):

    """
    Utility class that encapsulates basic socket functionality for
    communicating over the network.

    Authors:
        Attila Kovacs
    """

    class Protocols(IntEnum):

        """
        The list of supported SSL protocol versions.

        Authors:
            Attila Kovacs
        """

        UNKNOWN = 0 # Unknown

        UNENCRYPTED = 1 # Unencrypted

        TLSv12 = 2  # TLS v1.2
        TLSv13 = 3  # TLS v1.3

    class Purposes(IntEnum):

        """
        The list of supported authentication purposes for the SSL context.

        Authors:
            Attila Kovacs
        """

        UNKNOWN = 0

        CLIENT_AUTH = 1
        SERVER_AUTH = 2

    @property
    def Name(self) -> str:

        """
        Name of the socket.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def IsConnected(self) -> bool:

        """
        Returns whether or not the socket is connected to the remote end.

        Authors:
            Attila Kovacs
        """

        return self._connected

    @property
    def Protocol(self) -> 'BaseSocket.Protocols':

        """
        The SSL protocol the socket is using.

        Authors:
            Attila Kovacs
        """

        return self._ssl_protocol

    def __init__(
        self,
        name: str = None,
        ssl_protocol: 'BaseSocket.Protocols' = 'BaseSocket.Protocols.UNENCRYPTED',
        cert_file: str = None,
        ca_list: str = None,
        require_cert: bool = True,
        purpose: 'BaseSocket.Purposes' = 'BaseSocket.Purposes.SERVER_AUTH') -> None:

        """
        Creates a new BaseSocket instance.

        Args:
            name:               Name of the socket.
            ssl_protocol:       The SSL protocol to use when setting up the
                                socket.
            cert_file:          The certificate file to use when establishing
                                the connection.
            ca_list:            The certificate authority to use when
                                validating the SSL connection.
            require_cert:       Whether or not a valid certificate is required
                                during authentication.
            purpose:            The purpose of the SSL connection.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=SOCKET_LOG_CHANNEL,
                         cache_entries=True)

        self._name = '' if name is None else name
        """
        Name of the socket.
        """

        self._socket = None
        """
        The underlying socket object that is used.
        """

        self._raw_socket = None
        """
        The actual native socket object that is either unencrypted or
        wrapped in an SSL context when exposed for use.
        """

        self._context = None
        """
        The SSL context used by socket in encrypted mode.
        """

        self._connected = False
        """
        Marks whether or not the socket is connected to a remote end.
        """

        self._ssl_protocol = ssl_protocol
        """
        The SSL protocol that is used by the socket.
        """

        self._cert_file = cert_file
        """
        The certificate file to use when establishing a connection.
        """

        self._ca_list = ca_list
        """
        The certificate authority to use when validating the connection.
        """

        self._require_cert = require_cert
        """
        Whether or not a valid certificate is required during authentication.
        """

        try:
            self._create_socket(purpose)
        except InvalidInputError as exception:
            self.error(
                f'Failed to create socket. Reason: {exception.errormessage}.')
            raise

    def _create_socket(self, purpose: 'BaseSocket.Purposes') -> None:

        """
        Creates the socket based on the initial configuration.

        Args:
            purpose:            The purpose of the SSL connection.

        Authors:
            Attila Kovacs
        """

        # Create the socket
        self._raw_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
        self._raw_socket.setblocking(True)

        # Encrypt the socket if required
        if self._ssl_protocol == BaseSocket.Protocols.UNENCRYPTED:
            self._socket = self._raw_socket
            self.debug('Successfully created unencrypted socket.')
        else:
            self._encrypt_socket(purpose)
            self.debug('Successfully created encrypted socket.')

    def _encrypt_socket(self, purpose: 'BaseSocket.Purposes') -> None:

        """
        Encrypts the socket based on the selected encryption protocol.

        Raises:
            InvalidInputError:          Raised when trying to encrpyt by using
                                        an unsupported protocol.
            InvalidInputError:          Raised when trying to use an
                                        unsupported SSL context purpose.
            MissingRequirementError:    Raised when TLS v1.2 or TLS v1.3 is not
                                        supported by the plaform but the socket
                                        is configured to use it.

        Args:
            purpose:            The purpose of the SSL connection.

        Authors:
            Attila Kovacs
        """

        self.debug('Encrypting socket...')

        supported_protocols = \
        [
            BaseSocket.Protocols.TLSv12,
            BaseSocket.Protocols.TLSv13
        ]

        if self._ssl_protocol not in supported_protocols:
            raise InvalidInputError(
                f'Unsupported SSL protocol version {self._ssl_protocol} when '
                f'creating socket.')

        # Default context options for TLS v1.2
        if not ssl.HAS_TLSv1_2:
            raise MissingRequirementError(
                'TLS v1.2 is not supported by the platform, cannot '
                'create socket.')

        context_options = \
            ssl.OP_ALL|ssl.OP_NO_TLSv1|ssl.OP_NO_TLSv1_1|ssl.OP_NO_SSLv2|ssl.OP_NO_SSLv3

        # Overwrite the context options if TLS v1.3 is enforced
        if self._ssl_protocol == BaseSocket.Protocols.TLSv13:

            if not ssl.HAS_TLSv1_3:
                raise MissingRequirementError(
                    'TLS v1.3 is not supported by the platform, cannot '
                    'create socket.')

            context_options = \
                ssl.OP_ALL|ssl.OP_NO_TLSv1|ssl.OP_NO_TLSv1_1|ssl.OP_NO_TLSv1_2|ssl.OP_NO_SSLv2|ssl.OP_NO_SSLv3

        self.debug(f'Context options: {context_options}')

        # Set the purpose for context creation
        ssl_purpose = None
        if purpose == BaseSocket.Purposes.CLIENT_AUTH:
            ssl_purpose=ssl.Purpose.CLIENT_AUTH
            self.debug('Creating encrypted socket for client authentication.')
        elif purpose == BaseSocket.Purposes.SERVER_AUTH:
            ssl_purpose=ssl.Purpose.SERVER_AUTH
            self.debug('Creating encrypted socket for server authentication.')
        else:
            raise InvalidInputError(
                f'Unsupported SSL context purpose {purpose} when creating '
                f'the socket.')

        self._context = ssl.create_default_context(
            purpose=ssl_purpose,
            cafile=self._ca_list)

        # Set context verification mode to always require a valid certificate
        # unless otherwise configured, but disable hostname checking.
        self._context.check_hostname = False

        if self._require_cert:
            self._context.verify_mode = ssl.CERT_REQUIRED
            self.debug(
                'Creating encrypted socket with certificate validation '
                'enabled.')
        else:
            self._context.verify_mode = ssl.CERT_NONE
            self.warning(
                'Creating an encrypted socket without requiring a '
                'certificate is unsafe.')

        # Set options
        self._context.options = context_options

        # Load the certificate chain to use.
        if self._cert_file:
            self._context.load_cert_chain(self._cert_file)

        # Wrap the socket
        self._socket = self._context.wrap_socket(self._raw_socket)

        self.debug('Socket encrypted.')

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

class ClientSocket(BaseSocket):

    """
    Represents a socket to be used by a client connecting to a remote host.

    Authors:
        Attila Kovacs
    """

    @property
    def Host(self) -> str:

        """
        The host the socket is connected to.

        Authors:
            Attila Kovacs
        """

        return self._host

    @property
    def Port(self) -> int:

        """
        The port the socket is connected to.

        Authors:
            Attila Kovacs
        """

        return self._port

    def __init__(self,
                 host: str,
                 port: int,
                 name: str = None,
                 transformer: 'SocketMessageTransformer' = None,
                 ssl_protocol: BaseSocket.Protocols = BaseSocket.Protocols.UNENCRYPTED,
                 cert_file: str = None,
                 ca_list: str = None,
                 require_cert: bool = True) -> None:

        """
        Creates a new ClientSocket instance.

        Args:
            host:               The remote host to connect to.
            port:               The remote port to connect to.
            name:               The name of the socket.
            transformer:        The message transformer to use.
            ssl_protocol:       The SSL protocol to use when setting up the
                                socket.
            cert_file:          The certificate file to use when establishing
                                the connection.
            ca_list:            The certificate authority to use when
                                validating the SSL connection.
            require_cert:       Whether or not a valid certificate is required
                                during authentication.

        Raises:
            InvalidInputError:      Raised when an invalid port number is
                                    provided.

        Authors:
            Attila Kovacs
        """

        super().__init__(name=name,
                         ssl_protocol=ssl_protocol,
                         cert_file=cert_file,
                         ca_list=ca_list,
                         require_cert=require_cert,
                         purpose=BaseSocket.Purposes.SERVER_AUTH)

        self._host = host
        """
        The remote host to connect to.
        """

        self._port = port
        """
        The remote port to connect to.
        """

        self._transformer = transformer
        """
        The message transformer object to use.
        """

        try:
            self._validate_port(port)
        except InvalidInputError as exception:
            self.error(
                f'Failed to create socket due to invalid port. '
                f'Reason: {exception.errormessage}')
            raise

    def __del__(self) -> None:

        """
        Destructor. Makes sure that the socket is closed upon destruction.

        Authors:
            Attila Kovacs
        """

        if self.IsConnected:
            self._socket.close()
            del self._socket
            del self._raw_socket
            self._connected = False

    def connect(self, new_host: str = None, new_port: int = None) -> None:

        """
        Establishes the connection to the specified host on the configured
        port.

        Args:
            new_host:       Optional new host that overwrites the existing host
                            if specified.
            new_port:       Optional new port that overwrites the existing port
                            if specified.

        Authors:
            Attila Kovacs
        """

        # Set new host is requested
        if new_host is not None:
            self.debug(f'Changing host from {self._host} to {new_host}.')
            self._host = new_host

        # Set new port if requested
        if new_port is not None:
            try:
                self._validate_port(port=new_port)
                self._port = new_port
            except InvalidInputError as exception:
                self.error(
                    f'Trying to overwrite the port to invalid value in '
                    f'connect(){new_port}. Error: {exception.errormessage}. '
                    f'New port is ignored.')

        self.debug(f'Connecting to {self._host}:{self._port}...')

        # Disconnect the previous connection if the socket is already connected
        if self.IsConnected:
            self.debug(
                f'Socket is already connected to {self._host}:{self._port}. '
                f'Disconnecting...')
            self.disconnect()

        # Establish the connection
        try:
            self._socket.connect((self._host, self._port))
            self._connected = True
        except socket.error as socket_error:
            self.error(f'Failed to open socket to {self._host}:{self._port}. '
                       f'Reason: {socket_error}.')
            return

        self.debug(f'Connection established to {self._host}:{self._port}.')

    def disconnect(self) -> None:

        """
        Disconnects the socket.

        Authors:
            Attila Kovacs
        """

        if self.IsConnected:
            self.debug(f'Disconnecting from {self._host}:{self._port}.')
            self._socket.close()
            self._connected = False

    def send(self, message: Any) -> None:

        """
        Sends a message over the socket.

        Args:
            message:        The message to send.

        Authors:
            Attila Kovacs
        """

        raw_message = None

        if self._transformer:
            raw_message = self._transformer.transform(message)
        else:
            raw_message = message

        message_size = len(raw_message)

        try:
            self._socket.sendall(raw_message, message_size)
            self.debug(
                f'Sending message {raw_message} over socket {self.Name}.')
        except socket.error:
            self.error(
                f'Failed to send message {str(raw_message)} over socket '
                f'{self.Name}.')

    def _validate_port(self, port: int) -> None:

        """
        Validates the given port,

        Args:
            port:       The port number to validate.

        Raises:
            InvalidInputError:      Raised when an invalid port number is
                                    provided.

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

class ClientThread(Thread):

    """
    Prototype for the thread that is created for each client connection.

    Authors:
        Attila Kovacs
    """

    @property
    def Connection(self) -> object:

        """
        The connection object to the client.

        Authors:
            Attila Kovacs
        """

        return self._connection

    @property
    def IPAddress(self) -> str:

        """
        The IP address of the client.

        Authors:
            Attila Kovacs
        """

        return self._ip_address

    @property
    def Port(self) -> int:

        """
        The port the client connected from.
        """

        return self._port

    @property
    def IsRunning(self) -> bool:

        """
        Returns whether or not the main loop of the handler should be running.
        """

        return self._handler_running

    def __init__(
        self,
        connection: object,
        ip_address: str,
        port: int,
        receive_buffer_size: int = 4096,
        transformer: 'SocketMessageTransformer' = None) -> None:

        """
        Creates a new ClientThread instance.

        Args:
            connection:             The connection object to the client.
            ip_address:             The IP address of the client.
            port:                   The port the client connected from.
            receive_buffer_size:    Size of the receive buffer of the socket.
            transformer:            The message transformer object to use.
        """

        super().__init__(name=f'ClientThread-{ip_address}:{port}', daemon=True)

        self._connection = connection
        """
        The connection object to the client.
        """

        self._ip_address = ip_address
        """
        The IP address of the client.
        """

        self._port = port
        """
        The port the client is connected from.
        """

        self._transformer = transformer
        """
        The message transformer object to use.
        """

        self._handler_running = True
        """
        Whether or not the connection handler thread should run.
        """

        self._receive_buffer_size = receive_buffer_size
        """
        Size of the receive buffer.
        """

        self._logger = LogWriter(
            channel_name=SOCKET_LOG_CHANNEL,
            cache_entries=True)

        self._logger.debug(
            f'Created client handler for {self.IPAddress}:{self.Port}.')

    def abort(self) -> None:

        """
        Aborts the main loop of the thread on the next execution if needed.

        Authors:
            Attila Kovacs
        """

        self._handler_running = False

    def run(self) -> None:

        """
        Main socket connection handler function.

        Authors:
            Attila Kovacs
        """

        self.on_handler_start()

        while self.IsRunning:

            # Read from the socket
            try:
                raw_data = self.Connection.recv(4096)
                self._logger.debug(
                    f'Received data from {self.IPAddress}:{self.Port}. '
                    f'Raw data: {str(raw_data)}')
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
                data = self._transformer.transform(message=raw_data)

            self.handle_message(message=data)

    def handle_message(self, message: Any) -> None:

        """
        Message handler function that has to be implemented by all client
        handler objects.

        Args:
            message:        The message that was received on the socket.

        Raises:
            NotImplementedError:        Raised if the function is not
                                        implemented by the derived class.

        Authors:
            Attila Kovacs
        """

        del message

        raise NotImplementedError(
            f'ClientThread.handle_message() has to be implemented in '
            f'{self.__class__.__name__}.')

    def on_handler_start(self) -> None:

        """
        Handler function that can be implemented by derived classes to
        execute logic just before the client handler loop starts.

        Authors:
            Attila Kovacs
        """

        # Disable no self use warning as this is only an interface definition
        #pylint: disable=no-self-use

    def on_abort(self) -> None:

        """
        Handler function that can be implemented by derived classes to execute
        logic when the connection is closed.

        Authors:
            Attila Kovacs
        """

        # Disable no self use warning as this is only an interface definition
        #pylint: disable=no-self-use

class ServerSocket(BaseSocket):

    """
    Represents a socket running on the server side serving client connections.

    Authors:
        Attila Kovacs
    """

    @property
    def Host(self) -> str:

        """
        The host the socket is listening on.

        Authors:
            Attila Kovacs
        """

        return self._host

    @property
    def Port(self) -> int:

        """
        The port the socket is listening on.

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

        """
        Creates a new ServerSocket instance.

        Args:
            port:               The network port to listen on.
            host:               The network interface to listen on.
            name:               The name of the socket.
            transformer:        The message transformer object.
            client_handler:     A ClientThread class that will handle client
                                connections.
            ssl_protocol:       The SSL protocol to use when setting up the
                                socket.
            cert_file:          The certificate file to use when establishing
                                the connection.
            ca_list:            The certificate authority to use when
                                validating the SSL connection.
            require_cert:       Whether or not a valid certificate is required
                                during authentication.

        Raises:
            RuntimeError:       Raised when the socket cannot be created.

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
        """
        The local network interface to listen on.
        """

        self._port = port
        """
        The local port to listen on.
        """

        self._transformer = transformer
        """
        The message transformer object to use.
        """

        self._client_handler = client_handler
        """
        The client handler class that will be created for each connecting
        client.
        """

        self._socket_thread = None
        """
        The thread that is running the listen loop of the socket.
        """

        self._client_threads = []
        """
        The list of client threads handling a client connection.
        """

        self._handler_running = False
        """
        Whether or not the connection handler thread should run.
        """

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

        """
        Destructor. Makes sure that the socket is closed upon destruction.

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

        """
        Validates the given port,

        Args:
            port:       The port number to validate.

        Raises:
            InvalidInputError:      Raised when an invalid port number is
                                    provided.

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

        """
        The main listening loop of the server socket.

        Authors:
            Attila Kovacs
        """

        while self._handler_running:
            self._socket.listen(5)
            (connection, (ip_address, port)) = self._socket.accept()
            connection_handler = self._client_handler(
                connection=connection,
                ip_address=ip_address,
                port=port,
                transformer=self._transformer)
            self._client_threads.append(connection_handler)
            connection_handler.start()
