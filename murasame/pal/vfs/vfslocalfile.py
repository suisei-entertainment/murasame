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
Contains the implementation of the VFSLocalFile class.
"""

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfsresourcedescriptor import VFSResourceDescriptor
from murasame.pal.vfs.vfsresourcetypes import VFSResourceTypes

class VFSLocalFile(VFSResourceDescriptor):

    """Represents the resource descriptor of a file in file system that is
    added as a VFS node.

    Attributes:
        _path (str): Path fo the file.

        _content (str): The content type of the file.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """Path to the file in the local file system.

        Authors:
            Attila Kovacs
        """

        return self._path

    @property
    def ContentType(self) -> str:

        """The MIME type of the file located at the indicated path.

        Authors:
            Attila Kovacs
        """

        return self._content

    @property
    def Type(self) -> 'VFSResourceTypes':

        """Returns the type of the VFS resource.

        Authors:
            Attila Kovacs
        """

        return VFSResourceTypes.LOCAL_FILE

    def __init__(self) -> None:

        """Creates a new VFSSystemFile instance.

        Authors:
            Attila Kovacs
        """

        super().__init__()

        self._path = None
        self._content = None

    def serialize(self) -> dict:

        """Function prototype for the serialization function of the descriptor.

        Returns:
            dict: The descriptor serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        result = {}
        result['type'] = 'localfile'
        result['path'] = self._path

        if self._content is not None:
            result['contenttype'] = self._content

        return result

    def deserialize(self, data: dict) -> None:

        """Function prototype for the deserialization function of the
        descriptor.

        Args:
            data (dict): The descriptor serialized as a dictionary.

        Raises:
            InvalidInputError: Raised if the data doesn't contain the data of a
                VFSResourceDescriptor.

            InvalidInputError: Raised if the descriptor cannot be parsed as a
                VFSLocalFile object.

        Authors:
            Attila Kovacs
        """

        try:

            if data['type'] != 'localfile':
                raise InvalidInputError(
                    f'The descriptor does not contain the data of a '
                    f'VFSResourceDescriptor object. Data: {data}')

            self._path = data['path']
        except KeyError as error:
            raise InvalidInputError(f'Failed to parse VFSLocalFile from input '
                                    f'data: {data}.') from error

        # Retrieve the content type
        try:
            self._content = data['contenttype']
        except KeyError:
            self._content = None

    def update_content_type(self, content_type: str) -> None:

        """Updates the content type.

        Args:
            content_type (str): The content type to set.

        Authors:
            Attila Kovacs
        """

        self._content = content_type

    def create_connector(self) -> 'VFSResourceConnector':

        """Function prototype for creating the resource connector for each type
        of VFS resource.

        Returns:
            VFSResourceConnector: An object that is derived from
                VFSResourceConnector.

        Authors:
            Attila Kovacs
        """

        # Needed to import VFSLocalFileConnector to avoid circular imports
        #pylint: disable=import-outside-toplevel

        from murasame.pal.vfs.vfslocalfileconnector import VFSLocalFileConnector
        return VFSLocalFileConnector()
