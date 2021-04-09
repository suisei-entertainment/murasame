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

class TestHostLocation:

    """
    Contains the unit tests of HostLocation class.
    """

    def test_creation(self):

        """
        Tests that a HostLocation instance can be created successfully.
        """

        # Download a GeoIP database
        download_url = \
            'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=pELDCVUneMIsHhyU&suffix=tar.gz'

        print('')
        print('Downloading GeoIP database...')
        wget.download(url=download_url, out=DATABASE_PACKAGE_PATH)
        print('')
        print('Extracting GeoIP database...')
        tar = tarfile.open(DATABASE_PACKAGE_PATH)
        tar.extractall(path='/tmp', members=find_mmdb(tar))
        tar.close()
        shutil.move(src='/tmp/GeoLite2-City.mmdb', dst=DATABASE_PATH)
        os.remove(DATABASE_PACKAGE_PATH)

        # STEP #1 - Create with a valid IP, but without a database
        with pytest.raises(InvalidInputError):
            sut = HostLocation(public_ip='5.187.173.113',
                               database_path='/data')
            assert sut.Continent == 'UNKNOWN'
            assert sut.Country == 'UNKNOWN'
            assert sut.City == 'UNKNOWN'
            assert sut.PostalCode == 'UNKNOWN'
            assert sut.Location == (0,0)

        # STEP #2 - Create with an invalid IP and without a database
        with pytest.raises(InvalidInputError):
            sut = HostLocation(public_ip='192.168.0.1',
                               database_path='/data')
            assert sut.Continent == 'UNKNOWN'
            assert sut.Country == 'UNKNOWN'
            assert sut.City == 'UNKNOWN'
            assert sut.PostalCode == 'UNKNOWN'
            assert sut.Location == (0,0)

        # STEP #3 - Create with a valid IP and a database
        sut = HostLocation(public_ip='5.187.173.113',
                           database_path=DATABASE_DIR)
        assert sut.Continent != 'UNKNOWN'
        assert sut.Country != 'UNKNOWN'
        assert sut.City != 'UNKNOWN'
        assert sut.PostalCode != 'UNKNOWN'
        assert sut.Location != (0,0)

        # STEP #4 - Create with an invalid IP and a database
        sut = HostLocation(public_ip='192.168.0.1',
                           database_path=DATABASE_DIR)
        assert sut.Continent == 'UNKNOWN'
        assert sut.Country == 'UNKNOWN'
        assert sut.City == 'UNKNOWN'
        assert sut.PostalCode == 'UNKNOWN'
        assert sut.Location == (0,0)
