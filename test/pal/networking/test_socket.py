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
Contains the unit tests of socket wrappers.
"""

# Runtime Imports
import os
import sys
import shutil
import subprocess
import time
import socket
from typing import Any
from string import Template

# Dependency Imports
import pytest
import psutil
from xprocess import ProcessStarter

# Fix paths to make framework modules accessible
FRAMEWORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, FRAMEWORK_DIR)

# Murasame Imports
from murasame.pal.networking import \
(
    BaseSocket,
    ClientSocket,
    ServerSocket,
    ClientThread,
    SocketMessageTransformer
)
from murasame.exceptions import InvalidInputError

# Test Imports
from test.constants import SHEBANG_STRING

BASE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/socket'))

class ExampleClientThread(ClientThread):
    def handle_message(self, message: Any) -> None:
        if message == b'test':
            pass

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        message = message + os.linesep
        serialized_message = bytes(str(message), encoding='utf-8')
        return serialized_message
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf-8').strip()

class TestSocket:

    """
    Contains unit tests for the socket wrappers.

    Authors:
        Attila Kovacs
    """

    def test_create_unencrypted_client_socket(self):

        """
        Tests that an unencrypted client socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ClientSocket(name='testsocket', host='localhost', port=11495)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11495
        assert sut.Protocol == BaseSocket.Protocols.UNENCRYPTED

        del sut

    def test_create_unencrypted_client_socket_with_invalid_port(self):

        """
        Tests creation of a client socket with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport')

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789)

    def test_create_unencrypted_client_socket_with_invalid_protocol(self):

        """
        Tests creation of a client socket with invalid protocol.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(
                name='testsocket',
                host='localhost',
                port=11496,
                ssl_protocol='invalidprotocol')

    # This test seems to throw a warning about a non-raisable exception in
    # pytest around the ServerSocket descructor not having _client_threads
    # which is not true. Might be related to pytest internally changing the
    # class structure? It seems to be a false positive, so ignore this warning
    # for now.
    @pytest.mark.filterwarnings('ignore')
    def test_create_unencrypted_server_socket(self):

        """
        Tests that an unencrypted server socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ServerSocket(name='testsocket', host='', port=11497)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11497
        assert sut.Protocol == BaseSocket.Protocols.UNENCRYPTED

        del sut

    def test_create_unencrypted_server_socket_with_invalid_port(self):

        """
        Test creation of unencrypted server socket with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port='invalidport')

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=-1)

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=123456789)

    # This test seems to throw a warning about a non-raisable exception in
    # pytest around the ServerSocket descructor not having _client_threads
    # which is not true. Might be related to pytest internally changing the
    # class structure? It seems to be a false positive, so ignore this warning
    # for now.
    @pytest.mark.filterwarnings('ignore')
    def test_create_unencrypted_server_socket_with_invalid_protocol(self):

        """
        Test creation of unencrypted server socket with invalid protocol.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(
                name='testsocket',
                host='',
                port=11492,
                ssl_protocol='invalidprotocol')

    def test_create_tls12_client_socket(self):

        """
        Tests that a TLS v1.2 encrypted client socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ClientSocket(
            name='testsocket',
            host='localhost',
            port=11499,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11499
        assert sut.Protocol == BaseSocket.Protocols.TLS_V_1_2

        del sut

    def test_create_tls12_client_socket_with_invalid_port(self):

        """
        Tests TLS v1.2 client socket creation with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

    def test_create_tls12_server_socket(self):

        """
        Tests that a TLS v1.2 encrypted server socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ServerSocket(
            name='testsocket',
            host='',
            port=11500,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11500
        assert sut.Protocol == BaseSocket.Protocols.TLS_V_1_2

        del sut

    def test_create_tls12_server_socket_with_invalid_port(self):

        """
        Tests creation of TLSv1.2 server socket with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
                               require_cert=False)

    def test_create_tls13_client_socket(self):

        """
        Tests that a TLS v1.3 encrypted client socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ClientSocket(
            name='testsocket',
            host='localhost',
            port=11501,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11501
        assert sut.Protocol == BaseSocket.Protocols.TLS_V_1_3

        del sut

    def test_create_tls13_client_socket_with_invalid_port(self):

        """
        Test creation of TLSv1.3 client socket with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

    def test_create_tls13_server_socket(self):

        """
        Tests that a TLS v1.3 encrypted server socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ServerSocket(
            name='testsocket',
            host='',
            port=11502,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11502
        assert sut.Protocol == BaseSocket.Protocols.TLS_V_1_3

        del sut

    def test_create_tls13_server_socket_with_invalid_port(self):

        """
        Tests creation of TLSv1.3 server socket with invalid port.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
                               require_cert=False)

    def test_message_sending_from_client_socket(self):

        """
        Messages can be sent between sockets from a client socket.

        Authors:
            Attila Kovacs
        """

        client = ClientSocket(name='testsocket',
                              host='localhost',
                              port=11492,
                              transformer=ExampleMessageTransformer())
        client.connect(new_host='localhost', new_port=11492)
        assert client.IsConnected

        client.send('testmessage')
        response = client.receive()
        if response != 'testresponse':
            # Make sure that the server is stopped even if the check fails
            client.send('kill')
            assert False

        # Shut down the server
        client.send('kill')

        del client

    def test_message_sending_from_server_socket(self):

        """
        Messages can be sent between sockets from a server socket.

        Authors:
            Attila Kovacs
        """

        server = ServerSocket(name='testsocket',
                              port=11493,
                              transformer=ExampleMessageTransformer(),
                              client_handler=ExampleClientThread)

        client_script = f'{BASE_PATH}/client.py'

        try:
            subprocess.run(f'python {client_script}', shell=True, check=True)
        except subprocess.CalledProcessError as error:
            assert False
