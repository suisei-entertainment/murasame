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
Contains the implementation of the ClientSocket class.
"""

# Runtime Imports
import socket
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.networking.basesocket import BaseSocket

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
            self.increase_bytes_sent(bytes_sent=message_size)
            self.debug(
                f'Sending message {raw_message}  ({message_size} bytes) over '
                f'socket {self.Name}.')
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
