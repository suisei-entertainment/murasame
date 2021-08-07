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
Contains the implementation of the client side of the socket example.
"""

# Runtime Imports

# Murasame Imports
from murasame.pal.networking import ClientSocket, SocketMessageTransformer

SERVER_PORT = 11492

class MessageTransformer(SocketMessageTransformer):
    def serialize(self, message: str) -> bytes:
        return bytes(message, encoding='utf-8')
    def deserialize(self, message: bytes) -> str:
        return str(message, encoding='utf--8')

def main() -> int:

    client = ClientSocket(name='EchoSocket',
                          host='localhost',
                          port=SERVER_PORT,
                          transformer=MessageTransformer())
    client.connect()

    running = True
    while running:
        message = input('MESSAGE> ')
        client.send(message=message)
        print(client.receive())
        if message=='quit':
            running=False

    client.disconnect()
    del client

    return  0

if __name__ == '__main__':
    main()