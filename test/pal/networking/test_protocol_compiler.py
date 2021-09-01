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
Contains the unit tests of ProtocolCompiler class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.networking.protocolcompiler import ProtocolCompiler
from murasame.utils import SystemLocator
from murasame.pal.vfs import VFS
from murasame.api import VFSAPI

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

PROTOCOL_DIRECTORTY = os.path.abspath(os.path.expanduser(
    f'{TEST_FILES_DIRECTORY}/protocolcompiler'))

PROTOCOL_INPUT_DIRECTORY = f'{PROTOCOL_DIRECTORTY}/input'
PROTOCOL_OUTPUT_DIRECTORY = f'{PROTOCOL_DIRECTORTY}/output'
INVALID_INPUT_DIRECTORY = f'{PROTOCOL_DIRECTORTY}/invalidinput'

PROTOCOL_FILE = f'{PROTOCOL_INPUT_DIRECTORY}/testfile.proto'

class TestProtocolCompiler:

    """Contains the unit tests of ProtocolCompiler class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_valid_parameters(self) -> None:

        """Tests that a ProtocolCompiler instance can be created with valid
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = ProtocolCompiler(path='/input',
                               include_path=PROTOCOL_INPUT_DIRECTORY,
                               output_path=PROTOCOL_OUTPUT_DIRECTORY)

        assert sut is not None

    def test_compilation_of_valid_source_files(self) -> None:

        """Tests that valid protocol files can be compiled.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(path=PROTOCOL_DIRECTORTY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = ProtocolCompiler(path='/input',
                               include_path=PROTOCOL_INPUT_DIRECTORY,
                               output_path=PROTOCOL_OUTPUT_DIRECTORY)

        assert sut.compile()
        assert os.path.isfile(f'{PROTOCOL_OUTPUT_DIRECTORY}/testfile_pb2.py')
        assert os.path.isfile(f'{PROTOCOL_OUTPUT_DIRECTORY}/testfile_pb2_grpc.py')

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_compilation_of_invalid_source_file(self) -> None:

        """Tests trying to compile a source file with invalid syntax.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(path=PROTOCOL_DIRECTORTY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = ProtocolCompiler(path='/invalidinput',
                               include_path=INVALID_INPUT_DIRECTORY,
                               output_path=PROTOCOL_OUTPUT_DIRECTORY)

        assert not sut.compile()

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)