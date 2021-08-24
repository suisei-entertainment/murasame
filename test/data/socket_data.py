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
Contains the test data for the socket tests.
"""

# Runtime Imports
import os
import subprocess
from string import Template

# Test Imports
from test.constants import TEST_FILES_DIRECTORY, SHEBANG_STRING

FRAMEWORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

SERVER_TEST_SERVER_PORT = 11492

TEST_SERVER = \
"""
$shebang

import os
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
        elif message == 'hello':
            print('Sending hello response...')
            self.send('hello')
            print('Response sent.')
        elif message == 'kill':
            print('Kill message received, interrupting main thread.')
            _thread.interrupt_main()
        else:
            print('Unknown message')

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        message = message + os.linesep
        serialized_message = bytes(str(message), encoding='utf-8')
        return serialized_message
    def deserialize(self, message: bytes) -> str:
        print(f'RAW message: {message}')
        deserialized = str(message, encoding='utf-8').strip()
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
    shebang=SHEBANG_STRING,
    server_port=SERVER_TEST_SERVER_PORT,
    framework_dir=FRAMEWORK_DIR)

CLIENT_TEST_SERVER_PORT = 11493

TEST_CLIENT = \
"""
$shebang

import os
import sys

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.pal.networking import ClientSocket, SocketMessageTransformer
SERVER_PORT = $server_port

class ExampleMessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        message = message + os.linesep
        serialized_message = bytes(str(message), encoding='utf-8')
        return serialized_message
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf-8').strip()

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
    shebang=SHEBANG_STRING,
    server_port=CLIENT_TEST_SERVER_PORT,
    framework_dir=FRAMEWORK_DIR)

BASE_PATH = f'{TEST_FILES_DIRECTORY}/socket'

def create_socket_test_data():

    # Create server
    if not os.path.isdir(BASE_PATH):
            os.mkdir(BASE_PATH)

    server_script = f'{BASE_PATH}/server.py'

    with open(server_script, 'w') as server_file:
        server_file.write(TEST_SERVER)

    # Create client
    if not os.path.isdir(BASE_PATH):
        os.mkdir(BASE_PATH)

    client_path = f'{BASE_PATH}/client.py'

    with open(client_path, 'w') as client_file:
        client_file.write(TEST_CLIENT)

    # Start the server
    #command = ['python', f'{server_script}']
    #try:
    #    subprocess.Popen(command)
    #except subprocess.CalledProcessError:
    #    assert False