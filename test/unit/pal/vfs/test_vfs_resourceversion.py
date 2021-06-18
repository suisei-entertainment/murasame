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
Contains the unit tests of the ResourceVersion class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.resourceversion import ResourceVersion

class TestResourceVersion:

    """
    Contains the unit tests for the ResourceVersion class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_valid_version_number(self):

        """
        Tests that a ResourceVersion object can be created with a valid version
        number.

        Authors:
            Attila Kovacs
        """

        sut = ResourceVersion(version=1)
        assert sut is not None

    def test_creation_without_version_number(self):

        """
        Tests that a RersourceVersion object cannot be created without a
        version number.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(TypeError):
            sut = ResourceVersion()

    def test_creation_with_invalid_version_number(self):

        """
        Tests that a ResourceVersion object cannot be created with an invalid
        version number.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ResourceVersion(version=0)

        with pytest.raises(InvalidInputError):
            sut = ResourceVersion(version=-1)

    def test_comparison(self):

        """
        Tests that resource version instances can be compared.

        Authors:
            Attila Kovacs
        """
        sut1 = ResourceVersion(version=1)
        sut2 = ResourceVersion(version=1)
        sut3 = ResourceVersion(version=2)

        assert sut1 == sut2
        assert sut1 != sut3
        assert sut1 < sut3
        assert sut3 > sut1
        assert sut1 <= sut3
        assert sut3 >= sut1

        assert not sut1 == 1
        assert sut1 != 1

        with pytest.raises(TypeError):
            assert not sut1 <= 1

        with pytest.raises(TypeError):
            assert not sut1 >= 1

        with pytest.raises(TypeError):
            assert not sut1 < 1

        with pytest.raises(TypeError):
            assert not sut1 > 1

    def test_string_representations(self):

        """
        Tests that the string represenations of a resource version object are
        correct.

        Authors:
            Attila Kovacs
        """

        sut = ResourceVersion(version=1)

        assert sut.__str__() == '1'
        assert sut.__repr__() == 'ResourceVersion(1)'

    def test_bumping_version_number(self):

        """
        Tests that the version number can be bumped.

        Authors:
            Attila Kovacs
        """

        sut = ResourceVersion(version=1)

        assert sut.Version == 1
        sut.bump_version()
        assert sut.Version == 2

        sut.bump_version()
        sut.bump_version()
        assert sut.Version == 4
