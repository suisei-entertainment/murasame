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
Contains the implementation of the VFSResourceDescriptor class.
"""

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.log import LogWriter

class VFSResourceDescriptor(LogWriter):

    """Base class for for the descriptors of VFS resource types.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new VFSResourceDescriptor instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                         cache_entries=True)

    def serialize(self) -> dict:

        """Function prototype for the serialization function of the descriptor.

        Needs to be implemented in every derived class.

        Returns:
            dict: The descriptor serialized as a dictionary.

        Raises:
            NotImplementedError: Raised when the function is not implemented in
                the derived class.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.serialize() has to be implemented.')

    def deserialize(self, data: dict) -> bool:

        """Function prototype for the deserialization function of the descriptor.

        Needs to be implemented in every derived class.

        Args:
            data (dict): The descriptor serialized as a dictionary.

        Raises:
            NotImplementedError: Raised when the function is not implemented in
                the derived class.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.deserialize() has to be implemented.')

    def update_content_type(self, content_type: str) -> None:

        """Updates the content type.

        Args:
            content_type (str): The content type to set.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.update_content_type() has to be '
            f'implemented.')

    def create_connector(self) -> 'VFSResourceConnector':

        """Function prototype for creating the resource connector for each type
            of VFS resource.

        Returns:
            VFSResourceConnector: An object that is derived from
                VFSResourceConnector.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.create_connector() has to be '
            f'implemented.')
