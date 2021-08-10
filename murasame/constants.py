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
Contains constants used by the entire framework.
"""

# Runtime Imports
import os

## ============================================================================
##  DEFAULT DIRECTORIES
## ============================================================================

# The default VFS directory containing the language files
MURASAME_DEFAULT_LOCALIZATION_PATH = '/localization'

## ============================================================================
##  LOG CHANNELS
## ============================================================================

# List of log channels used by the framework

MURASAME_APPLICATION_LOG_CHANNEL = 'murasame.application'

MURASAME_CONFIGURATION_LOG_CHANNEL = 'murasame.configuration'

MURASAME_DEBUG_LOG_CHANNEL = 'murasame.debug'

MURASAME_EVENT_LOG_CHANNEL = 'murasame.event'

MURASAME_EXCEPTIONS_LOG_CHANNEL = 'murasame.exceptions'

MURASAME_LOCALIZER_LOG_CHANNEL = 'murasame.localizer'

MURASAME_PAL_LOG_CHANNEL = 'murasame.pal'

MURASAME_SOCKET_LOG_CHANNEL = 'murasame.pal.networking.socket'

MURASAME_VFS_LOG_CHANNEL = 'murasame.pal.vfs'

## ============================================================================
##  COMMON CONSTANTS
## ============================================================================

MURASAME_LOGGING_CONFIG = os.path.abspath('./config/log.conf')
