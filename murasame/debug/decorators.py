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
Contains the implementation of debug decorators.
"""

# Runtime Imports
from typing import Any, Callable
from time import perf_counter

# Murasame Imports
from murasame.constants import MURASAME_DEBUG_LOG_CHANNEL
from murasame.log import LogWriter

def debug(function: Callable) -> Any:

    """Allows log of a function call with the arguments it was called with.

    Args:
        function (Callable): The function to debug.

    Returns:
        Any: The return value of the wrapped function.

    Authors:
        Attila Kovacs
    """

    def wrapper(*args, **kwargs) -> Any:
        logger = LogWriter(channel_name=MURASAME_DEBUG_LOG_CHANNEL,
                           cache_entries=True)
        logger.debug(f'Calling {function.__name__}')
        logger.debug(f'    - Args: {args}')
        logger.debug(f'    - Kwargs: {kwargs}')
        result = function(*args, **kwargs)
        logger.debug(f'   > Result: {result}')
        return result
    return wrapper

def measure(function: Callable) -> Any:

    """Allows log of the execution time of functions.

    Args:
        *args: Variable argument list.
        **kwargs: Variable length list of named arguments.

    Returns:
        Any: The return value of the wrapped function.

    Authors:
        Attila Kovacs
    """

    def wrapper(*args, **kwargs) -> Any:
        logger = LogWriter(channel_name=MURASAME_DEBUG_LOG_CHANNEL,
                           cache_entries=True)
        start_time = perf_counter()
        result = function(*args, **kwargs)
        end_time = perf_counter()
        duration = (end_time - start_time) * 1000
        logger.debug(f'    -- Execution time: {duration:0.4f} ms.')
        return result
    return wrapper
