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
from murasame.vfs.vfslocalfile import VFSLocalFile

class TestVFSLocalFile:

    """
    Contains the unit tests of the VFSLocalFile class.
    """

    def test_creation(self):

        """
        Tests that a VFSLocalFile object can be created.
        """

        sut = VFSLocalFile()
        assert sut.Path is None

    def test_serialization(self):

        """
        Tests that at a VFSLocalFile object can be serialized to a dictionary.
        """

        sut = VFSLocalFile()
        sut._path = '/test/path'

        serialized = sut.serialize()

        assert serialized['type'] == 'localfile'
        assert serialized['path'] == '/test/path'


    def test_deserialization(self):

        """
        Tests that a VFSLocalFile object can be deserialized from a dictionary.
        """

        # STEP #1 - Valid structure can be deserialized
        serialized = { 'type': 'localfile', 'path': '/test/path' }
        sut = VFSLocalFile()
        sut.deserialize(data=serialized)
        assert sut.Path == '/test/path'

        # STEP #2 - Invalid structure cannot be deserialized
        sut = VFSLocalFile()
        with pytest.raises(InvalidInputError):
            sut.deserialize(data={'path': '/test/path'})

        # STEP #3 - Structure without type marker cannot be deserialized
        sut = VFSLocalFile()
        serialized = { 'type': 'invalidtype', 'path': '/test/path' }
        with pytest.raises(InvalidInputError):
            sut.deserialize(data=serialized)
