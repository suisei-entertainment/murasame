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
Contains the test data for the configuration tests.
"""

# Runtime Imports
import os
import json

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

CONFIG_TEST_DIRECTORY = f'{TEST_FILES_DIRECTORY}/configurationtest'
CONFIG_DIRECTORY = f'{CONFIG_TEST_DIRECTORY}/configuration'
CONFIG_FILE = f'{CONFIG_DIRECTORY}/configuration.conf'

CONFIG_DATA = \
{
    'testgroup1':
    {
        'testgroup2':
        {
            'testattribute2': 'testvalue'
        },
        'testattribute1': 1
    }
}

def create_configuration_data() -> None:

    # Create directories
    if not os.path.isdir(CONFIG_TEST_DIRECTORY):
        os.mkdir(CONFIG_TEST_DIRECTORY)
        os.mkdir(CONFIG_DIRECTORY)

    # Create files
    with open(CONFIG_FILE, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(CONFIG_DATA))