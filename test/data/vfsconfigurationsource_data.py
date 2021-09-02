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
Contains the test data for the VFSConfigurationSource tests.
"""

# Runtime Imports
import os
import json

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

SOURCE_DIRECTORY = f'{TEST_FILES_DIRECTORY}/vfsconfigurationsource'
CONFIG_DIRECTORY = f'{SOURCE_DIRECTORY}/config'
CONFIG_FILE = f'{CONFIG_DIRECTORY}/testconfig.conf'
INVALID_CONFIG_DIRECTORY = f'{SOURCE_DIRECTORY}/invalidconfig'
INVALID_CONFIG_FILE = f'{INVALID_CONFIG_DIRECTORY}/testconfig.conf'

CONFIG_DATA = \
{
    'testgroup':
    {
        'testgroup2':
        {
            'testattribute1': 1
        },
        'testattribute2': 2,
        'testlist': [1,2,3]
    }
}

INVALID_CONFIG_DATA = \
{
    "testdata": 1
}

def create_vfsconfigurationsource_data() -> None:

    # Create directories
    if not os.path.isdir(SOURCE_DIRECTORY):
        os.mkdir(SOURCE_DIRECTORY)
        os.mkdir(CONFIG_DIRECTORY)
        os.mkdir(INVALID_CONFIG_DIRECTORY)

    # Create files
    with open(CONFIG_FILE, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(CONFIG_DATA))

    with open(INVALID_CONFIG_FILE, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(INVALID_CONFIG_DATA))