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
Contains the implementation of the event system.
"""

# Runtime Imports
from typing import Callable

# Murasame Imports
from murasame.constants import MURASAME_EVENT_LOG_CHANNEL
from murasame.log.logwriter import LogWriter

class EventSystem(LogWriter):

    """Implementation of a simple event system.

    Attributes:
        _events (dict): The events currently registered in the event system.

    Authors:
        Attila Kovacs
    """

    @property
    def NumEvents(self) -> int:

        """The amount of events currently registered.

        Authors:
            Attila Kovacs
        """

        return  len(self._events)

    def __init__(self) -> None:

        """
        Creates a new EventSystem instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_EVENT_LOG_CHANNEL,
                         cache_entries=True)

        self._events = {}

    def get_num_handlers_for_event(self, event_name: str) -> int:

        """Returns the amount of registered handlers for a given event.

        Args:
            event_name (str): Name of the event to check.

        Returns:
            (int): The amount of event handlers for the given event.

        Authors:
            Attila Kovacs
        """

        if not self.has_event(event_name=event_name):
            return 0

        return len(self._events[event_name])

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

        if event_name in self._events:
            return True

        return  False

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

        self.debug(f'Subscribing to event {event_name}...')

        # Create a new event handler list if the event is not yet subscribed to
        if not self.has_event(event_name):
            self._events[event_name] = []
            self.debug(f'Event {event_name} has no subscribers yet, creating '
                       f'event in the event system.')

        # Add the handler to the handler list
        self._events[event_name].append(cb_handler_function)
        self.debug(f'Subscribed to {event_name}.')

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

        self.debug(f'Unsubscribing from {event_name}...')

        if not self.has_event(event_name):
            self.debug(f'Event {event_name} doesn\'t exist, nothing to do.')
            return

        handlers = self._events[event_name]
        handlers.remove(cb_handler_function)

        if len(handlers) == 0:
            self.debug(f'No handlers left for event {event_name}, removing '
                       f'the event.')
            del self._events[event_name]

        self.debug(f'Unsubscribed from {event_name}.')

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

        self.debug(f'Sending event {event_name} with parameters: '
                   f'{args} {kwargs}.')

        if not self.has_event(event_name):
            self.debug(f'Event {event_name} has no subscribers yet, nothing '
                       f'to do.')
            return

        handlers = self._events[event_name]
        self.debug(f'Sending event {event_name} to {len(handlers)} '
                   f'handlers.')
        for handler in handlers:
            handler(args, kwargs)

        self.debug(f'Event {event_name} was sent.')
