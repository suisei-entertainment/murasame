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
Contains the unit tests of HostDistribution class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.hostdistribution import HostDistribution

class TestHostDistribution:

    """Contains the unit tests of HostDistribution class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a HostDistribution instance can be created.

        Authors:
            Attila Kovacs
        """

        sut = HostDistribution()
        assert sut.ID == 'ubuntu'
        assert sut.Name == 'Ubuntu'
        assert sut.FullName.startswith('Ubuntu 18.04') \
               or sut.FullName.startswith('Ubuntu 19.04') \
               or sut.FullName.startswith('Ubuntu 20.04')
        assert sut.MajorVersion in (18, 19, 20)
        assert sut.MinorVersion == 4
        assert sut.BuildNumber == -1
        assert sut.VersionString in ('18.04', '19.04', '20.04')
        assert sut.Codename.lower() in ('bionic', 'disco', 'focal')
        assert sut.Like == 'debian'
