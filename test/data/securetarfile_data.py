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
Contains the test data for the SecureTarFile tests.
"""

# Runtime Imports
import os
import tarfile

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

DIR_LEVEL = "../"

def create_securetarfile_data() -> None:

    # Create directory
    tartest_path = f'{TEST_FILES_DIRECTORY}/tartest'
    if not os.path.isdir(tartest_path):
        os.mkdir(tartest_path)

    # Create valid tar file
    with open(f'{tartest_path}/testfile.txt', 'w') as file:
        file.write('test')

    with tarfile.open(f'{tartest_path}/valid.tar.gz', mode='w:gz') as tar:
        tar.add(f'{tartest_path}/testfile.txt')
        tar.close()

    # Create tarbomb
    depth = 3
    payload = f'{tartest_path}/testfile.txt'
    path = tartest_path
    dt_path = f'{DIR_LEVEL*int(depth)}{path}{os.path.basename(payload)}'
    with tarfile.open(f'{tartest_path}/tarbomb.tar.gz', mode='w:gz') as tar:
        tar.add(payload, dt_path)
        tar.close()
