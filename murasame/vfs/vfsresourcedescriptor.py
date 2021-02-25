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

class VFSResourceDescriptor:

    """
    Base class for for the descriptors of VFS resource types.

    Authors:
        Attila Kovacs
    """

    def serialize(self) -> dict:

        """
        Function prototype for the serialization function of the descriptor.
        Needs to be implemented in every derived class.

        Returns:
            The descriptor serialized as a dictionary.

        Raises:
            NotImplementedError:        Raised when the function is not
                                        implemented in the derived class.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.serialize() has to be implemented.')

    def deserialize(self, data: dict) -> bool:

        """
        Function prototype for the deserialization function of the descriptor.
        Needs to be implemented in every derived class.

        Args:
            data:       The descriptor serialized as a dictionary.

        Raises:
            NotImplementedError:        Raised when the function is not
                                        implemented in the derived class.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'{self.__class__.__name__}.deserialize() has to be implemented.')
