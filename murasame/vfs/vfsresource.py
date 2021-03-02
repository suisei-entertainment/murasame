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
from murasame.logging import LogWriter

class VFSResource(LogWriter):

    """
    Represents a single entity associated with a VFS node. Typically this is
    one version of the file that is associated with the VFS node.

    Authors:
        Attila Kovacs
    """

    @property
    def Version(self) -> 'ResourceVersion':

        """
        Provides access to the version of the VFS resource.

        Authors:
            Attila Kovacs
        """

        return self._version

    @property
    def Resource(self) -> object:

        """
        Provides access to the actual resource.

        Authors:
            Attila Kovacs
        """

        return self._resource

    @property
    def Descriptor(self) -> object:

        """
        The descriptor of the underlying resource.

        Authors:
            Attila Kovacs
        """

        return self._descriptor

    @property
    def Type(self) -> 'VFSResourceTypes':

        """
        The type of the underlying resource.

        Authors:
            Attila Kovacs
        """

        return self._type

    def __init__(
        self,
        resource_type: 'VFSResourceTypes' = None,
        descriptor: 'VFSResourceDescriptor' = None,
        version: 'ResourceVersion' = None,
        data: dict = None) -> None:

        """
        Creates a new VFSResource instance.

        Args:
            resource_type:  The type of the resource.
            descriptor:     The resource descriptor of the resource.
            version:        The version of the resource.
            data:           Optional data to be deserialized.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.vfs', cache_entries=True)

        self._version = version
        """
        The version of the content.
        """

        self._descriptor = descriptor
        """
        The resource descriptor of the underlying resource.
        """

        self._resource = None
        """
        The actual resource embedded in this VFS resource.
        """

        self._type = resource_type
        """
        The type of the underlying resource.
        """

        if data is not None:
            self.deserialize(data=data)

    def serialize(self) -> dict:

        """
        Serializes the contents of the resource into a dictionary.

        Returns:
            The resource serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        result = {}
        return result

    def deserialize(self, data: dict) -> None:

        """
        Deserializes the resource from a dictionary.

        Args:
            data:       The resources serialized as a dictionary.

        Authors:
            Attila Kovacs
        """

        return
