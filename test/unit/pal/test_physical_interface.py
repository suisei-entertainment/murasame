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
Contains the unit tests of PhysicalInterface class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.hostnetworking import PhysicalInterface

class TestPhysicalInterface:

    """
    Contains the unit tests of PhysicalInterface class.
    """

    def test_creation(self):

        """
        Tests that a PhysicalInterface instance can be created.
        """

        sut = PhysicalInterface(interface_name='test')
        assert sut.Name == 'test'

    def test_link_address_handling(self):

        """
        Tests that link adddresses are handled correctly.
        """

        sut = PhysicalInterface(interface_name='test')
        assert not sut.has_link_address('00:0A:95:9D:68:16')
        sut.add_link_address(address='00:0A:95:9D:68:16')
        assert sut.has_link_address('00:0A:95:9D:68:16')
        assert not sut.has_link_address('00:0A:95:9D:68:FF')
        sut.add_link_address(address='00:0A:95:9D:68:16')

    def test_ipv4_address_handling(self):

        """
        Tests that IPv4 addresses are handled correctly.
        """

        sut = PhysicalInterface(interface_name='test')
        assert not sut.has_ipv4_address('192.168.0.1')
        sut.add_ipv4_address(address='192.168.0.1',
                             netmask='255.255.255.0',
                             broadcast_address='192.168.0.255',
                             is_localhost=False,
                             is_link_local_address=False)
        assert sut.has_ipv4_address('192.168.0.1')
        assert not sut.has_ipv4_address('192.168.0.2')
        sut.add_ipv4_address(address='192.168.0.1',
                             netmask='255.255.255.0',
                             broadcast_address='192.168.0.255',
                             is_localhost=False,
                             is_link_local_address=False)

    def test_ipv6_address_handling(self):

        """
        Tests that IPv6 addresses are handled correctly.
        """

        sut = PhysicalInterface(interface_name='test')
        assert not sut.has_ipv6_address('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        sut.add_ipv6_address(address='2001:0db8:85a3:0000:0000:8a2e:0370:7334',
                             netmask='ffff:ffff:ffff::',
                             broadcast_address='',
                             is_localhost=False,
                             is_link_local_address=False)
        assert sut.has_ipv6_address('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        assert not sut.has_ipv6_address('2001:0db8:85a3:0000:0000:8a2e:0370:7335')
        sut.add_ipv6_address(address='2001:0db8:85a3:0000:0000:8a2e:0370:7334',
                             netmask='ffff:ffff:ffff::',
                             broadcast_address='',
                             is_localhost=False,
                             is_link_local_address=False)
