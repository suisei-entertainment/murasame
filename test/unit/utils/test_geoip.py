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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import GeoIP, GeoIPData

DATABASE_UPDATE_LINK = \
    'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=pELDCVUneMIsHhyU&suffix=tar.gz'

DATABASE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles'))

class TestGeoIP:

    """
    Contains all unit tests of the GeoIP class.
    """

    def test_creation(self):

        """
        Tests that a GeoIP object can be created.
        """

        # Delete the database if it's already there
        if os.path.isfile('{}/GeoLite2-City.mmdb'.format(DATABASE_PATH)):
            os.remove('{}/GeoLite2-City.mmdb'.format(DATABASE_PATH))

        sut = GeoIP(update_link=DATABASE_UPDATE_LINK,
                    database_path=DATABASE_PATH)


        assert sut is not None
        assert os.path.isfile(
            '{}/GeoLite2-City.mmdb'.format(DATABASE_PATH))

    def test_geoip_query(self):

        """
        Tests that IP addresses can be queried.
        """

        sut = GeoIP(update_link=DATABASE_UPDATE_LINK,
                    database_path=DATABASE_PATH)

        # STEP #1 - Query valid IP address
        result = sut.query('5.187.173.113')
        assert result is not None
        assert result.IPAddress == '5.187.173.113'
        assert result.Continent == 'Europe'
        assert result.Country == 'Hungary'
        assert result.City == 'God'
        assert result.PostalCode in ('2131', '2132')
        assert result.Latitude == 47.6838
        assert result.Longitude == 19.1401

        # STEP #2 - Query internal IP address
        result = sut.query('192.168.0.1')
        assert result is not None
        assert result.IPAddress == '192.168.0.1'
        assert result.Continent == 'UNKNOWN'
        assert result.Country == 'UNKNOWN'
        assert result.City == 'UNKNOWN'
        assert result.PostalCode == 'UNKNOWN'
        assert result.Latitude == 'UNKNOWN'
        assert result.Longitude == 'UNKNOWN'
