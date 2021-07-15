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
Contains the implementation of the HostSystem class.
"""

# Murasame Imports
from murasame.pal.host.hostdescriptor import HostDescriptor

class HostSystem:

    """Common implementation for host systems.

    Attributes:
        _host_descriptor (HostDescriptor): The host descriptor instance.

    Authors:
        Attila Kovacs
    """

    @property
    def HostDescriptor(self) -> 'HostDescriptor':

        """Provides access to the host descriptor.

        Authors:
            Attila Kovacs
        """

        return self._host_descriptor

    def __init__(self) -> None:

        """Creates a new HostSystem instance.

        Authors:
            Attila Kovacs
        """

        self._host_descriptor = None

    def initialize(self, geoip_database_path: str = '/data/geoip') -> None:

        """Initializes the host service.

        Args:
            geoip_database_path (str): Path to the local GeoIP database.

        Authors:
            Attila Kovacs
        """

        self._host_descriptor = HostDescriptor(
            geoip_database_path=geoip_database_path)
