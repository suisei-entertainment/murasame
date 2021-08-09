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
Contains the data used for secrets testing.
"""

# Runtime Imports
import os

# Murasame Imports
from murasame.utils import JsonFile

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

TEST_PASSWORD = 'testpassword'

def get_password():
    return TEST_PASSWORD

TEST_DATA = \
{
    'testkey': 'testvalue'
}

def create_secrets_data():

    # Create the test file
    config_file = JsonFile(
        path=f'{TEST_FILES_DIRECTORY}/secrets.conf',
        cb_retrieve_key=get_password)
    config_file.overwrite_content(content=TEST_DATA)
    config_file.save()