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
Contains the unit tests of the LogWriter class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import SystemLocator
from murasame.logging import LogLevels, LoggingAPI, LogWriter

class LoggingSystemTester:
    def __init__(self):
        SystemLocator.instance().register_provider(LoggingAPI, self)
    def get_channel(self, name):
        return self
    @property
    def DefaultLogLevel(self):
        return LogLevels.INFO
    def write(self, entry):
        return

class TestLogWriter:

    """
    Contains all unit tests of the LogWriter class.
    """

    def test_creation(self):

        """
        Tests that a log writer can be created.
        """

        # STEP #1 - Log writer can be created without a logging service if
        #           caching is enabled
        sut = LogWriter(channel_name='test', cache_entries=True)
        assert sut.LogLevel == LogLevels.DEBUG

        # STEP #2 - Log writer can be created without a logging service if
        #           caching is not enabled
        sut = LogWriter(channel_name='test', cache_entries=False)
        assert sut.LogLevel == LogLevels.DEBUG

        # STEP #3 - Log writer can be created if there is a logging service
        system = LoggingSystemTester()
        sut = LogWriter(channel_name='test')
        assert sut.LogLevel == LogLevels.INFO
        SystemLocator.instance().reset()

    def test_log_level_overwrite(self):

        """
        Tests that log levels can be overwritten in the log writer.
        """

        # STEP #1 - Log level can be overwritten.
        sut = LogWriter(channel_name='test', cache_entries=False)
        assert sut.LogLevel == LogLevels.DEBUG
        sut.overwrite_log_level(new_log_level=LogLevels.WARNING)
        assert sut.LogLevel == LogLevels.WARNING
        assert sut.IsLogLevelOverwritten

        # STEP #2 - Log level overwrite can be disabled
        sut.reset_log_level()
        assert sut.LogLevel, LogLevels.INFO
        assert not sut.IsLogLevelOverwritten

        # STEP #3 - Log level can be reset when there is a channel attached
        system = LoggingSystemTester()
        sut = LogWriter(channel_name='test')
        sut.overwrite_log_level(LogLevels.EMERGENCY)
        assert sut.LogLevel == LogLevels.EMERGENCY
        sut.reset_log_level()
        assert sut.LogLevel == LogLevels.INFO
        SystemLocator.instance().reset()

    def test_trace_message(self):

        """
        Tests that TRACE level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is TRACE
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.TRACE)
        sut.trace(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is not writen if log level is above TRACE
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.trace(message='test')
        assert not sut.CachedLogEntries

        # STEP #3 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.TRACE)
        sut.suspend_logging()
        sut.trace(message='test')
        assert not sut.CachedLogEntries

    def test_debug_message(self):

        """
        Tests that DEBUG level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is DEBUG
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.debug(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is not writen if log level is above DEBUG
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.INFO)
        sut.debug(message='test')
        assert not sut.CachedLogEntries

        # STEP #3 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.debug(message='test')
        assert not sut.CachedLogEntries

    def test_info_message(self):

        """
        Tests that INFO level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below INFO
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.info(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is INFO
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.INFO)
        sut.info(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above INFO
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.info(message='test')
        assert not sut.CachedLogEntries

        # STEP #4 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.info(message='test')
        assert not sut.CachedLogEntries

    def test_notice_message(self):

        """
        Tests that NOTICE level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below NOTICE
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.notice(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is NOTICE
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.NOTICE)
        sut.notice(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above NOTICE
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.notice(message='test')
        assert not sut.CachedLogEntries

        # STEP #4 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.notice(message='test')
        assert not sut.CachedLogEntries

    def test_warning_message(self):

        """
        Tests that NOTICE level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below WARNING
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.warning(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is WARNING
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.WARNING)
        sut.warning(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above WARNING
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.warning(message='test')
        assert not sut.CachedLogEntries

        # STEP #4 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.warning(message='test')
        assert not sut.CachedLogEntries

    def test_error_message(self):

        """
        Tests that ERROR level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below ERROR
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.error(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is ERROR
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.ERROR)
        sut.error(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above ERROR
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.error(message='test')
        assert not sut.CachedLogEntries

        # STEP #5 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.error(message='test')
        assert not sut.CachedLogEntries

    def test_critical_message(self):

        """
        Tests that CRITICAL level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below CRITICAL
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.critical(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is CRITICAL
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.CRITICAL)
        sut.critical(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above CRITICAL
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.critical(message='test')
        assert not sut.CachedLogEntries

        # STEP #4 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.critical(message='test')
        assert not sut.CachedLogEntries

    def test_alert_message(self):

        """
        Tests that ALERT level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below ALERT
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.alert(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is ALERT
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.ALERT)
        sut.alert(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if log level is above ALERT
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.alert(message='test')
        assert not sut.CachedLogEntries

        # STEP #4 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.alert(message='test')
        assert not sut.CachedLogEntries

    def test_emergency_message(self):

        """
        Tests that EMERGENCY level messages are handled correctly.
        """

        # STEP #1 - Message is written if log level is below EMERGENCY
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.emergency(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #2 - Message is written if log level is EMERGENCY
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.EMERGENCY)
        sut.emergency(message='test')
        assert sut.CachedLogEntries[0].Message == 'test'

        # STEP #3 - Message is not writen if logging has been suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.overwrite_log_level(new_log_level=LogLevels.DEBUG)
        sut.suspend_logging()
        sut.emergency(message='test')
        assert not sut.CachedLogEntries

    def test_logging_suspension(self):

        """
        Tests that logging can be suspended and resumed.
        """

        # STEP #1 - Logging can be suspended
        sut = LogWriter(channel_name='test', cache_entries=True)
        sut.suspend_logging()
        assert sut.IsLoggingSuspended

        # STEP #2 - Logging can be resumed
        sut.resume_logging()
        assert not sut.IsLoggingSuspended
