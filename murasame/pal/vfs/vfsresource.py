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
Contains the implementation of the VFSResource class.
"""

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log import LogWriter
from murasame.pal.vfs.resourceversion import ResourceVersion

class VFSResource(LogWriter):

    """Represents a single entity associated with a VFS node.

    Typically this is one version of the file that is associated with the VFS
    node.

    Attributes:
        _version (ResourceVersion): The version of the content.

        _descriptor (VFSResourceDescriptor): The resource descriptor of the
            underlying resource.

        _resource_connector (VFSResourceConnector): The resource connector that
            is to be used when accessing the resource.

        _resource (Any): The actual resource embedded in this VFS resource.

    Authors:
        Attila Kovacs
    """

    @property
    def Version(self) -> 'ResourceVersion':

        """Provides access to the version of the VFS resource.

        Authors:
            Attila Kovacs
        """

        return self._version

    @property
    def Resource(self) -> object:

        """Provides access to the actual resource.

        Raises:
            RuntimeError: Raised when trying to access the resource without
                specifying a resource loader.

        Authors:
            Attila Kovacs
        """

        if not self._resource:

            if not self._resource_connector:
                raise RuntimeError('No resource connector is specified when '
                                   'trying to access a VFS resource.')

            self._resource=self._resource_connector.load(
                descriptor=self._descriptor)

        return self._resource

    @property
    def Descriptor(self) -> 'VFSResourceDescriptor':

        """The descriptor of the underlying resource.

        Authors:
            Attila Kovacs
        """

        return self._descriptor

    @property
    def Type(self) -> 'VFSResourceTypes':

        """The type of the underlying resource.

        Authors:
            Attila Kovacs
        """

        return self._descriptor.Type

    def __init__(
        self,
        descriptor: 'VFSResourceDescriptor',
        version: 'ResourceVersion' = None,
        data: dict = None) -> None:

        """Creates a new VFSResource instance.

        Args:
            descriptor (VFSResourceDescriptor): The resource descriptor of the
                resource.

            version (ResourceVersion): The version of the resource.

            data (dict): The serialized form of the resource.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                         cache_entries=True)

        self._version = version
        self._descriptor = descriptor
        self._resource_connector = None
        self._resource = None

        if data is not None:
            self.deserialize(data=data)

        if descriptor is not None:
            self._resource_connector = descriptor.create_connector()

    def serialize(self) -> dict:

        """Serializes the contents of the resource into a dictionary.

        Returns:
            dict: The resource serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        result = {}
        result['version'] = self._version.Version
        result['descriptor'] = self._descriptor.serialize()
        return result

    def deserialize(self, data: dict) -> None:

        """Deserializes the resource from a dictionary.

        Args:
            data (dict): The resources serialized as a dictionary.

        Raises:
            InvalidInputError: Raised when the VFS resource descriptor is not
                serialized as a dictionary.

            InvalidInputError: Raised when the resource version is not found in
                the serialized data.

            InvalidInputError: Raised when the resource descriptor is not found
                in the serialized data.

        Authors:
            Attila Kovacs
        """

        # Retrieve version
        try:
            version = data['version']
            self._version = ResourceVersion(version=int(version))
        except KeyError as error:
            self.error('No resource version specified in the serialized data.')
            raise InvalidInputError('No resource version specified in the '
                                    'serialized data.') from error

        # Retrieve descriptor
        try:
            descriptor = data['descriptor']

            if not isinstance(descriptor, dict):
                self.error('The descriptor in the serialized VFS resource '
                           'data must be a dictionary.')
                raise InvalidInputError(
                    'Invalid type encountered, when trying to deserialize '
                    'VFS resource.')

            self._descriptor.deserialize(descriptor)

        except KeyError as error:
            self.error('No descriptor found when trying to deserialize a VFS '
                       'resource.')
            raise InvalidInputError('No descriptor found when trying to '
                                    'deserialize a VFS resource') from error
