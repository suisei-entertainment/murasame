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
Contains the test data for the application tests.
"""

# Runtime Imports
import os
from string import Template

# Test Imports
from test.constants import SHEBANG_STRING, TEST_FILES_DIRECTORY

TEST_DAEMON = \
"""
$shebang

import os
import sys
import time

# Fix paths to make framework modules accessible without installation
sys.path.insert(0, '$framework_dir')

from murasame.application import Application, BusinessLogic
from murasame.log import LogLevels

TEST_FILE_1 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest1.txt'))
TEST_FILE_2 = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon/daemontest2.txt'))

class TestDaemon(BusinessLogic):

    @property
    def WorkingDirectory(self):
        return os.path.abspath(os.path.expanduser('~/.murasame/testfiles/daemon'))

    def main_loop(*argc, **argv):
        with open(TEST_FILE_1, 'w') as file:
            file.write('test')

if __name__ == '__main__':
    print('Creating application...')
    app = Application(business_logic=TestDaemon())
    app.overwrite_log_level(new_log_level=LogLevels.DEBUG)
    print('Starting application...')
    for entry in app._cache:
        print(entry.Message)
    app.start()
    print('Stopping application...')
    for entry in app._cache:
        print(entry.Message)
    app.stop()
    print('Restarting application...')
    for entry in app._cache:
        print(entry.Message)
    app.restart()
    print('Application logs:')
    for entry in app._cache:
        print(entry.Message)
"""

TEST_DAEMON = Template(TEST_DAEMON).substitute(
    shebang=SHEBANG_STRING,
    framework_dir=os.path.abspath(os.path.expanduser('../..')))

def create_application_data():

    """
    Creates data needed for application testing.

    Authors:
        Attila Kovacs
    """

    if not os.path.isdir(f'{TEST_FILES_DIRECTORY}/apptest'):
        os.mkdir(f'{TEST_FILES_DIRECTORY}/apptest')

    if not os.path.isdir(f'{TEST_FILES_DIRECTORY}/apptest/config'):
        os.mkdir(f'{TEST_FILES_DIRECTORY}/apptest/config')

    if not os.path.isdir(f'{TEST_FILES_DIRECTORY}/apptest2'):
        os.mkdir(f'{TEST_FILES_DIRECTORY}/apptest2')

    daemon_dir = f'{TEST_FILES_DIRECTORY}/daemon'

    if not os.path.isdir(daemon_dir):
        os.mkdir(daemon_dir)
    else:
        if os.path.isfile(f'{daemon_dir}/daemontest1.txt'):
            os.remove(f'{daemon_dir}/daemontest1.txt')

    if not os.path.isdir(f'{daemon_dir}/config'):
        os.mkdir(f'{daemon_dir}/config')

    with open(f'{daemon_dir}/daemon.py', 'w') as file:
        file.write(TEST_DAEMON)
        os.chmod(f'{daemon_dir}/daemon.py', 0o777)
