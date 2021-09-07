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
Contains the unit tests of the VFS class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfslocalfile import VFSLocalFile

class TestVFSLocalFile:

    """Contains the unit tests of the VFSLocalFile class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a VFSLocalFile object can be created.

        Authors:
            Attila Kovacs
        """

        sut = VFSLocalFile()
        assert sut.Path is None

    def test_serialization(self) -> None:

        """Tests that at a VFSLocalFile object can be serialized to a
        dictionary.

        Authors:
            Attila Kovacs
        """

        sut = VFSLocalFile()
        sut._path = '/test/path'

        serialized = sut.serialize()

        assert serialized['type'] == 'localfile'
        assert serialized['path'] == '/test/path'


    def test_deserialization(self) -> None:

        """Tests that a VFSLocalFile object can be deserialized from a
        dictionary.

        Authors:
            Attila Kovacs
        """

        serialized = { 'type': 'localfile', 'path': '/test/path' }
        sut = VFSLocalFile()
        sut.deserialize(data=serialized)
        assert sut.Path == '/test/path'

    def test_deserialization_of_invalid_structure(self) -> None:

        """Tests the deserialization of an invalid structure.

        Authors:
            Attila Kovacs
        """

        # STEP #2 - Invalid structure cannot be deserialized
        sut = VFSLocalFile()
        with pytest.raises(InvalidInputError):
            sut.deserialize(data={'path': '/test/path'})

    def test_deserialization_without_type_marker(self) -> None:

        """Tests deserialization without a valid type marker in the serialized
        data.

        Authors:
            Attila Kovacs
        """

        sut = VFSLocalFile()
        serialized = { 'type': 'invalidtype', 'path': '/test/path' }
        with pytest.raises(InvalidInputError):
            sut.deserialize(data=serialized)
