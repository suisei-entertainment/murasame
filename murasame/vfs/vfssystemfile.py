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
Contains the implementation of the VFSSystemFile class.
"""

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.vfs.vfsresourcedescriptor import VFSResourceDescriptor

class VFSLocalFile(VFSResourceDescriptor):

    """
    Represents the resource descriptor of a file in file system that is
    added as a VFS node.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """
        Path to the file in the local file system.

        Authors:
            Attila Kovacs
        """

        return self._path

    def __init__(self):

        """
        Creates a new VFSSystemFile instance.
        """

        self._path = None
        """
        Path fo the file.
        """

    def serialize(self) -> dict:

        """
        Function prototype for the serialization function of the descriptor.

        Returns:
            The descriptor serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        result = {}
        result['type'] = 'localfile'
        result['path'] = self._path
        return result

    def deserialize(self, data: dict) -> bool:

        """
        Function prototype for the deserialization function of the descriptor.

        Args:
            data:       The descriptor serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        try:
            self._path = data['path']
        except KeyError as error:
            raise InvalidInputError(f'Failed to parse VFSLocalFile from input '
                                    f'data: {data}.') from error
