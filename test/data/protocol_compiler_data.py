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
Contains the test data for the protocol compiler tests.
"""

# Runtime Imports
import os

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

PROTOCOL_DIRECTORTY = os.path.abspath(os.path.expanduser(
    f'{TEST_FILES_DIRECTORY}/protocolcompiler'))

PROTOCOL_INPUT_DIRECTORY = f'{PROTOCOL_DIRECTORTY}/input'
PROTOCOL_OUTPUT_DIRECTORY = f'{PROTOCOL_DIRECTORTY}/output'

PROTOCOL_FILE = f'{PROTOCOL_INPUT_DIRECTORY}/testfile.proto'

TEST_PROTOCOL_FILE = \
"""
syntax = "proto3";

package testpackage;

service TestService
{
    rpc TestCall(TestInput) returns (TestReturn) {} 
}

message TestInput
{
    int32 testInt = 1;
    string testString = 2;
}

message TestReturn
{
    string response = 1;
}
"""

def create_protocol_compiler_data():

    # Create directories
    if not os.path.isdir(PROTOCOL_DIRECTORTY):
        os.mkdir(PROTOCOL_DIRECTORTY)
        os.mkdir(PROTOCOL_INPUT_DIRECTORY)
        os.mkdir(PROTOCOL_OUTPUT_DIRECTORY)

    # Create protocol files
    with open(PROTOCOL_FILE, 'w') as file:
        file.write(TEST_PROTOCOL_FILE)
