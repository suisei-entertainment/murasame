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
Contains the unit tests of HostPython class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.pal.host.hostpython import HostPython

class TestHostPython:

    """
    Contains the unit tests of HostPython class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a HostPython instance can be created.

        Authors:
            Attila Kovacs
        """

        sut = HostPython()
        assert sut.MajorVersion == sys.version_info.major
        assert sut.MinorVersion == sys.version_info.minor
        assert sut.PatchLevel == sys.version_info.micro
        assert sut.PythonVersion == '{}.{}.{}'.format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro)
        assert sut.Location == sys.executable

    def test_virtualenv_detection(self):

        """
        Tests that detecting virtualenv is working.

        This testcase assumes that tests are always executed in a virtualenv
        environment.

        Authors:
            Attila Kovacs
        """

        sut = HostPython()
        assert sut.is_virtual_env()
