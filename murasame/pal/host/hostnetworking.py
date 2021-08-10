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
Contains the implementation of the HostNetworking class.
"""

# Runtime Imports
import requests

# SEED Imports
from murasame.constants import MURASAME_PAL_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log import LogWriter
from murasame.pal.host.physicalinterface import PhysicalInterface
from murasame.pal.host.hostlocation import HostLocation

class HostNetworking(LogWriter):

    """Utility class that represents the networking capabilities of the host
    system.

    Attributes:
        _physical_interfaces (dict): List of physical network interfaces in the
            host system.

        _public_ip (str): The public IP address of the host system.

        _host_location (HostLocation): The location descriptor of the public IP
            address.

        _geoip_database_path (str): Path to the GeoIP database to use.

    Authors:
        Attila Kovacs
    """

    @property
    def PhysicalInterfaces(self) -> dict:

        """Provides access to the identified physical network interfaces of the
        host system.

        Authors:
            Attila Kovacs
        """

        return self._physical_interfaces

    @property
    def PublicIP(self) -> str:

        """Provides access to the public IP address of the machine.

        Authors:
            Attila Kovacs
        """

        return self._public_ip

    @property
    def HostLocation(self) -> 'HostLocation':

        """Provides access to the host location descriptor.

        Authors:
            Attila Kovacs
        """

        return self._host_location

    def __init__(
            self,
            geoip_database_path: str = '/data/geoip',
            auto_download_geoip_database: bool = False,
            geoip_license_key: str = None) -> None:

        """Creates a new HostNetworking instance.

        Args:
            geoip_database_path (str): Path to the GeoIP database.

            auto_download_geoip_database (bool): Whether or not the GeoIP
                database should be downloaded automatically.

            geoip_license_key (str): The license key to use when downloading
                the GeoIP database.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_PAL_LOG_CHANNEL,
                         cache_entries=True)

        self._physical_interfaces = {}
        self._public_ip = None
        self._host_location = None
        self._geoip_database_path = geoip_database_path

        self._detect_networking(self._get_interfaces())
        self._detect_public_ip(
            auto_download_geoip_database=auto_download_geoip_database,
            geoip_license_key=geoip_license_key)

    def has_network_interface(self, interface_name: str) -> bool:

        """Returns whether or not the given network interface exists.

        Args:
            interface_name (str): Name of the network interface to check.

        Returns:
            bool: 'True' if the interface exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if interface_name in self._physical_interfaces:
            return True

        return False

    def _has_netifaces(self) -> bool:

        """Checks whether or not the netifaces package is available on the host
        system.

        Returns:
            bool: 'True' if the package is available, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        # Disable pylint warnings as this is intentional here to allow
        # checking for package availability
        #pylint: disable=unused-import
        #pylint: disable=import-outside-toplevel

        try:
            import netifaces
        except ImportError:
            self.warning('The netifaces package is not available on '
                         'the host system. Network interfaces cannot be '
                         'retrieved.')
            return False

        return True

    def _get_interfaces(self) -> list:

        """Collects the network interfaces on the host system using netifaces.

        Returns:
            list: A list of all interfaces found by netifaces.

        Authors:
            Attila Kovacs
        """

        interfaces = []

        if self._has_netifaces():
            self.debug('Attempting to retrieve network interfaces by using '
                       'netifaces...')
            # Imported here so detection works even without the package
            # installed.
            #pylint: disable=import-outside-toplevel
            import netifaces
            interfaces = netifaces.interfaces()
            self.debug('Network interfaces retrieved successfully.')

        return interfaces

    def _add_physical_interface(self, nwif: str) -> PhysicalInterface:

        """Create the physical interface if it doesn't exist already.

        Args:
            nwif (str): The name of the network interface.

        Returns:
            PhysicalInterface: The new physical interface object.

        Authors:
            Attila Kovacs
        """

        if not self.has_network_interface(nwif):
            self._create_network_interface(nwif)

        return self._physical_interfaces[nwif]

    def _add_link_addresses(self,
                            physical_interface: PhysicalInterface,
                            addresses: list) -> None:

        """Adds all link layer addresses to a physical interface.

        Args:
            physical_interface (PhysicalInterface): The PhysicalInterface
                instance to add to.

            addresses (list): List of addresses returned by netifaces.

        Authors:
            Attila Kovacs
        """

        if self._has_netifaces():
            try:
                self.debug(f'Adding link layer addresses to interface '
                           f'{physical_interface.Name}')
                # Imported here so detection works even without the package
                # installed.
                #pylint: disable=import-outside-toplevel
                import netifaces
                for address in addresses[netifaces.AF_LINK]:
                    physical_interface.add_link_address(address['addr'])
            except KeyError:
                self.debug(f'No link layer addresses found for interface '
                           f'{physical_interface.Name}')

    def _add_ipv4_addresses(self,
                            physical_interface: PhysicalInterface,
                            addresses: list) -> None:

        """Adds all IPv4 addresses to a physical interface.

        Args:
            physical_interface (PhysicalInterface): The PhysicalInterface
                instance to add to.

            addresses (list): List of addresses returned by netifaces.

        Authors:
            Attila Kovacs
        """

        if self._has_netifaces():
            try:
                self.debug(f'Adding IPv4 addresses to interface '
                           f'{physical_interface.Name}')
                # Imported here so detection works even without the package
                # installed.
                #pylint: disable=import-outside-toplevel
                import netifaces
                for address in addresses[netifaces.AF_INET]:

                    # Identify localhost
                    is_locahost = False
                    if address['addr'].startswith('127.0.0.'):
                        is_locahost = True

                    # Identify link local address, according to RFC 3927
                    is_link_local = False
                    if address['addr'].startswith('169.254'):
                        is_link_local = True

                    physical_interface.add_ipv4_address(
                        address=address['addr'],
                        netmask=address['netmask'],
                        broadcast_address=address['broadcast'],
                        is_localhost=is_locahost,
                        is_link_local_address=is_link_local)
            except KeyError:
                self.debug(f'No IPv4 addresses found for interface '
                           f'{physical_interface.Name}')

    def _add_ipv6_addresses(self,
                            physical_interface: PhysicalInterface,
                            addresses: list) -> None:

        """Adds all IPv6 addresses to a physical interface.

        Args:
            physical_interface (PhysicalInterface): The PhysicalInterface
                instance to add to.

            addresses (list): List of addresses returned by netifaces.

        Authors:
            Attila Kovacs
        """

        if self._has_netifaces():
            try:
                self.debug(f'Adding IPv6 addresses to interface '
                           f'{physical_interface.Name}')
                # Imported here so detection works even without the package
                # installed.
                #pylint: disable=import-outside-toplevel
                import netifaces
                for address in addresses[netifaces.AF_INET6]:

                    # Identify localhost
                    is_locahost = False
                    if address['addr'] == '::1':
                        is_locahost = True

                    # Identify link local address, according to RFC 3927
                    is_link_local = False
                    if address['addr'].startswith('fe80'):
                        is_link_local = True

                    physical_interface.add_ipv6_address(
                        address=address['addr'],
                        netmask=address['netmask'],
                        broadcast_address=address['broadcast'],
                        is_localhost=is_locahost,
                        is_link_local_address=is_link_local)
            except KeyError:
                self.debug(f'No IPv6 addresses found for interface '
                           f'{physical_interface.Name}')

    def _detect_networking(self, interfaces: list) -> None:

        """Processes all network interfaces returned by netifaces.

        Args:
            interfaces (list): List of network interfaces returned by
                netifaces.

        Authors:
            Attila Kovacs
        """

        for nwif in interfaces:

            # Create the physical interface if it doesn't exist already
            physical_interface = self._add_physical_interface(nwif)

            # Collect all addresses on the interface
            addresses = []
            if self._has_netifaces():
                # Imported here so detection works even without the package
                # installed.
                #pylint: disable=import-outside-toplevel
                import netifaces
                addresses = netifaces.ifaddresses(nwif)

            # Link layer addresses
            self._add_link_addresses(physical_interface, addresses)

            # IPv4 addresses
            self._add_ipv4_addresses(physical_interface, addresses)

            # IPv6 addresses
            self._add_ipv6_addresses(physical_interface, addresses)

    def _create_network_interface(self, interface_name: str) -> None:

        """Creates a new physical network interface.

        Args:
            interface_name (str): Name of the physical interface to create.

        Authors:
            Attila Kovacs
        """

        if self.has_network_interface(interface_name):
            self.warning(f'Physical interface {interface_name} already '
                         f'exists, won\'t be created again.')
            return

        self._physical_interfaces[interface_name] = \
            PhysicalInterface(interface_name)

        self.debug(f'New physical network interface ({interface_name}) has '
                   f'been created.')

    def _detect_public_ip(
        self,
        auto_download_geoip_database: bool = False,
        geoip_license_key: str = None) -> None:

        """Detects the public IP of the host by calling the ipify API.

        Args:
            auto_download_geoip_database (bool): Whether or not the GeoIP
                database should be downloaded automatically.

            geoip_license_key (str): The license key to use when downloading
                the GeoIP database.

        Authors:
            Attila Kovacs
        """

        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            response.raise_for_status()
            ip_address = response.text
        except requests.exceptions.ConnectionError:
            self.warning('Failed to connect to the public IP detection '
                         'service.')
            self._public_ip = 'UNKNOWN'
            return
        except requests.exceptions.Timeout:
            self.warning('Failed to detect public IP. Request timeout.')
            self._public_ip = 'UNKNOWN'
            return
        except requests.exceptions.HTTPError as error:
            self.warning(f'Failed to detect public IP. Received HTTP '
                         f'error: {error.response.status_code}')
            self._public_ip = 'UNKNOWN'
            return

        self._public_ip = ip_address
        self.debug(f'Public IP is detected as {self._public_ip}.')

        if auto_download_geoip_database and not geoip_license_key:
            raise InvalidInputError(
                'Automatic download of GeoIP database has been requested, '
                'but no license key was provided.')

        try:
            self._host_location = HostLocation(
                public_ip=self._public_ip,
                database_path=self._geoip_database_path,
                geoip_license_key=geoip_license_key)
        except InvalidInputError:
            self.debug('Failed to detect host location. GeoIP databasae is '
                       'not available.')
