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
Contains the unit tests of GRPCServer class.
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
from murasame.pal.networking.grpcserver import GRPCServer
from murasame.pal.networking.grpcservertypes import GRPCServerTypes
from murasame.utils import SystemLocator
from murasame.api import VFSAPI
from murasame.pal.vfs import VFS

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

GRPC_TEST_DIRECTORY = f'{TEST_FILES_DIRECTORY}/grpc'

PROTOCOL_INPUT_DIRECTORY = f'{GRPC_TEST_DIRECTORY}/input'
PROTOCOL_OUTPUT_DIRECTORY = f'{GRPC_TEST_DIRECTORY}/output'
PROTOCOL_FILE = f'{GRPC_TEST_DIRECTORY}/testfile.proto'

class TestGRPCServer:

    """Contains the unit tests for the GRPCServer class.

    Authors:
        Attila Kovacs
    """

    def test_creation_of_insecure_server(self) -> None:

        """Tests that an insecure gRPC server can be created.

        Authors:
            Attila Kovacs
        """

        sut = GRPCServer(port=12345,
                         server_type=GRPCServerTypes.INSECURE)

        assert sut is not None
        assert isinstance(sut, GRPCServer)
        assert sut.Server is not None

    def test_creation_of_secure_server_with_valid_certificate(self) -> None:

        """Tests that a secure gRPC server can be created with a valid
        certificate.

        Authors:
            Attila Kovacs
        """

        sut = GRPCServer(port=12346,
                         server_type=GRPCServerTypes.SECURE,
                         certificate_path=f'{GRPC_TEST_DIRECTORY}/cert.pem',
                         private_key_path=f'{GRPC_TEST_DIRECTORY}/key.pem')

    def test_creation_of_secure_server_without_valid_certificate(self) -> None:

        """Tests that a secure gRPC server cannot be created without a valid
        certificate.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = GRPCServer(port=12347,
                             server_type=GRPCServerTypes.SECURE)

    def test_start_stop_server_in_non_blocking_mode(self) -> None:

        """Tests that a gRPC server can be started in non-blocking mode and
        stopped.

        Authors:
            Attila Kovacs
        """

        sut = GRPCServer(port=12348,
                         server_type=GRPCServerTypes.INSECURE)

        sut.start()
        sut.stop(grace_period=1)

    def test_start_stop_server_in_blocking_mode(self) -> None:

        """Tests that a gRPC server can be started in blocking mode and
        stopped.

        Authors:
            Attila Kovacs
        """

        sut = GRPCServer(port=12349,
                         server_type=GRPCServerTypes.INSECURE)

        sut.start(block=True, timeout=0.1)
        sut.stop()

    def test_compiling_protocol_files(self) -> None:

        """Tests that protocol files can be compiled through the gRPC server
        object.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(path=GRPC_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = GRPCServer(port=12350,
                         server_type=GRPCServerTypes.INSECURE)

        assert sut.compile_protocol(input_path='/input',
                                    output_path=PROTOCOL_OUTPUT_DIRECTORY)

        assert os.path.isfile(f'{PROTOCOL_OUTPUT_DIRECTORY}/testfile_pb2.py')
        assert os.path.isfile(f'{PROTOCOL_OUTPUT_DIRECTORY}/testfile_pb2_grpc.py')

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_message_handling(self) -> None:

        """Tests that gRPC messages can be handled.

        Authors:
            Attila Kovacs
        """

        #TODO
