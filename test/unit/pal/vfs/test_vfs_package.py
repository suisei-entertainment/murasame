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
Contains the unit tests of the VFSPackage class.
"""

# Runtime Imports
import os
import sys
import tarfile
import json
from pathlib import Path

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.api import VFSAPI
from murasame.pal.vfs.vfspackage import VFSPackage
from murasame.pal.vfs.vfs import VFS
from murasame.utils import SystemLocator

TEST_PACKAGE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfspackage.pkg'))

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

class TestPackage:

    """
    Contains the unit tests for the VFSPackage class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

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

        # Setup VFS
        SystemLocator.instance().register_provider(VFSAPI, VFS())

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(TEST_PACKAGE_PATH):
            os.remove(TEST_PACKAGE_PATH)

        SystemLocator.instance().reset()

    def test_creation(self):

        """
        Tests that a VFSPackage object can be created.

        Authors:
            Attila Kovacs
        """

        sut = VFSPackage(path=TEST_PACKAGE_PATH)
        assert sut is not None
        assert sut.Path == TEST_PACKAGE_PATH

    def test_package_loading(self):

        """
        Tests that a VFSPackage loads correctly from file.

        Authors:
            Attila Kovacs
        """

        vfs = SystemLocator.instance().get_provider(VFSAPI)

        sut = VFSPackage(path=TEST_PACKAGE_PATH)
        assert vfs.has_node('/directory1')
        assert vfs.has_node('/directory2')
        assert vfs.has_node('/directory1/file1.txt')
        assert vfs.has_node('/directory2/file2.txt')
        assert vfs.get_node('/directory1/file1.txt').Latest.Descriptor.PackagePath == TEST_PACKAGE_PATH
        assert vfs.get_node('/directory2/file2.txt').Latest.Descriptor.PackagePath == TEST_PACKAGE_PATH
