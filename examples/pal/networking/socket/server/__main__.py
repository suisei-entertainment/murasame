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
Contains the implementation of the server side of the socket example.
"""

# Runtime Imports
import _thread
from typing import Any

# Murasame Imports
import time

from murasame.pal.networking import (
    ServerSocket,
    ClientThread,
    SocketMessageTransformer)

SERVER_PORT = 11492

class EchoClientHandler(ClientThread):
    def handle_message(self, message: Any) -> None:
        if message == 'quit':
            self.send(message='Shutting down server...')
            print('Server shutdown requested.')
            _thread.interrupt_main()
            return
        print(f'Received message: {message}')
        self.send(message=message)

class MessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        return bytes(message, encoding='utf-8')
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf--8')

def main() -> int:

    server = ServerSocket(port = SERVER_PORT,
                          name='ServerSocketExample',
                          client_handler=EchoClientHandler,
                          transformer=MessageTransformer())
    print(f'Server listening on port {SERVER_PORT}.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    return  0

if __name__ == '__main__':
    main()