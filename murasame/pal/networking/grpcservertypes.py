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
Contains the implementation of the GRPCServerTypes class.
"""

# Runtime Imports
from enum import IntEnum, auto

class GRPCServerTypes(IntEnum):

    """Contains the list of supported gRPC server types.

    Attributes:
        UNKNOWN: Unknown server type.

        INSECURE: Represents an insecure server, using non-encrypted
            communication.

        SECURE: Represents a secure server using encrypted communication.

    Authors:
        Attila Kovacs
    """

    UNKNOWN = auto()
    INSECURE = auto()
    SECURE = auto()