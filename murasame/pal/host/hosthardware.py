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
Contains the implementation of the HostHardware class.
"""

# Murasame Imports
from murasame.pal.host.hostcpu import HostCPU
from murasame.pal.host.hostmemory import HostMemory
from murasame.pal.host.hostnetworking import HostNetworking

class HostHardware:

    """Utility class that represents the hardware of the host system.

    Attributes:
        _cpu (HostCPU): The descriptor of the CPU of the host system.

        _memory (HostMemory): The descriptor of the host system's memory.

        _networking (HostNetworking): The descriptor of the available
            networking in the host system.

    Authors:
        Attila Kovacs
    """

    @property
    def CPU(self) -> HostCPU:

        """Provides access to the information of the host CPU.

        Authors:
            Attila Kovacs
        """

        return self._cpu

    @property
    def Memory(self) -> HostMemory:

        """Provides access to the information of the host memory.

        Authors:
            Attila Kovacs
        """

        return self._memory

    @property
    def Networking(self) -> HostNetworking:

        """Provides access to the information of the host's networkig
        capabilities.

        Authors:
            Attila Kovacs
        """

        return self._networking

    def __init__(
            self,
            geoip_database_path: str = '/data/geoip',
            auto_download_geoip_database: bool = False,
            geoip_license_key: str = None) -> None:

        """Creates a new HostHardware instance.

        Args:
            geoip_database_path (str): Path to the local GeoIP database.

            auto_download_geoip_database (bool): Whether or not the GeoIP
                database should be downloaded automatically.

            geoip_license_key (str): The license key to use when downloading
                the GeoIP database.

        Authors:
            Attila Kovacs
        """

        self._cpu = HostCPU()
        self._memory = HostMemory()
        self._networking = HostNetworking(
            geoip_database_path=geoip_database_path,
            auto_download_geoip_database=auto_download_geoip_database,
            geoip_license_key=geoip_license_key)
