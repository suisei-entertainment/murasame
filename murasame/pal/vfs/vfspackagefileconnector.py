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
Contains the implementation of the VFSPackageFileConnector class.
"""

# Runtime Imports
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfsresourceconnector import VFSResourceConnector
from murasame.pal.vfs.vfspackagefile import VFSPackageFile

class VFSPackageFileConnector(VFSResourceConnector):

    """Resource connector implementation for files in a resource package.

    Authors:
        Attila Kovacs
    """

    def load(self, descriptor: 'VFSResourceDescriptor') -> Any:

        """Loads the content of the VFS resource into memory.

        Args:
            descriptor (VFSResourceDescriptor): The resource descriptor of the
                resource to load.

        Raises:
            InvalidInputError: Raised when the provided descriptor is not
                a VFSPackageFile.

        Returns:
            Any: The loaded resource data.

        Authors:
            Attila Kovacs
        """

        # This connector can only load resources with type VFSLocalFile
        if not descriptor or not isinstance(descriptor, VFSPackageFile):
            raise InvalidInputError('Invalid descriptor type provided.')
