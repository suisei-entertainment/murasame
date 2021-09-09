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
Contains the initialization logic for all test data needed by the tests.
"""

# Runtime Imports
import os
import time

# Dependency Imports
import shutil

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

from test.data.app_data import create_application_data
from test.data.licensing_data import create_test_license_key
from test.data.localizer_data import create_localizer_data
from test.data.geoip_data import download_geoip_database
from test.data.socket_data import create_socket_test_data
from test.data.vfs_data import create_vfs_data
from test.data.pwdlist_data import create_common_pwd_list
from test.data.certificate_data import create_certificate_data
from test.data.rsa_data import create_rsa_data
from test.data.secrets_data import create_secrets_data
from test.data.systemlocator_data import create_systemlocator_data
from test.data.protocol_compiler_data import create_protocol_compiler_data
from test.data.securetarfile_data import create_securetarfile_data
from test.data.vfsconfigurationsource_data import create_vfsconfigurationsource_data
from test.data.configuration_data import create_configuration_data
from test.data.grpcserver_data import create_grpc_data

# Contains the list of callback functions to call when creating the test data
# for a test run.
SESSION_INIT_FUNCTIONS = \
[
    create_application_data,
    create_test_license_key,
    create_localizer_data,
    download_geoip_database,
    create_socket_test_data,
    create_vfs_data,
    create_common_pwd_list,
    create_certificate_data,
    create_rsa_data,
    create_secrets_data,
    create_systemlocator_data,
    create_protocol_compiler_data,
    create_securetarfile_data,
    create_vfsconfigurationsource_data,
    create_configuration_data,
    create_grpc_data
]

# Path to the file that is used to mark that the environment is ready for
# test execution.
READY_MARKER = f'{TEST_FILES_DIRECTORY}/data_ready'

def initialize_test_data():

    """Initializes all test data needed by the test cases.

    This function makes sure that data initialization happens only once.

    Authors:
        Attila Kovacs
    """

    # Try to retrieve the name of the xdist worker. If it was found, it means
    # the test is running with xdist enable, in which case this init code
    # should be only executed once. If running without xdist, the init code can
    # be executed without precautions as the test run is ran by a single
    # process.
    in_init_thread = False
    try:
        current_worker = os.environ['PYTEST_XDIST_WORKER']
        if current_worker == 'gw0':
            in_init_thread = True
    except KeyError:
        in_init_thread = True

    if in_init_thread:

        # Either running in single process mode, or we're inside the process
        # that is supposed to do the initialization

        # Remove data from previous test runs
        if os.path.isdir(TEST_FILES_DIRECTORY):
            shutil.rmtree(TEST_FILES_DIRECTORY)

        # Create the test directory
        os.mkdir(TEST_FILES_DIRECTORY)

        # Execute all initialization functions
        for session_init_function in SESSION_INIT_FUNCTIONS:
            session_init_function()

        # Create the ready marker for the other processes
        with open(READY_MARKER, 'w'):
            pass

    else:

        # Running in a non-initializer thread, wait for test data to be
        # created
        data_available = False
        while not data_available:
            time.sleep(1)
            if os.path.isfile(READY_MARKER):
                data_available = True
