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
from typing import Any
from string import Template

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
FRAMEWORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
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

TEST_SERVER = \
"""
#!$shebang

import time
import sys
from typing import Any

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.pal.networking import ServerSocket, ClientThread
SERVER_PORT = 11492

class ExampleClientHandler(ClientThread):
    def handle_message(self, message: Any) -> None:
        if message == b'kill':
            raise SystemExit

def main() -> int:
    server = ServerSocket(
        port=SERVER_PORT,
        name='ServerSocketExample',
        client_handler=ExampleClientHandler)

    time.sleep(1)
    del server

    return 0

if __name__ == '__main__':
    main()
"""

TEST_SERVER = Template(TEST_SERVER).substitute(
    shebang=os.path.abspath(os.path.expanduser('~/.murasame/.env/bin/python')),
    framework_dir=FRAMEWORK_DIR)

TEST_CLIENT = \
"""
#!$shebang

import sys

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.pal.networking import ClientSocket, SocketMessageTransformer
SERVER_PORT = 11492

class ExampleMessageTransformer(SocketMessageTransformer):
    def transform(self, message: str) -> bytes:
        return bytes(message, encoding='utf-8')

def main() -> int:

    client = ClientSocket(
        name='ClientSocketExample',
        host='localhost',
        port=SERVER_PORT,
        transformer=ExampleMessageTransformer())

    client.connect()
    message = 'test'
    client.send(message)
    client.disconnect()
    del client

    return 0

if __name__ == '__main__':
    main()
"""

TEST_CLIENT = Template(TEST_CLIENT).substitute(
    shebang=os.path.abspath(os.path.expanduser('~/.murasame/.env/bin/python')),
    framework_dir=FRAMEWORK_DIR)

class ExampleClientThread(ClientThread):
    def handle_message(self, message: Any) -> None:
        if message == b'test':
            pass

class ExampleMessageTransformer(SocketMessageTransformer):
    def transform(self, message: str) -> bytes:
        return bytes(str(message), encoding='utf-8')

class TestSocket:

    """
    Contains unit tests for the socket wrappers.
    """

    def test_create_unencrypted_client_socket(self):

        """
        Tests that an unencrypted client socket can be created.
        """

        # STEP #1 - Client socket can be created with valid parameters
        sut = ClientSocket(name='testsocket', host='localhost', port=11492)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.UNENCRYPTED

        del sut

        # STEP #2 - Socket can't be created with invalid port
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

        # STEP #3 - Socket can't be created with invalid protocol
        with pytest.raises(InvalidInputError):
            sut = ClientSocket(
                name='testsocket',
                host='localhost',
                port=11492,
                ssl_protocol='invalidprotocol')

    # This test seems to throw a warning about a non-raisable exception in
    # pytest around the ServerSocket descructor not having _client_threads
    # which is not true. Might be related to pytest internally changing the
    # class structure? It seems to be a false positive, so ignore this warning
    # for now.
    @pytest.mark.filterwarnings('ignore')
    def test_create_unencrypted_server_socket(self):

        """
        Tests that an unencrypted server socket can be created.
        """

        # STEP #1 - Server socket can be created with valid parameters
        sut = ServerSocket(name='testsocket', host='', port=11492)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.UNENCRYPTED

        del sut

        # STEP #2 - Socket can't be created with invalid port
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

        # STEP #3 - Socket can't be created with invalid protocol
        with pytest.raises(InvalidInputError):
            sut = ServerSocket(
                name='testsocket',
                host='',
                port=11492,
                ssl_protocol='invalidprotocol')

    def test_create_tls12_client_socket(self):

        """
        Tests that a TLS v1.2 encrypted client socket can be created.
        """

        # STEP #1 - Client socket can be created with valid parameters
        sut = ClientSocket(
            name='testsocket',
            host='localhost',
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLSv12,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.TLSv12

        del sut

        # STEP #2 - Socket can't be created with invalid port
        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

    def test_create_tls12_server_socket(self):

        """
        Tests that a TLS v1.2 encrypted server socket can be created.
        """

        # STEP #1 - Server socket can be created with valid parameters
        sut = ServerSocket(
            name='testsocket',
            host='',
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLSv12,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.TLSv12

        del sut

        # STEP #2 - Socket can't be created with invalid port
        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ServerSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLSv12,
                               require_cert=False)

    def test_create_tls13_client_socket(self):

        """
        Tests that a TLS v1.3 encrypted client socket can be created.
        """

        # STEP #1 - Client socket can be created with valid parameters
        sut = ClientSocket(
            name='testsocket',
            host='localhost',
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLSv13,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.TLSv13

        del sut

        # STEP #2 - Socket can't be created with invalid port
        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

    def test_create_tls13_server_socket(self):

        """
        Tests that a TLS v1.3 encrypted server socket can be created.
        """

        # STEP #1 - Server socket can be created
        sut = ServerSocket(
            name='testsocket',
            host='',
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLSv13,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
        assert sut.Protocol == BaseSocket.Protocols.TLSv13

        del sut

        # STEP #2 - Socket can't be created with invalid port
        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port='invalidport',
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=-1,
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

        with pytest.raises(InvalidInputError):
            sut = ClientSocket(name='testsocket',
                               host='localhost',
                               port=123456789,
                               ssl_protocol=BaseSocket.Protocols.TLSv13,
                               require_cert=False)

    def test_message_sending(self):

        """
        Messages can be sent between sockets.
        """

        # Setup
        base_path = os.path.abspath(
            os.path.expanduser('~/.murasame/testfiles/socket'))

        if not os.path.isdir(base_path):
            os.mkdir(base_path)

        client_path = f'{base_path}/client.py'
        server_path = f'{base_path}/server.py'

        with open(client_path, 'w') as client_file:
            client_file.write(TEST_CLIENT)

        with open(server_path, 'w') as server_file:
            server_file.write(TEST_SERVER)

        current_dir = os.getcwd()
        os.chdir(base_path)

        # STEP #1 - Test sending from client socket

        try:
            subprocess.run('python server.py', shell=True, check=True)
        except subprocess.CalledProcessError as error:
            assert False

        client = ClientSocket(name='testsocket',
                              host='localhost',
                              port=11492,
                              transformer=ExampleMessageTransformer())
        client.connect(new_host='localhost', new_port=11492)
        client.send('testmessage')
        client.send('kill')
        client.disconnect()
        del client

        # STEP #2 - Test sending from server socket
        server = ServerSocket(name='testsocket',
                              port=11492,
                              transformer=ExampleMessageTransformer(),
                              client_handler=ExampleClientThread)

        try:
            subprocess.run('python client.py', shell=True, check=True)
        except subprocess.CalledProcessError as error:
            assert False

        # Cleanup
        os.chdir(current_dir)
        shutil.rmtree(base_path)
