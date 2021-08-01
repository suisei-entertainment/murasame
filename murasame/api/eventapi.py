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
Contains the definition of the EventAPI.
"""

# Runtime Imports
from abc import ABC, abstractmethod
from typing import Callable

class EventAPI(ABC):

    """System definition for the event system.

    Authors:
        Attila Kovacs
    """

    @abstractmethod
    def get_num_handlers_for_event(self, event_name: str) -> int:

        """Returns the amount of registered handlers for a given event.

        Args:
            event_name (str): Name of the event to check.

        Returns:
            (int): The amount of event handlers for the given event.

        Authors:
            Attila Kovacs
        """

        del event_name

    @abstractmethod
    def has_event(self, event_name: str) -> bool:

        """Returns whether or not a given event is already registered.

        Args:
            event_name (str): The name of the event to check.

        Returns:
            bool: 'True' if the given event is already registered, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        del event_name
        return  False

    @abstractmethod
    def subscribe(
        self,
        event_name: str,
        cb_handler_function: Callable) -> None:

        """Registers a new event handler for the given event.

        Args:
            event_name (str): Name of the event to register to.

            cb_handler_function (Callable): Callback function that should be
                called when the event is triggered.

        Authors:
            Attila Kovacs
        """

        del event_name
        del cb_handler_function

    @abstractmethod
    def unsubscribe(
        self,
        event_name: str,
        cb_handler_function: Callable) -> None:

        """Unregisters an event handler.

        Args:
            event_name (str): Name of the event to unregister from.
            cb_handler_function (Callable): Callback function to unregister.

        Authors:
            Attila Kovacs
        """

        del event_name
        del cb_handler_function

    @abstractmethod
    def send_event(self, event_name: str, *args, **kwargs) -> None:

        """Sends an event to all subscribers.

        Args:
            event_name (str): The name of the event to send.

            *args (list): List of optional arguments to pass to the event
                handlers.

            **kwargs (dict): List of optional arguments to pass to the event
                handlers.

        Authors:
            Attila Kovacs
        """

        del event_name
        del args
        del kwargs
