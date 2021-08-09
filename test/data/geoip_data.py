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
Contains the test data for tests using GeoIP data.
"""

# Runtime Imports
import os
import tarfile
import shutil

# Dependency Imports
import wget

# Test Imports
from test.constants import TEST_FILES_DIRECTORY, GEOIP_LICENSE_KEY, GEOIP_DOWNLOAD_URL

# Constants
DATABASE_PACKAGE_PATH = os.path.abspath(
    os.path.expanduser('/tmp/GeoLite2-City.tar.gz'))

DATABASE_PATH = f'{TEST_FILES_DIRECTORY}/GeoLite2-City.mmdb'

def find_mmdb(members):
    for member in members:
        if os.path.splitext(member.name)[1] == '.mmdb':
            member.name = os.path.basename(member.name)
            yield member

def download_geoip_database():

    """
    Downloads a new GeoIP database from the Internet.

    Authors:
        Attila Kovacs
    """

    wget.download(url=GEOIP_DOWNLOAD_URL, out=DATABASE_PACKAGE_PATH)
    tar = tarfile.open(DATABASE_PACKAGE_PATH)
    tar.extractall(path='/tmp', members=find_mmdb(tar))
    tar.close()
    shutil.move(src='/tmp/GeoLite2-City.mmdb', dst=DATABASE_PATH)
    os.remove(DATABASE_PACKAGE_PATH)
