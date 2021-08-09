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
Contains the unit tests of HostLocation class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.hostlocation import HostLocation
from murasame.exceptions import InvalidInputError

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

class TestHostLocation:

    """
    Contains the unit tests of HostLocation class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_valid_ip_without_database(self):

        """
        Tests that a HostLocation instance can be created successfully with
        a valid IP address but without a GeoIP database.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = HostLocation(public_ip='5.187.173.113',
                               database_path='/data')
            assert sut.Continent == 'UNKNOWN'
            assert sut.Country == 'UNKNOWN'
            assert sut.City == 'UNKNOWN'
            assert sut.PostalCode == 'UNKNOWN'
            assert sut.Location == (0,0)

    def test_creation_without_valid_ip_without_database(self):

        """
        Tests that a HostLocation instance can be created successfully without
        a valid IP address and a GeoIP database.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = HostLocation(public_ip='192.168.0.1',
                               database_path='/data')
            assert sut.Continent == 'UNKNOWN'
            assert sut.Country == 'UNKNOWN'
            assert sut.City == 'UNKNOWN'
            assert sut.PostalCode == 'UNKNOWN'
            assert sut.Location == (0,0)

    def test_creation_with_valid_ip_and_database(self):

        """
        Tests that a HostLocation instance can be created successfully with
        a valid IP address and GeoIP database.

        Authors:
            Attila Kovacs
        """

        sut = HostLocation(public_ip='5.187.173.113',
                           database_path=TEST_FILES_DIRECTORY)
        assert sut.Continent != 'UNKNOWN'
        assert sut.Country != 'UNKNOWN'
        assert sut.City != 'UNKNOWN'
        assert sut.PostalCode != 'UNKNOWN'
        assert sut.Location != (0,0)

    def test_creation_with_invalid_ip_and_valid_database(self):

        """
        Tests that a HostLocation instance can be created successfully without
        a valid IP address but with a GeoIP database.

        Authors:
            Attila Kovacs
        """

        sut = HostLocation(public_ip='192.168.0.1',
                           database_path=TEST_FILES_DIRECTORY)
        assert sut.Continent == 'UNKNOWN'
        assert sut.Country == 'UNKNOWN'
        assert sut.City == 'UNKNOWN'
        assert sut.PostalCode == 'UNKNOWN'
        assert sut.Location == (0,0)
