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
Contains the unit tests for the EventSystem class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.api import EventAPI
from murasame.event import EventSystem

def cb_handler(*args, **kwargs):
    return

def cb_handler2(*args, **kwargs):
    return

def cb_handler3(*args, **kwargs):
    raise RuntimeError

class TestEventSystem:

    """Contains the unit tests of the EventSystem class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """Tests that the EventSystem can be created.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        assert sut is not None

    def test_subscribing_to_new_event(self):

        """Tests that it's possible to subscribe to a new event.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        assert sut.NumEvents == 0
        sut.subscribe('testevent', cb_handler)
        assert sut.NumEvents == 1
        assert sut.get_num_handlers_for_event('testevent') == 1

    def test_subscribing_to_existing_event(self):

        """Tests that it's possible to subscribe to an existing event.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        sut.subscribe('testevent', cb_handler)
        sut.subscribe('testevent', cb_handler2)
        assert sut.NumEvents == 1
        assert sut.get_num_handlers_for_event('testevent') == 2

    def test_unsubscribing_from_existing_event(self):

        """Tests that it's possible to subscribe from an existing event.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        sut.subscribe('testevent', cb_handler)
        sut.subscribe('testevent', cb_handler2)
        assert sut.get_num_handlers_for_event('testevent') == 2
        sut.unsubscribe('testevent', cb_handler)
        assert sut.get_num_handlers_for_event('testevent') == 1

    def test_unsubscribing_from_existing_event_with_last_handler(self):

        """Tests that when the last event handler is unsubscribed, the event is
        removed as well.

        Authors
            Attila Kovacs
        """

        sut = EventSystem()
        sut.subscribe('testevent', cb_handler)
        sut.subscribe('testevent', cb_handler2)
        sut.unsubscribe('testevent', cb_handler)
        sut.unsubscribe('testevent', cb_handler2)
        assert sut.get_num_handlers_for_event('testevent') == 0

    def test_unsubscribing_from_non_existing_event(self):

        """Tests that unsubscribing from a non-existing event is handled.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        sut.subscribe('testevent', cb_handler)
        sut.unsubscribe('testevent2', cb_handler)

    def test_sending_event_without_handlers(self):

        """Tests that events can be sent when there are no handlers registered.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        sut.send_event('testevent')

    def test_sending_event_with_handlers(self):

        """Tests that events can be sent when there are registered handlers.

        Authors:
            Attila Kovacs
        """

        sut = EventSystem()
        sut.subscribe('testevent', cb_handler3)

        with pytest.raises(RuntimeError):
            sut.send_event('testevent')