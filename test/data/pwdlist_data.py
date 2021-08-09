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
Contains the test data for the password tests.
"""

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

COMMON_PASSWORD_LIST_PATH = f'{TEST_FILES_DIRECTORY}/commonpwd.txt'
COMMON_PASSWORD_LIST = "password1\npassword2\npassword3"

def create_common_pwd_list():
    with open(COMMON_PASSWORD_LIST_PATH, 'w') as pwd_file:
        pwd_file.write(COMMON_PASSWORD_LIST)