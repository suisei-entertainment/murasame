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
Contains the implementation of the HostPython class.
"""

# Runtime Imports
import sys

class HostPython:

    """Utility class that represents the Python environment on the host system.

    Attributes:
        _major (int): The major Python version on the host system.

        _minor (int): The minor Python version on the host system.

        _patch (int): The patch level of the Python version on the host system.

        _location (str): Location of the Python interpreter on the host system.

    Authors:
        Attila Kovacs
    """

    @property
    def MajorVersion(self) -> int:

        """The major version of Python on the host system.

        Authors:
            Attila Kovacs
        """

        return self._major

    @property
    def MinorVersion(self) -> int:

        """The minor version of Python on the host system.

        Authors:
            Attila Kovacs
        """

        return self._minor

    @property
    def PatchLevel(self) -> int:

        """The patch level of Python on the host system.

        Authors:
            Attila Kovacs
        """

        return self._patch

    @property
    def PythonVersion(self) -> str:

        """The full version of Python on the host system as a string.

        Authors:
            Attila Kovacs
        """

        return '{}.{}.{}'.format(self._major, self._minor, self._patch)

    @property
    def Location(self) -> str:

        """The location of the Python executable on the host system.

        Authors:
            Attila Kovacs
        """

        return self._location

    def __init__(self) -> None:

        """Creates a new HostPython instance.

        Authors:
            Attila Kovacs
        """

        self._major = -1
        self._minor = -1
        self._patch = -1
        self._location = ''

        self._detect_version()
        self._detect_location()

    @staticmethod
    def is_virtual_env() -> bool:

        """Returns whether or not the application was started inside virtualenv.

        Returns:
            bool: 'True' if the application is running inside virtualenv, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if (hasattr(sys, 'real_prefix')) \
           or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return True

        return False

    def _detect_version(self) -> None:

        """Detection logic for the Python version.

        Authors:
            Attila Kovacs
        """

        self._major = sys.version_info.major
        self._minor = sys.version_info.minor
        self._patch = sys.version_info.micro

    def _detect_location(self) -> None:

        """Detects the location of the Python executable on the host system.

        Authors:
            Attila Kovacs
        """

        self._location = sys.executable
