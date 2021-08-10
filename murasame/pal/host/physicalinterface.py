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
Contains the implementation of the PhysicalInterface class.
"""

# Murasame Imports
from murasame.constants import MURASAME_PAL_LOG_CHANNEL
from murasame.log import LogWriter
from murasame.pal.host.linkaddress import LinkAddress
from murasame.pal.host.ipv4address import IPv4Address
from murasame.pal.host.ipv6address import IPv6Address

class PhysicalInterface(LogWriter):

    """Represents a single physical network interface.

    Attributes:
        _name (str): Name of the physical interface.

        _link_addresses (dict): The list of link layer addresses associated
            with the interface.

        _ipv4_addresses (dict): The list of IPv4 addresses associated with the
            interface.

        _ipv6_addresses (dict): The list of IPv6 addresses associated with the
            interface.

    Authors:
        Attila Kovacs
    """

    @property
    def Name(self) -> str:

        """Returns the name of the physical interface.

        Authors:
            Attila Kovacs
        """

        return self._name

    def __init__(self, interface_name: str) -> str:

        """Creates a new PhysicalInterface instance.

        Args:
            interface_name (str): Name of the physical interface.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_PAL_LOG_CHANNEL,
                         cache_entries=True)

        self._name = interface_name
        self._link_addresses = {}
        self._ipv4_addresses = {}
        self._ipv6_addresses = {}

    def has_link_address(self, address: str) -> bool:

        """Returns whether or not the link address already exists in the
        interface.

        Args:
            address (str): The link address to check.

        Returns:
            bool: 'True' if the given link address is already associated with
                the network interface, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not self._link_addresses:
            return False

        if address in self._link_addresses:
            return True

        return False

    def add_link_address(self, address: str) -> None:

        """Adds a new link address to the interface.

        Args:
            address (str): The address to add.

        Authors:
            Attila Kovacs
        """

        if self.has_link_address(address):
            self.warning(f'Link address {address} already exists in physical '
                         f'interface {self._name}, won\'t be added twice.')
            return

        self._link_addresses[address] = LinkAddress(address)
        self.debug(f'Link address {address} was added to physical interface '
                   f'{self._name}.')

    def has_ipv4_address(self, address: str) -> bool:

        """Returns whether or not the IPv4 already exists in the
        interface.

        Args:
            address (str): The IPv4 address to check.

        Returns:
            bool: 'True' if the given IPv4 address is already associated with
            the network interface, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not self._ipv4_addresses:
            return False

        if address in self._ipv4_addresses:
            return True

        return False

    def add_ipv4_address(self,
                         address: str,
                         netmask: str,
                         broadcast_address: str,
                         is_localhost: bool = False,
                         is_link_local_address: bool = False) -> None:

        """Adds a new IPv4 address to the interface.

        Args:
            address (str): The IPv4 address.

            netmask (str): The netmask of the address.

            broadcast_address (str): The broadcast address associated with the
                address.

            is_localhost (bool): Marks whether or not the address is a
                localhost address.

            is_link_local_address (bool): Marks whether or not the address is a
                link local address.

        Authors:
            Attila Kovacs
        """

        if self.has_ipv4_address(address):
            self.warning(f'IPv4 address {address} already exists in physical '
                         f'interface {self._name}, won\'t be added twice.')

        self._ipv4_addresses[address] = IPv4Address(address,
                                                    netmask,
                                                    broadcast_address,
                                                    is_localhost,
                                                    is_link_local_address)
        self.debug(f'IPv4 address {address} was added to physical interface '
                   f'{self._name}.')

    def has_ipv6_address(self, address: str) -> bool:

        """Returns whether or not the IPv6 already exists in the
        interface.

        Args:
            address (str): The IPv6 address to check.

        Returns:
            bool: 'True' if the given IPv6 address is already associated with
                the network interface, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not self._ipv6_addresses:
            return False

        if address in self._ipv6_addresses:
            return True

        return False

    def add_ipv6_address(self,
                         address: str,
                         netmask: str,
                         broadcast_address: str,
                         is_localhost: bool = False,
                         is_link_local_address: bool = False) -> None:

        """Adds a new IPv6 address to the interface.

        Args:
            address (str): The IPv6 address.

            netmask (str): The netmask of the address.

            broadcast_address (str): The broadcast address associated with the
                address.

            is_localhost (bool): Marks whether or not the address is a
                localhost address.

            is_link_local_address (bool): Marks whether or not the address is a
                link local address.

        Authors:
            Attila Kovacs
        """

        if self.has_ipv6_address(address):
            self.warning(f'IPv6 address {address} already exists in physical '
                         f'interface {self._name}, won\'t be added twice.')

        self._ipv6_addresses[address] = IPv6Address(address,
                                                    netmask,
                                                    broadcast_address,
                                                    is_localhost,
                                                    is_link_local_address)
        self.debug(f'IPv6 address {address} was added to physical interface '
                   f'{self._name}')
