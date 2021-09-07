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
Contains the unit tests of SecureTarFile class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils.securetarfile import SecureTarFile
from murasame.exceptions import SecurityValidationError

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

TARTEST_DIRECTORY = f'{TEST_FILES_DIRECTORY}/tartest'

class TestSecureTarFile:

    """Contains the unit tests for the SecureTarFile class.

    Authors:
        Attila Kovacs
    """

    def test_creation_without_parameters(self) -> None:

        """Tests that a SecureTarFile object cannot be created without
        valid parameters.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(TypeError):
            sut = SecureTarFile()

    def test_opening_valid_tar_file(self) -> None:

        """Tests that a valid tar file can be opened.

        Authors:
            Attila Kovacs
        """

        with SecureTarFile.open(name=f'{TARTEST_DIRECTORY}/valid.tar.gz') as tar:
            assert tar is not None
            assert isinstance(tar, SecureTarFile)

    def test_extracting_from_valid_tar_file(self) -> None:

        """Tests that members can be extracted from a valid tar file.

        Authors:
            Attila Kovacs
        """

        with SecureTarFile.open(name=f'{TARTEST_DIRECTORY}/valid.tar.gz') as tar:
            tar.extract(path=TARTEST_DIRECTORY, member=tar.getmembers()[0])

        assert os.path.isdir(f'{TARTEST_DIRECTORY}/home')

    def test_extracting_from_tarbomb(self) -> None:

        """Tests that a tar bomb is recognized when trying to extract a single
        member from it.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(SecurityValidationError):
            with SecureTarFile.open(name=f'{TARTEST_DIRECTORY}/tarbomb.tar.gz') as tar:
                tar.extract(member=tar.getmembers()[0])

    def test_extracting_all_from_valid_tar_file(self) -> None:

        """Tests that all members can be extracted from a valid tar file.

        Authors:
            Attila Kovacs
        """

        with SecureTarFile.open(name=f'{TARTEST_DIRECTORY}/valid.tar.gz') as tar:
            tar.extractall(path=TARTEST_DIRECTORY)

        assert os.path.isdir(f'{TARTEST_DIRECTORY}/home')

    def test_extracting_all_from_tarbomb(self) -> None:

        """Tests that a tar bomb is recognized when trying to extract all
        members from it.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(SecurityValidationError):
            with SecureTarFile.open(name=f'{TARTEST_DIRECTORY}/tarbomb.tar.gz') as tar:
                tar.extractall(members=tar.getmembers())
