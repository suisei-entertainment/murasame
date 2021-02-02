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
Contains the unit tests of the YamlFile class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import YamlFile

TEST_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/yaml_test.yaml'))

INVALID_TEST_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/nonexistent.yaml'))

MALFORMED_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/malformed.yaml'))

def get_password():

    """
    Utility function for returning a password for file encryption tests.

    Returns:
        The test password.
    """

    return 'testpassword'

class TestYamlFile:

    """
    Contains all unit tests of the JsonFile class.
    """

    def test_creation(self):

        """
        Tests that a JsonFile object can be created.
        """

        # STEP 1 - Create file
        sut = YamlFile(path=TEST_FILE_PATH)
        assert sut.Path is not None
        assert sut.Content == {}

    def test_saving_and_loading_json_file(self):

        """
        Tests that YAML content can be saved to and loaded from a file on disk.
        """

        # STEP #1 - Compacted YAML file
        sut1 = YamlFile(path=TEST_FILE_PATH)
        sut1.Content['test'] = 'test content'
        sut1.save()
        del sut1

        sut2 = YamlFile(path=TEST_FILE_PATH)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

        # STEP #2 - Formatted YAML file
        sut1 = YamlFile(path=TEST_FILE_PATH)
        sut1.Content['test'] = 'test content'
        sut1.save(compact=False)
        del sut1

        sut2 = YamlFile(path=TEST_FILE_PATH)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

    def test_saving_and_loading_encrypted_json_file(self):

        """
        Tests that YAML content can be saved to and loaded from an encrypted
        file on disk.
        """

        sut1 = YamlFile(path=TEST_FILE_PATH, cb_retrieve_key=get_password)
        sut1.Content['test'] = 'test content'
        sut1.save()

        sut2 = YamlFile(path=TEST_FILE_PATH, cb_retrieve_key=get_password)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

    def test_loading_non_existent_file(self):

        """
        Tests loading a non-existent YAML file is handled properly.
        """

        sut = YamlFile(path=INVALID_TEST_FILE_PATH)
        sut.load()
        assert sut.Content == {}

    def test_savig_file_to_invalid_location(self):

        """
        Tests that the file is not saved to an invalid location.
        """

        # STEP #1 - Unencrypted YAML file
        sut = YamlFile(path='/invalid/path/to/somewhere/file.yaml')
        with pytest.raises(RuntimeError):
            sut.save()

        # STEP #2 - Encrypted YAML file
        sut = YamlFile(path='/invalid/path/to/somewhere/file.yaml',
                       cb_retrieve_key=get_password)
        with pytest.raises(RuntimeError):
            sut.save()

    def test_loading_malformed_yaml_file(self):

        # Create a malformed file
        malformed_json = '{invalid yaml: [}'
        with open(MALFORMED_FILE_PATH, 'w+') as malformed:
            malformed.write(malformed_json)

        # STEP 1 - Trying to load a malformed YAML file results in
        # an exception
        sut = YamlFile(path=MALFORMED_FILE_PATH)
        with pytest.raises(InvalidInputError):
            sut.load()

        # Create a malformed file and encrypt it
        from murasame.utils import AESCipher
        cipher = AESCipher(get_password())
        content = cipher.encrypt(malformed_json)
        with open(MALFORMED_FILE_PATH, 'wb') as malformed:
            malformed.write(content)

        # STEP #2 - Trying to load an encrypted and malformed JSON file results
        # in an exception

        sut = YamlFile(path=MALFORMED_FILE_PATH, cb_retrieve_key=get_password)
        with pytest.raises(InvalidInputError):
            sut.load()

    def test_overwrite_yaml_file_content(self):

        sut1 = YamlFile(path=TEST_FILE_PATH)
        sut1.Content['test'] = 'test content'
        sut1.overwrite_content({'test': 'overwritten'})
        assert sut1.Content['test'] == 'overwritten'
