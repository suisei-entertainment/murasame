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
Contains the unit tests of HostOS class.
"""

# Runtime Imports
import os
import sys
import platform

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.pal.host.hostos import HostOS

class TestHostOS:

    """
    Contains the unit tests of HostOS class.
    """

    def test_creation(self):

        """
        Tests that a HostOS instance can be created.
        """

        sut = HostOS()
        assert sut.Platform == platform.platform()
        assert sut.Name == platform.system()
        assert sut.Release == platform.release()
        assert sut.Version == platform.version()

        if platform.system().lower() == 'linux':
            assert sut.Distribution is not None
        else:
            assert sut.Distribution is None
