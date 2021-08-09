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
Contains the test data for the VFS tests.
"""

# Runtim Imports
import os
import json
import tarfile

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

JSON_PATH = f'{TEST_FILES_DIRECTORY}/vfstest.json'
YAML_PATH = f'{TEST_FILES_DIRECTORY}/vfstest.yaml'
JSON_CONF_PATH = f'{TEST_FILES_DIRECTORY}/vfstestjson.conf'
YAML_CONF_PATH = f'{TEST_FILES_DIRECTORY}/vfstestyaml.conf'
GENERIC_PATH = f'{TEST_FILES_DIRECTORY}/vfstest.txt'

TEST_PACKAGE_PATH = f'{TEST_FILES_DIRECTORY}/vfspackage.pkg'

PACKAGE_DESCRIPTOR = \
{
    'name': 'ROOT',
    'type': 'directory',
    'subdirectories':
    {
        'directory1':
        {
            'name': 'directory1',
            'type': 'directory',
            'subdirectories': {},
            'files':
            {
                'file1.txt':
                {
                    'name': 'file1.txt',
                    'type': 'packagefile',
                    'resource':
                    [
                        {
                            'version': '1',
                            'descriptor':
                            {
                                'type': 'packagefile',
                                'path': '/directory1/file1.txt',
                                'contenttype': 'text/plain'
                            }
                        }
                    ]
                }
            }
        },
        'directory2':
        {
            'name': 'directory2',
            'type': 'directory',
            'subdirectories': {},
            'files':
            {
                'file2.txt':
                {
                    'name': 'file2.txt',
                    'type': 'packagefile',
                    'resource':
                    [
                        {
                            'version': '1',
                            'descriptor':
                            {
                                'type': 'packagefile',
                                'path': '/directory2/file2.txt',
                                'contenttype': 'text/plain'
                            }
                        }
                    ]
                }
            }
        }
    },
    'files':
    {

    }
}

def create_vfs_data():

    # Create files for VFSLocalFileConnector
    with open(JSON_PATH, 'w') as file:
        file.write('{\"test\": \"value\"}')

    if os.path.isfile(YAML_PATH):
        os.remove(YAML_PATH)

    with open(YAML_PATH, 'w') as file:
        file.write('test: value')

    if os.path.isfile(GENERIC_PATH):
        os.remove(GENERIC_PATH)

    with open(GENERIC_PATH, 'w') as file:
        file.write('test')

    if os.path.isfile(JSON_CONF_PATH):
        os.remove(JSON_CONF_PATH)

    with open(JSON_CONF_PATH, 'w') as file:
        file.write('{\"test\": \"value\"}')

    if os.path.isfile(YAML_CONF_PATH):
        os.remove(YAML_CONF_PATH)

    with open(YAML_CONF_PATH, 'w') as file:
        file.write('test: value')

    # Create files for VFSPackage
    if os.path.isfile(TEST_PACKAGE_PATH):
        os.remove(TEST_PACKAGE_PATH)

    if os.path.isfile('/tmp/packagebuild/.vfs'):
        os.remove('/tmp/packagebuild/.vfs')

    # Create test package files
    if not os.path.isdir('/tmp/packagebuild'):
        os.mkdir('/tmp/packagebuild')

    if not os.path.isdir('/tmp/packagebuild/directory1'):
        os.mkdir('/tmp/packagebuild/directory1')

    if not os.path.isfile('/tmp/packagebuild/directory1/file1.txt'):
        with open('/tmp/packagebuild/directory1/file1.txt', 'w') as file:
            file.write('file1')

    if not os.path.isdir('/tmp/packagebuild/directory2'):
        os.mkdir('/tmp/packagebuild/directory2')

    if not os.path.isfile('/tmp/packagebuild/directory2/file2.txt'):
        with open('/tmp/packagebuild/directory2/file2.txt', 'w') as file:
            file.write('file2')

    if not os.path.isfile('/tmp/packagebuild/.vfs'):
        with open('/tmp/packagebuild/.vfs', 'w') as file:
            json.dump(obj=PACKAGE_DESCRIPTOR, fp=file)

    # Create the package
    current_dir = os.getcwd()
    os.chdir('/tmp/packagebuild')
    with tarfile.open(TEST_PACKAGE_PATH, 'w') as tar:
        tar.add('.vfs')
        tar.add('directory1')
        tar.add('directory1/file1.txt')
        tar.add('directory2')
        tar.add('directory2/file2.txt')
    os.chdir(current_dir)
