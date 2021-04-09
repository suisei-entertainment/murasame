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
Contains the implementation of the VFSPackage class.
"""

# Murasame Imports
from murasame.logging import LogWriter

class VFSPackage(LogWriter):

    """
    Represents a single VFS resource package.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new VFSPackage instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.pal.vfs', cache_entries=True)
