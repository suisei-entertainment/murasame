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
Contains the implementation of the IPAddress class.
"""

class IPAddress:

    """Representation of an IP address of a physical network interface.

    Attributes:
        _address (str): The actual IP address.

        _netmask (str): The netmask associated with the IP address.

        _broadcast_address (str): The broadcast address associated with the IP
            address.

        _is_localhost (bool): Whether or not the address is a localhost
            address.

        _is_link_local_address (bool): Whether or not the address is a link
            local address.

    Authors:
        Attila Kovacs
    """

    @property
    def Address(self) -> str:

        """The IP address.

        Authors:
            Attila Kovacs
        """

        return self._address

    @property
    def Netmask(self) -> str:

        """The netmask associated with the address.

        Authors:
            Attila Kovacs
        """

        return self._netmask

    @property
    def BroadcastAddress(self) -> str:

        """The broadcast address associated with the address.

        Authors:
            Attila Kovacs
        """

        return self._broadcast_address

    def __init__(self,
                 address: str,
                 netmask: str,
                 broadcast_address: str,
                 is_localhost: bool = False,
                 is_link_local_address: bool = False) -> None:

        """Creates a new IPAddress instance.

        Args:
            address (str): The actual IP address.

            netmask (str): The netmask associated with the IP address.

            broadcast_address (str): The broadcast address associated with the
                IP address.

            is_localhost (bool): Whether or not the address is a localhost
                address.

            is_link_local_address (bool): Whether or not the address is a link
                local address.

        Authors:
            Attila Kovacs
        """

        self._address = address
        self._netmask = netmask
        self._broadcast_address = broadcast_address
        self._is_localhost = is_localhost
        self._is_link_local_address = is_link_local_address

    def is_localhost(self) -> bool:

        """Returns whether or not the address represents a localhost address.

        Returns:
            bool: 'True' if the address is a localhost address, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        return self._is_localhost

    def is_link_local_address(self) -> bool:

        """Returns whether or not the address represents a link local address.

        Returns:
            bool: 'True' if the address is a link local address, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        return self._is_link_local_address
