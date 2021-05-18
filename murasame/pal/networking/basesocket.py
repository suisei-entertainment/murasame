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
Contains the implementation of the BaseSocket class.
"""

# Runtime Imports
import socket
import ssl
from enum import IntEnum

# Murasame Imports
from murasame.exceptions import InvalidInputError, MissingRequirementError
from murasame.logging import LogWriter
from murasame.pal.networking.constants import SOCKET_LOG_CHANNEL

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
            socket.SOCK_STREAM)
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
