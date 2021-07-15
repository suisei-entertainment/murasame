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
Contains the implementation of the HostDistribution class.
"""

# Murasame Imports
from murasame.exceptions import MissingRequirementError

class HostDistribution:

    """Utility class that provides additional details on the host OS
    distribution on Unix systems.

    This class requires the distro package to be installed on the host system.

    Attributes:
        _id (str): ID of the host operating system.

        _name (str): Name of the host operating system.

        _fullname (str): Full name of the host operating system.

        _major (int): Major product version of the host operating system.

        _minor (int): Minor product version of the host operating system.

        _build (int): Build number of the host operating system.

        _versionstring (str): The string representation of the operating system
            version.

        _codename (str): The codename of the operating system's version.

        _like (str): Family description of the operating system, e.g. 'Debian'
            for Ubuntu.

    Authors:
            Attila Kovacs
    """

    @property
    def ID(self) -> str:

        """Returns the distro ID of the host operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._id

    @property
    def Name(self) -> str:

        """Returns the short name of the host operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def FullName(self) -> str:

        """Returns the full name of the host operating system's distribution,
        including the version number and release codename.

        Authors:
            Attila Kovacs
        """

        return self._fullname

    @property
    def MajorVersion(self) -> int:

        """Returns the major version of the operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._major

    @property
    def MinorVersion(self) -> int:

        """Returns the minor version of the operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._minor

    @property
    def BuildNumber(self) -> int:

        """Returns the build number of the operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._build

    @property
    def VersionString(self) -> str:

        """Returns the version string of the operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._versionstring

    @property
    def Codename(self) -> str:

        """Returns the release codename of the operating system's distribution.

        Authors:
            Attila Kovacs
        """

        return self._codename

    @property
    def Like(self) -> str:

        """Returns a space separated distribution list that are similar to
        this one.

        Authors:
            Attila Kovacs
        """

        return self._like

    def __init__(self) -> None:

        """Creates a new HostDistribution instance.

        Authors:
            Attila Kovacs
        """

        try:
            # Imported here so detection works even without the package
            # installed.
            #pylint: disable=import-outside-toplevel
            import distro
            self._id = distro.id()
            self._name = distro.name(pretty=False)
            self._fullname = distro.name(pretty=True)

            try:
                self._major = int(distro.major_version())
            except ValueError:
                self._major = -1

            try:
                self._minor = int(distro.minor_version())
            except ValueError:
                self._minor = -1

            try:
                self._build = int(distro.build_number())
            except ValueError:
                self._build = -1

            self._versionstring = distro.version(pretty=False)
            self._codename = distro.codename()
            self._like = distro.like()
        except ImportError as exception:
            raise MissingRequirementError(
                'HostDistribution requires the distro package.',
                requirement='distro') from exception
