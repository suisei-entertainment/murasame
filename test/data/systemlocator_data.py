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
Contains the data used for system locator testing.
"""

# Runtime Imports
import os
import sys

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

TEST_SYSTEM = \
"""
from murasame.utils import System, SystemLocator

class AbstractSystem:
    def system_function(self):
        pass

class AnotherAbstractSystem:
    def system_function(self):
        pass

@System(AbstractSystem)
class ConcreteSystem(AbstractSystem):
    def system_function(self):
        return True
"""

SYSTEM_DIR = f'{TEST_FILES_DIRECTORY}/systems/'

def create_systemlocator_data():

    if not os.path.isdir(SYSTEM_DIR):
        os.mkdir(SYSTEM_DIR)

        # Create a test system file
        system_file = f'{SYSTEM_DIR}/testsystem.py'
        with open(system_file, 'w+') as test_file:
            test_file.write(TEST_SYSTEM)

        # Create an __init__.py file
        init_file = f'{SYSTEM_DIR}/__init__.py'
        with open(init_file, 'w+') as test_file:
            test_file.write('\n')