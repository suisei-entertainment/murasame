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
Contains the implementation of the HostDescriptor class.
"""

# Murasame Imports
from murasame.pal.host.hosthardware import HostHardware
from murasame.pal.host.hostos import HostOS
from murasame.pal.host.hostpython import HostPython
from murasame.pal.host.hostuser import HostUser

class HostDescriptor:

    """Utility class that inspects the host system upon creation and stores
    basic system information about it.

    Attributes:
        _hardware (HostHardware): The descriptor object for the host hardware.

        _os = (HostOS): The descriptor object for the host operating system.

        _python = (HostPython): The descriptor object of the Python runtime.

        _user = (HostUser): The descriptor object for the user account used to
            execute the application.

    Authors:
        Attila Kovacs
    """

    @property
    def Hardware(self) -> str:

        """Provides access to the information of the host hardware.

        Authors:
            Attila Kovacs
        """

        return self._hardware

    @property
    def OS(self) -> str:

        """Provides access to the information of the host operating system.

        Authors:
            Attila Kovacs
        """

        return self._os

    @property
    def Python(self) -> HostPython:

        """Provides access to the information of the host Python environment.

        Authors:
            Attila Kovacs
        """

        return self._python

    @property
    def User(self) -> HostUser:

        """Provides access to the information of the host user account.

        Authors:
            Attila Kovacs
        """

        return self._user

    def __init__(
            self,
            geoip_database_path: str = '/shared/geoip',
            auto_download_geoip_database: bool = False,
            geoip_license_key: str = None) -> None:

        """Creates a new HostDescriptor instance.

        Args:
            geoip_database_path (str): Path to the directory where the GeoIP
                database is located.

            auto_download_geoip_database (bool): Whether or not the GeoIP
                database should be downloaded automatically.

            geoip_license_key (str): The license key to use when downloading
                the GeoIP database.

        Authors:
            Attila Kovacs
        """

        self._hardware = HostHardware(
            geoip_database_path=geoip_database_path,
            auto_download_geoip_database=auto_download_geoip_database,
            geoip_license_key=geoip_license_key)
        self._os = HostOS()
        self._python = HostPython()
        self._user = HostUser()
