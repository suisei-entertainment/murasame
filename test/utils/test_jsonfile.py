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
Contains the unit tests of the JsonFile class.
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
from murasame.utils import JsonFile

TEST_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/json_test.json'))

TEST_FILE_PATH_2 = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/json_test2.json'))

TEST_FILE_PATH_3 = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/json_test3.json'))

TEST_FILE_PATH_4 = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/json_test4.json'))

TEST_FILE_PATH_5 = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/json_test5.json'))

INVALID_TEST_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/nonexistent.json'))

MALFORMED_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/malformed.json'))

MALFORMED_FILE_PATH_2 = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/malformed_2.json'))

def get_password():

    """
    Utility function for returning a password for file encryption tests.

    Returns:
        The test password.

    Authors:
        Attila Kovacs
    """

    return 'testpassword'

class TestJsonFile:

    """
    Contains all unit tests of the JsonFile class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a JsonFile object can be created.

        Authors:
            Attila Kovacs
        """

        sut = JsonFile(path=TEST_FILE_PATH)
        assert sut.Path is not None
        assert sut.Content == {}

    def test_saving_and_loading_compacted_json_file(self):

        """
        Tests that a compacted JSON content can be saved to and loaded from a
        file on disk.

        Authors:
            Attila Kovacs
        """

        sut1 = JsonFile(path=TEST_FILE_PATH_2)
        sut1.Content['test'] = 'test content'
        sut1.save()
        del sut1

        sut2 = JsonFile(path=TEST_FILE_PATH_2)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

    def test_saving_and_loading_formatted_json_file(self):

        """
        Tests that a formatted JSON content can be saved to and loaded from a
        file on disk.

        Authors:
            Attila Kovacs
        """

        sut1 = JsonFile(path=TEST_FILE_PATH_3)
        sut1.Content['test'] = 'test content'
        sut1.save(compact=False)
        del sut1

        sut2 = JsonFile(path=TEST_FILE_PATH_3)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

    def test_saving_and_loading_encrypted_json_file(self):

        """
        Tests that JSON content can be saved to and loaded from an encrypted
        file on disk.

        Authors:
            Attila Kovacs
        """

        sut1 = JsonFile(path=TEST_FILE_PATH_4, cb_retrieve_key=get_password)
        sut1.Content['test'] = 'test content'
        sut1.save()

        sut2 = JsonFile(path=TEST_FILE_PATH_4, cb_retrieve_key=get_password)
        sut2.load()
        assert sut2.Content['test'] == 'test content'

    def test_loading_non_existent_file(self):

        """
        Tests loading a non-existent JSON file is handled properly.

        Authors:
            Attila Kovacs
        """

        sut = JsonFile(path=INVALID_TEST_FILE_PATH)
        sut.load()
        assert sut.Content == {}

    def test_savig_unencrypted_file_to_invalid_location(self):

        """
        Tests that an unencrypted JSON  file is not saved to an invalid
        location.

        Authors:
            Attila Kovacs
        """

        sut = JsonFile(path='/invalid/path/to/somewhere/file.json')
        with pytest.raises(RuntimeError):
            sut.save()

    def test_savig_encrypted_file_to_invalid_location(self):

        """
        Tests that an encrypted JSON  file is not saved to an invalid
        location.

        Authors:
            Attila Kovacs
        """

        sut = JsonFile(path='/invalid/path/to/somewhere/file.json',
                       cb_retrieve_key=get_password)
        with pytest.raises(RuntimeError):
            sut.save()

    def test_loading_unencrypted_malformed_json_file(self):

        """
        Tests loading an unencrypted and malformed JSON file.

        Authors:
            Attila Kovacs
        """

        # Create a malformed file
        malformed_json = '{invalid json: [}'
        with open(MALFORMED_FILE_PATH, 'w+') as malformed:
            malformed.write(malformed_json)

        sut = JsonFile(path=MALFORMED_FILE_PATH)
        with pytest.raises(InvalidInputError):
            sut.load()

    def test_loading_encrypted_malformed_json_file(self):

        """
        Tests loading an encrypted and malformed JSON file.

        Authors:
            Attila Kovacs
        """

        # Create a malformed file and encrypt it
        malformed_json = '{invalid json: [}'
        from murasame.utils import AESCipher
        cipher = AESCipher(get_password())
        content = cipher.encrypt(malformed_json)
        with open(MALFORMED_FILE_PATH_2, 'wb') as malformed:
            malformed.write(content)

        sut = JsonFile(path=MALFORMED_FILE_PATH_2, cb_retrieve_key=get_password)
        with pytest.raises(InvalidInputError):
            sut.load()

    def test_overwrite_json_file_content(self):

        """
        Tests that athe content of the JSON file can be overwritten.

        Authors:
            Attila Kovacs
        """

        sut1 = JsonFile(path=TEST_FILE_PATH_5)
        sut1.Content['test'] = 'test content'
        sut1.overwrite_content({'test': 'overwritten'})
        assert sut1.Content['test'] == 'overwritten'
