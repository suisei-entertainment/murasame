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
Contains the implementation of the ResourceVersion class.
"""

# Runtime Imports
import sys

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log import LogWriter

class ResourceVersion(LogWriter):

    """Represents the resource version of a single VFS resource object.

    Attributes:
        LATEST (int): Constant representing the latest resource version.

        _version (int): The actual version number associated with the resource.

    Authors:
        Attila Kovacs
    """

    LATEST = sys.maxsize

    @property
    def Version(self) -> int:

        """Provides access to the version number.

        Authors:
            Attila Kovacs
        """

        return self._version

    def __init__(self, version: int) -> None:

        """Creates a new ResourceVersion instance.

        Args:
            version (int): The version number.

        Raises:
            InvalidInputError: Raised when trying to create an object with an
                invalid version number.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                         cache_entries=True)

        if version < 1:
            raise InvalidInputError('Resource version must be greater than 0.')

        self._version = version

    def __eq__(self, other: 'ResourceVersion') -> bool:

        """Equality operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if the two resource versions are equal, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return self.is_equal(other)

    def __ne__(self, other: 'ResourceVersion') -> bool:

        """Inequality operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if the two resource versions are not equal, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return not self.is_equal(other)

    def __lt__(self, other: 'ResourceVersion') -> bool:

        """Less-than operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if this resource version is older than the other one,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return self.is_older(other)

    def __le__(self, other: 'ResourceVersion') -> bool:

        """Less-than or equal operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if this resource version is the same or older than the
                other one, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return self.is_older(other) or self.is_equal(other)

    def __gt__(self, other: 'ResourceVersion') -> bool:

        """Greater-than operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if this resource version is newer than the other one,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return self.is_newer(other)

    def __ge__(self, other: 'ResourceVersion') -> bool:

        """Greater-than or equal operator.

        Args:
            other (ResourceVersion): The resource version instance to compare
                with.

        Returns:
            bool: 'True' if this resource version is the same or newer than the
                other one, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ResourceVersion):
            return NotImplemented

        return self.is_newer(other) or self.is_equal(other)

    def __repr__(self) -> str:

        """Unambiguity operator.

        Authors:
            Attila Kovacs
        """

        return f'ResourceVersion({self.Version})'

    def __str__(self) -> str:

        """Returns the string representation of this resource version.

        Authors:
            Attila Kovacs
        """

        return f'{self.Version}'

    def is_equal(self, other: 'ResourceVersion') -> bool:

        """Returns whether or not this resource version equals to the given one.

        Args:
            other (ResourceVersion): The other resource version to compare with.

        Returns:
            bool: 'True' if the two resource versions are equal, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if self.Version == other.Version:
            return True

        return False

    def is_newer(self, other: 'ResourceVersion') -> bool:

        """Returns whether or not this resource is newer than an other one.

        Args:
            other (ResourceVersion): The other resource version to compare with.

        Returns:
            bool: 'True' if this resource versions is newer, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if self.Version > other.Version:
            return True

        return False

    def is_older(self, other: 'ResourceVersion') -> bool:

        """Returns whether or not this resource is older than an other one.

        Args:
            other (ResourceVersion): The other resource version to compare with.

        Returns:
            bool: 'True' if the this resource versions is older, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        if self.Version < other.Version:
            return True

        return False

    def bump_version(self) -> None:

        """Increases the version number.

        Authors:
            Attila Kovacs
        """

        self._version = self._version + 1
