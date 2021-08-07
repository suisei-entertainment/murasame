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
from typing import Any
from string import Template

# Dependency Imports
import pytest
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

SERVER_PORT = 11492

BASE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/socket'))

TEST_SERVER = \
"""
#!$shebang

import time
import sys
import _thread
from typing import Any

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.pal.networking import ServerSocket, ClientThread, SocketMessageTransformer
SERVER_PORT = $server_port

class ExampleClientHandler(ClientThread):
    def handle_message(self, message: Any) -> None:
        print(f'Message received: {message}')
        if message == 'testmessage':
            print('Sending response...')
            self.send('testresponse')
            print('Response sent.')
        elif message == 'kill':
            print('Kill message received, interrupting main thread.')
            _thread.interrupt_main()
        else:
            print('Unknown message')

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        return bytes(str(message), encoding='utf-8')
    def deserialize(self, message: bytes) -> str:
        print(f'RAW message: {message}')
        deserialized = str(message, encoding='utf-8')
        print(f'Deserialized message: {deserialized}') 
        return deserialized

def main() -> int:

    print('Starting server...')

    server = ServerSocket(
        port=SERVER_PORT,
        name='ServerSocketExample',
        client_handler=ExampleClientHandler,
        transformer=ExampleMessageTransformer())

    print(f'Server is listening on port {SERVER_PORT}.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting main loop...')
        
    print('Cleanup...')
    del server

    return 0

if __name__ == '__main__':
    main()
"""

TEST_SERVER = Template(TEST_SERVER).substitute(
    shebang=os.path.abspath(os.path.expanduser('~/.murasame/.env/bin/python')),
    server_port=SERVER_PORT,
    framework_dir=FRAMEWORK_DIR)

@pytest.fixture()
def start_server(xprocess):

    if not os.path.isdir(BASE_PATH):
            os.mkdir(BASE_PATH)

    server_script = f'{BASE_PATH}/server.py'

    with open(server_script, 'w') as server_file:
            server_file.write(TEST_SERVER)

    class Starter(ProcessStarter):
        pattern = f'Server is listening on port {SERVER_PORT}.'
        args = ['python', server_script]
        terminate_on_interrupt = True
        timeout=10

    logfile = xprocess.ensure('socketserver', Starter)

    yield

    xprocess.getinfo('socketserver').terminate()

TEST_CLIENT = \
"""
#!$shebang

import sys

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.pal.networking import ClientSocket, SocketMessageTransformer
SERVER_PORT = $server_port

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        return bytes(message, encoding='utf-8')
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf-8')

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
    server_port=SERVER_PORT,
    framework_dir=FRAMEWORK_DIR)

class ExampleClientThread(ClientThread):
    def handle_message(self, message: Any) -> None:
        if message == b'test':
            pass

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        serialized_message = bytes(str(message), encoding='utf-8')
        return serialized_message
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf-8')

class TestSocket:

    """
    Contains unit tests for the socket wrappers.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        if not os.path.isdir(BASE_PATH):
            os.mkdir(BASE_PATH)

        client_path = f'{BASE_PATH}/client.py'

        with open(client_path, 'w') as client_file:
            client_file.write(TEST_CLIENT)

    @classmethod
    def teardown_class(cls):

        shutil.rmtree(BASE_PATH)

    def test_create_unencrypted_client_socket(self):

        """
        Tests that an unencrypted client socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ClientSocket(name='testsocket', host='localhost', port=11492)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
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
        Tests that an unencrypted server socket can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ServerSocket(name='testsocket', host='', port=11492)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
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
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
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
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_2,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
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
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == 'localhost'
        assert sut.Port == 11492
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
            port=11492,
            ssl_protocol=BaseSocket.Protocols.TLS_V_1_3,
            require_cert=False)

        assert sut.Name == 'testsocket'
        assert sut.Host == ''
        assert sut.Port == 11492
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

    #def test_message_sending_from_client_socket(self, start_server):

        #"""
        #Messages can be sent between sockets from a client socket.

        #Authors:
        #    Attila Kovacs
        #"""

        #client = ClientSocket(name='testsocket',
        #                      host='localhost',
        #                      port=11492,
        #                      transformer=ExampleMessageTransformer())
        #client.connect(new_host='localhost', new_port=11492)
        #assert client.IsConnected

        #client.send('testmessage')
        #response = client.receive()
        #assert response == 'testresponse'

        #del client

    def test_message_sending_from_server_socket(self):

        """
        Messages can be sent between sockets from a server socket.

        Authors:
            Attila Kovacs
        """

        server = ServerSocket(name='testsocket',
                              port=11492,
                              transformer=ExampleMessageTransformer(),
                              client_handler=ExampleClientThread)

        client_script = f'{BASE_PATH}/client.py'

        try:
            subprocess.run(f'python {client_script}', shell=True, check=True)
        except subprocess.CalledProcessError as error:
            assert False
