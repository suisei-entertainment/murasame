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
Contains the unit tests of IpAddress class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.ipaddress import IPAddress
from murasame.pal.host.ipv4address import IPv4Address
from murasame.pal.host.ipv6address import IPv6Address

class TestIPAddress:

    """
    Contains the unit tests of IpAddress class.
    """

    def test_creation(self):

        """
        Tests that a IpAddress instance can be created.
        """

        sut = IPAddress(address='192.168.0.1',
                        netmask='255.255.255.0',
                        broadcast_address='192.168.0.255',
                        is_localhost=False,
                        is_link_local_address=False)

        assert sut.Address == '192.168.0.1'
        assert sut.Netmask == '255.255.255.0'
        assert sut.BroadcastAddress == '192.168.0.255'
        assert not sut.is_localhost()
        assert not sut.is_link_local_address()

        sut = IPv4Address(address='192.168.0.1',
                          netmask='255.255.255.0',
                          broadcast_address='192.168.0.255',
                          is_localhost=False,
                          is_link_local_address=False)

        assert sut.Address == '192.168.0.1'
        assert sut.Netmask == '255.255.255.0'
        assert sut.BroadcastAddress == '192.168.0.255'
        assert not sut.is_localhost()
        assert not sut.is_link_local_address()

        sut = IPv6Address(address='2001:0db8:85a3:0000:0000:8a2e:0370:7334',
                          netmask='ffff:ffff:ffff::',
                          broadcast_address='',
                          is_localhost=False,
                          is_link_local_address=False)

        assert sut.Address == '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        assert sut.Netmask == 'ffff:ffff:ffff::'
        assert sut.BroadcastAddress == ''
        assert not sut.is_localhost()
        assert not sut.is_link_local_address()
