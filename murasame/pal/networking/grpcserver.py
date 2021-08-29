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
Contains the implementation of the GRPCServer class.
"""

# Runtime Imports
from concurrent import futures
from typing import Union

# Dependency Imports
import grpc

# Murasame Imports
from murasame.constants import MURASAME_GRPC_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log.logwriter import LogWriter
from murasame.pal.networking.grpcservertypes import GRPCServerTypes
from murasame.utils import X509Certificate, RSAPrivate

class GRPCServer(LogWriter):

    """Utility class to simplify the creation of a gRPC server.

    Attributes:

        _port (int): The port the server is going to listen on.

        _server_type (GRPCServerTypes): The type of the server.

        _server (object): The underlying gRPC server object.

        _server_credentials (object): The credentials to use when configuring
            a secure gRPC server.

    Authors:
        Attila Kovacs
    """

    @property
    def Server(self) -> object:

        """Provides access to the underlying gRPC server object.

        Authors:
            Attila Kovacs
        """

        return  self._server

    def __init__(
        self,
        port: int,
        server_type: GRPCServerTypes = GRPCServerTypes.SECURE,
        max_threads: Union[int, None] = None,
        certificate: X509Certificate = None,
        private_key: RSAPrivate = None,
        root_certificate: X509Certificate = None,
        capacity: Union[int, None] = None) -> None:

        """Creates a new GRPCServer object.

        Args:
            port (int): The port the server is going to listen on.

            server_type (GRPCServerTypes): The type of server to create.

            max_threads (Union[int, None]): The maximum amount of threads to
                assign to the server.

            certificate (X509Certificate): Optional X.509 certificate to use to
                secure the server.

            private_key (RSAPrivate): The private key associated with the
                certificate.

            root_certificate (X509Certificate): The root certificate to use for
                client authentication.

            capacity (Union[int, None]): The total amount of RPCs this server
                is allowed to execute.

        Raises:
            InvalidInputError: Raised when trying to create a secure GRPCServer
                object without a valid certificate and/or private key.

        Args:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_GRPC_LOG_CHANNEL,
                         cache_entries=True)

        if server_type == GRPCServerTypes.SECURE \
            and (certificate is None or private_key is None):
            raise InvalidInputError(
                'Cannot create a secure gRPC server without a valid '
                'certificate and private key.')

        self._server_type = server_type
        self._port = port

        # Create the server
        self._server = grpc.server(futures.ThreadPoolExecutor(
            max_workers=max_threads),
            maximum_concurrent_rpcs=capacity)

        # Create the server credentials
        self._server_credentials = None
        if server_type == GRPCServerTypes.SECURE:

            if root_certificate:
                self._server_credentials = grpc.ssl_server_credentials(
                    [(private_key.Key,
                      certificate.CertificateBytes)],
                    root_certificates=root_certificate.CertificateBytes,
                    require_client_auth=True)
            else:
                self._server_credentials = grpc.ssl_server_credentials(
                    [(private_key.Key,
                      certificate.CertificateBytes)],
                    root_certificates=None,
                    require_client_auth=False)

        # Add the port
        if server_type == GRPCServerTypes.SECURE:
            self._server.add_secure_port(f'[::]:{self._port}',
                                         self._server_credentials)
        else:
            self._server.add_insecure_port(f'[::]:{self._port}')

    def start(self, block: bool = False) -> None:

        """Starts the server.

        Args:
            block (bool): Whether or not starting the server should block the
                main thread. Defaults to 'False'.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Starting gRPC server on port {self._port}...')
        self._server.start()
        self.debug(f'gRPC server on port {self._port} has been started.')

        if block:
            self.debug(
                f'Waiting for gRPC server on port {self._port} to finish.')
            self._server.wait_for_termination()
            self.debug(
                f'gRPC server on port {self._port} has been terminated.')

    def stop(self, grace_period: Union[int, None] = None):

        """Stops the server.

        Args:
            grace_period (Union[int, None]): The amount of time in seconds to
                wait for the ongoing RPC requests to be finished before
                forcibly shutting down the worker threads.

        Authors:
            Attila Kovacs
        """

        if grace_period:
            self.debug(
                f'Stopping gRPC server on port {self._port} with a grace '
                f'period of {grace_period} seconds...')
        else:
            self.debug(
                f'Stopping gRPC server on port {self._port} immediately...')

        if self._server:
            self._server.stop(grace=grace_period)
        else:
            self.error(f'Trying to stop non-existent gRPC server on port '
                       f'{self._port}.')

        self.debug(f'gRPC server on port {self._port} has been stopped.')
