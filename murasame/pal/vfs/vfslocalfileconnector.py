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
Contains the implementation of the VFSLocalFileConnector class.
"""

# Runtime Imports
from typing import Any

# Murasame Imports
from murasame.pal.vfs.vfsresourceconnector import VFSResourceConnector

class VFSLocalFileConnector(VFSResourceConnector):

    """
    Resource connector implementation for files in the local file system.

    Authors:
        Attila Kovacs
    """

    def load(self, descriptor: 'VFSResourceDescriptor') -> Any:

        """
        Loads the content of the VFS resource into memory.

        Args:
            descriptor:     The resource descriptor of the resource to load.

        Returns:
            The loaded resource data.

        Authors:
            Attila Kovacs
        """
