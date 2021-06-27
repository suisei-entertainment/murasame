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
Contains the unit tests of Secrets class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import Secrets, JsonFile

# Test data
TEST_CONFIG_DIRECTORY = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles'))

TEST_DATA = \
{
    'testkey': 'testvalue'
}

TEST_PASSWORD = 'testpassword'

def get_password():
    return TEST_PASSWORD

class TestSecrets:

    """
    Contains all unit tests of the GeoIP class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        # Create the test file
        config_file = JsonFile(
            path=f'{TEST_CONFIG_DIRECTORY}/secrets.conf',
            cb_retrieve_key=get_password)
        config_file.overwrite_content(content=TEST_DATA)
        config_file.save()

        # Set the environment variable
        os.environ['MURASAME_SECRETS_KEY'] = TEST_PASSWORD

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(f'{TEST_CONFIG_DIRECTORY}/secrets.conf'):
            os.remove(f'{TEST_CONFIG_DIRECTORY}/secrets.conf')

    def test_creation(self):

        """
        Tests that a Secrets object can be created.

        Authors:
            Attila Kovacs
        """

        sut = Secrets(config_directory=TEST_CONFIG_DIRECTORY)
        assert sut is not None

    def test_query(self):

        """
        Tests that values can be retrieved from the secrets file.

        Authors:
            Attila Kovacs
        """

        sut = Secrets(config_directory=TEST_CONFIG_DIRECTORY)
        assert sut.get_secret(key='testkey') == 'testvalue'
