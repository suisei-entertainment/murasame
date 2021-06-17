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
import tarfile
import shutil

# Dependency Imports
import pytest
import wget

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.pal.host.hostlocation import HostLocation
from murasame.exceptions import InvalidInputError

# Constants
DATABASE_PACKAGE_PATH = os.path.abspath(
    os.path.expanduser('/tmp/GeoLite2-City.tar.gz'))

DATABASE_PATH = os.path.abspath(
    os.path.expanduser('~/.murasame/testfiles/GeoLite2-City.mmdb'))

DATABASE_DIR = os.path.abspath(
    os.path.expanduser('~/.murasame/testfiles'))

def find_mmdb(members):
    for member in members:
        if os.path.splitext(member.name)[1] == '.mmdb':
            member.name = os.path.basename(member.name)
            yield member

GEOIP_DOWNLOAD_URL = \
    'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=pELDCVUneMIsHhyU&suffix=tar.gz'

class TestHostLocation:

    """
    Contains the unit tests of HostLocation class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        # Download a new GeoIP database
        wget.download(url=GEOIP_DOWNLOAD_URL, out=DATABASE_PACKAGE_PATH)
        tar = tarfile.open(DATABASE_PACKAGE_PATH)
        tar.extractall(path='/tmp', members=find_mmdb(tar))
        tar.close()
        shutil.move(src='/tmp/GeoLite2-City.mmdb', dst=DATABASE_PATH)
        os.remove(DATABASE_PACKAGE_PATH)

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(DATABASE_PATH):
            os.remove(DATABASE_PATH)

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
                           database_path=DATABASE_DIR)
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
                           database_path=DATABASE_DIR)
        assert sut.Continent == 'UNKNOWN'
        assert sut.Country == 'UNKNOWN'
        assert sut.City == 'UNKNOWN'
        assert sut.PostalCode == 'UNKNOWN'
        assert sut.Location == (0,0)
