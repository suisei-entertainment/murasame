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
Contains the implementation of the HostOS class.
"""

# Platform Imports
import platform

# Murasame Imports
from murasame.exceptions import MissingRequirementError
from murasame.logging import LogWriter

from murasame.pal.host.hostdistribution import HostDistribution

class HostOS(LogWriter):

    """
    Utility class that represents the host operating system.

    Authors:
        Attila Kovacs
    """

    @property
    def Platform(self) -> str:

        """
        Name of the host platform.

        Authors:
            Attila Kovacs
        """

        return self._platform

    @property
    def Name(self) -> str:

        """
        Name of the host operating system.

        Authors:
            Attila Kovacs
        """

        return self._os

    @property
    def Release(self) -> str:

        """
        The release name of the host operating system.

        Authors:
            Attila Kovacs
        """

        return self._os_release

    @property
    def Version(self) -> str:

        """
        The version of the host operating system.

        Authors:
            Attila Kovacs
        """

        return self._os_version

    @property
    def Distribution(self) -> HostDistribution:

        """
        Provides access to the detailed distribution information on Linux
        systems.

        Authors:
            Attila Kovacs
        """

        return self._distro

    def __init__(self) -> None:

        """
        Creates a new HostOS instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.pal', cache_entries=True)

        self._platform = ''
        """
        Name of the host platform.
        """

        self._os = ''
        """
        Name of the host operating system.
        """

        self._os_release = ''
        """
        The release name of the host operating system.
        """

        self._os_version = ''
        """
        The version of the host operating system.
        """

        self._distro = None
        """
        Contains detailed information on the host Linux distribution.
        """

        self._detect_os()

    def _detect_os(self) -> None:

        """
        Executes the OS detection logic.

        Authors:
            Attila Kovacs
        """

        self.debug('Detecting host operating system...')

        self._platform = platform.platform()
        self.debug(f'Host platform is identified as {self._platform}.')

        self._os = platform.system()
        self.debug(f'Host operating system is identified as {self._os}.')

        self._os_release = platform.release()
        self.debug(f'Host operating system release is identified as '
                   f'{self._os_release}.')

        self._os_version = platform.version()
        self.debug(f'Host operating system version is identified as '
                   f'{self._os_version}.')

        # Gather additional information on Linux by using the distro package
        if self._os.lower() == 'linux':
            try:
                self._distro = HostDistribution()
            except MissingRequirementError:
                self.warning(
                    'The distro package is not installed on the host system, '
                    'not all operating system information can be retrieved.')
