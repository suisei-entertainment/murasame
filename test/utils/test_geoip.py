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
Contains the unit tests of GeoIP class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import GeoIP, GeoIPData

# Test Imports
from test.constants import TEST_FILES_DIRECTORY, GEOIP_DOWNLOAD_URL

class TestGeoIP:

    """
    Contains all unit tests of the GeoIP class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a GeoIP object can be created.

        Authors:
            Attila Kovacs
        """

        sut = GeoIP(update_link=GEOIP_DOWNLOAD_URL,
                    database_path=TEST_FILES_DIRECTORY)

        assert sut is not None
        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/GeoLite2-City.mmdb')

    def test_geoip_query_with_valid_ip_address(self):

        """
        Tests that valid IP addresses can be queried.

        Authors:
            Attila Kovacs
        """

        sut = GeoIP(update_link=GEOIP_DOWNLOAD_URL,
                    database_path=TEST_FILES_DIRECTORY)

        result = sut.query('8.8.8.8')
        assert result is not None
        assert result.IPAddress == '8.8.8.8'
        assert result.Continent == 'North America'
        assert result.Country == 'United States'
        assert result.City == None
        assert result.PostalCode == None
        assert result.Latitude == 37.751
        assert result.Longitude == -97.822

    def test_geoip_with_local_ip_address(self):

        """
        Test querying an internal IP address for GeoIP.

        Authors:
            Attila Kovacs
        """

        sut = GeoIP(update_link=GEOIP_DOWNLOAD_URL,
                    database_path=TEST_FILES_DIRECTORY)

        result = sut.query('192.168.0.1')
        assert result is not None
        assert result.IPAddress == '192.168.0.1'
        assert result.Continent == 'UNKNOWN'
        assert result.Country == 'UNKNOWN'
        assert result.City == 'UNKNOWN'
        assert result.PostalCode == 'UNKNOWN'
        assert result.Latitude == 'UNKNOWN'
        assert result.Longitude == 'UNKNOWN'

    def test_geoip_with_invalid_ip_address(self):

        """
        Test querying an invalid IP address for GeoIP.

        Authors:
            Attila Kovacs
        """

        sut = GeoIP(update_link=GEOIP_DOWNLOAD_URL,
                    database_path=TEST_FILES_DIRECTORY)

        result = sut.query('256.256.0.1')
        assert result is not None
        assert result.IPAddress == '256.256.0.1'
        assert result.Continent == 'UNKNOWN'
        assert result.Country == 'UNKNOWN'
        assert result.City == 'UNKNOWN'
        assert result.PostalCode == 'UNKNOWN'
        assert result.Latitude == 'UNKNOWN'
        assert result.Longitude == 'UNKNOWN'