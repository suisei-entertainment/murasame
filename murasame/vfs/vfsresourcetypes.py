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
Contains the implementation of the VFSResourceTypes class.
"""

# Runtime Imports
from enum import IntEnum

class VFSResourceTypes(IntEnum):

    """
    List of supported VFS resource types.

    Authors:
        Attila Kovacs
    """

    UNKNOWN = 0 # Unknown resource type
    LOCAL_FILE = 1 # File in the local file system
    PACKAGE_FILE = 2 # File in a resource package
