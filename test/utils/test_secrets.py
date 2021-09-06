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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import Secrets, JsonFile

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

TEST_PASSWORD = 'testpassword'

def get_password():
    return TEST_PASSWORD

class TestSecrets:

    """Contains all unit tests of the GeoIP class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_existing_directory(self) -> None:

        """Tests that a Secrets object can be created with a valid config
        directory.

        Authors:
            Attila Kovacs
        """

        sut = Secrets(config_directory=TEST_FILES_DIRECTORY)
        assert sut is not None

    def test_creation_with_invalid_directory(self) -> None:

        """Tests that a Secrets object cannot be created without providing a
        config directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Secrets(config_directory=None)

    def test_creation_with_non_existent_directory(self) -> None:

        """Tests that a Secrets object cannot be created without a valid config
        directory.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Secrets(config_directory='/invalid/path')

    def test_creation_without_config_file(self) -> None:

        """Tests that a Secrets object cannot be created without a valid
        secrets.conf file.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = Secrets(config_directory='~')

    def test_retrieving_valid_key(self) -> None:

        """Tests that values can be retrieved from the secrets file.

        Authors:
            Attila Kovacs
        """

        # Set the environment variable
        os.environ['MURASAME_SECRETS_KEY'] = TEST_PASSWORD

        sut = Secrets(config_directory=TEST_FILES_DIRECTORY)
        assert sut.get_secret(key='testkey') == 'testvalue'

    def test_retrieving_invalid_key(self) -> None:

        """Test handling of retrieval of non-existent key.

        Authors:
            Attila Kovacs
        """

        # Set the environment variable
        os.environ['MURASAME_SECRETS_KEY'] = TEST_PASSWORD

        sut = Secrets(config_directory=TEST_FILES_DIRECTORY)
        assert sut.get_secret(key='invalidkey') == None