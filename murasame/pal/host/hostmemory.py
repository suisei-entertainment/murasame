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
Contains the implementation of the HostMemory class.
"""

# Murasame Imports
from murasame.constants import MURASAME_PAL_LOG_CHANNEL
from murasame.log import LogWriter

class HostMemory(LogWriter):

    """Utility class that represents the memory of the host system.

    Attributes:
        _total_ram (str): Total amount of system memory.

    Authors:
        Attila Kovacs
    """

    @property
    def TotalSystemMemory(self) -> str:

        """The total amount of system memory in the host system.

        Authors:
            Attila Kovacs
        """

        return self._total_ram

    def __init__(self) -> None:

        """Creates a new HostMemory instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_PAL_LOG_CHANNEL,
                         cache_entries=True)

        self._total_ram = 0

        self._get_total_ram()

    def _get_total_ram(self) -> None:

        """Retrieves the total amount of RAM available on the host system.

        Authors:
            Attila Kovacs
        """

        try:
            self.debug('Attempting to retrieve the total amount of host '
                       'memory through psutil...')
            # Imported here so detection works even without the package
            # installed.
            #pylint: disable=import-outside-toplevel
            import psutil
            memory = psutil.virtual_memory()
            self._total_ram = memory.total
            self.debug(f'Total amount of memory on the host system: '
                       f'{self._total_ram} MB')
        except ImportError:
            self.warning('The psutil library is not available on the host '
                         'system. Memory information cannot be retrieved.')
            self._total_ram = -1
