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
Contains the implementation of the LogWriter class.
"""

# Runtime Imports
from datetime import datetime

# Murasame Imports
from murasame.utils.systemlocator import SystemLocator
from murasame.log.loglevels import LogLevels
from murasame.log.logentry import LogEntry

class LogWriter:

    """Utility class that represents an object that wants to write into the log.

    Attributes:
        _cache_entries (bool): Whether or not log entries should be cached if
            the log service is unavailable.

        _cache (list): Stores cached log entries until they are sent to the log
            channel after attach.

        _channel_name (str): Name of the channel this writer logs to.

        _log_level (LogLevels): Current log level of the writer.

        _log_level_overwritten (bool): Whether or not the log level has been
            overwritten for this writer.

        _channel (LogChannel): The log channel object to log to.

        _log_writer_suspended (bool): Whether or not the log writer has been
            suspended.

    Authors:
        Attila Kovacs
    """

    @property
    def LogLevel(self) -> LogLevels:

        """The current log level of the writer.

        Authors:
            Attila Kovacs
        """

        return self._log_level

    @property
    def IsLogLevelOverwritten(self) -> bool:

        """Whether or not the log level of the channel this writer logs to has
        been overwritten by the writer.

        Authors:
            Attila Kovacs
        """

        return self._log_level_overwritten

    @property
    def IsLoggingSuspended(self) -> bool:

        """Returns whether or not log has been suspended in this writer.

        Authors:
            Attila Kovacs
        """

        return self._log_writer_suspended

    @property
    def CachedLogEntries(self) -> list:

        """Provides access to the list of cached log entries.

        Authors:
            Attila Kovacs
        """

        return self._cache

    def __init__(self, channel_name: str, cache_entries: bool = False) -> None:

        """Creates a new LogWriter instance.

        Args:
            channel_name (str): Name of the channel this writer logs to.
            cache_entries (bool): Whether or not log entries should be cached
                if the log service is not available.

        Authors:
            Attila Kovacs
        """

        self._cache_entries = cache_entries
        self._cache = []
        self._channel_name = channel_name
        self._log_level = None
        self._log_level_overwritten = False
        self._channel = self._attach()
        self._log_writer_suspended = False

    def overwrite_log_level(self, new_log_level: LogLevels) -> None:

        """Overwrites the log level of the writer.

        Args:
            new_log_level (LogLevels): The new log level that will be used by
                the writer.

        Authors:
            Attila Kovacs
        """

        self._log_level = new_log_level
        self._log_level_overwritten = True

    def reset_log_level(self) -> None:

        """Resets the log level of the writer to the default value set by its
        parent channel.

        Authors:
            Attila Kovacs
        """

        if self._channel:
            self._log_level = self._channel.DefaultLogLevel
        else:
            self._log_level = LogLevels.INFO

        self._log_level_overwritten = False

    def suspend_logging(self) -> None:

        """Suspends all log from this writer.

        Authors:
            Attila Kovacs
        """

        self._log_writer_suspended = True

    def resume_logging(self) -> None:

        """Resumes log from this writer.

        Authors:
            Attila Kovacs
        """

        self._log_writer_suspended = False

    def trace(self, message: str) -> None:

        """Writes a new trace level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level == LogLevels.TRACE:
            entry = self._make_entry(level=LogLevels.TRACE, message=message)
            self._log(entry=entry)

    def debug(self, message: str) -> None:

        """Writes a new debug level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.DEBUG:
            entry = self._make_entry(level=LogLevels.DEBUG, message=message)
            self._log(entry=entry)

    def info(self, message: str) -> None:

        """Writes a new info level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.INFO:
            entry = self._make_entry(level=LogLevels.INFO, message=message)
            self._log(entry=entry)

    def notice(self, message: str) -> None:

        """Writes a new notice level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.NOTICE:
            entry = self._make_entry(level=LogLevels.NOTICE, message=message)
            self._log(entry=entry)

    def warning(self, message: str) -> None:

        """Writes a new warning level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.WARNING:
            entry = self._make_entry(level=LogLevels.WARNING, message=message)
            self._log(entry=entry)

    def error(self, message: str) -> None:

        """Writes a new error level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.ERROR:
            entry = self._make_entry(level=LogLevels.ERROR, message=message)
            self._log(entry=entry)

    def critical(self, message: str) -> None:

        """Writes a new critical level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.CRITICAL:
            entry = self._make_entry(level=LogLevels.CRITICAL, message=message)
            self._log(entry=entry)

    def alert(self, message: str) -> None:

        """Writes a new alert level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        if self._log_level <= LogLevels.ALERT:
            entry = self._make_entry(level=LogLevels.ALERT, message=message)
            self._log(entry=entry)

    def emergency(self, message: str) -> None:

        """Writes a new emergency level log message to the log channel, if the
        configured log level allows it.

        Args:
            message (str): The log message to write.

        Authors:
            Attila Kovacs.
        """

        if self.IsLoggingSuspended:
            return

        entry = self._make_entry(level=LogLevels.EMERGENCY, message=message)
        self._log(entry=entry)

    def _log(self, entry: LogEntry) -> None:

        """Adds a new log entry to the log.

        Args:
            entry (LogEntry): The log entry to add.

        Authors:
            Attila Kovacs
        """

        # Try to attach to the log channel if not already attached
        if not self._channel:
            self._channel = self._attach()

        if self._channel:
            # Empty the cache if there if there are cached entries
            self._flush_cache()
            self._channel.write(entry=entry)
        elif self._cache_entries:
            self._cache_entry(entry=entry)

    def _attach(self) -> 'LogChannel':

        """Attaches this log writer to a log channel the writer needs to write
            to.

        Returns:
            LogChannel: The log channel object that has been attached to.

        Authors:
            Attila Kovacs
        """

        channel = None

        # Pylint cannot find the instance() method of ServiceLocator
        #pylint: disable=no-member

        # Logging API has to be imported here to avoid circular imports
        # pylint: disable=import-outside-toplevel

        # Get the channel based on its name
        from murasame.api import LoggingAPI
        log_system= SystemLocator.instance().get_provider(LoggingAPI)

        if log_system:
            channel = log_system.get_channel(self._channel_name)

            if not channel:
                self._log_level = LogLevels.INFO
                return None

            self._log_level = channel.DefaultLogLevel
        else:
            self._log_level = LogLevels.INFO

        return channel

    def _make_entry(self, level: LogLevels, message: str) -> LogEntry:

        """Creates a new log entry.

        Args:
            level (LogLevels): The log level the message was sent with.

            message (str): The log message.

        Authors:
            Attila Kovacs
        """

        return LogEntry(level=level,
                        timestamp=datetime.utcnow(),
                        message=message,
                        classname=self.__class__.__name__)

    def _cache_entry(self, entry: LogEntry) -> None:

        """Adds a new entry to the log cache.

        Args:
            entry (LogEntry): The log entry to cache.

        Authors:
            Attila Kovacs
        """

        self._cache.append(entry)

    def _flush_cache(self) -> None:

        """Sends all cached log entries to the channel.

        Authors:
            Attila Kovacs
        """

        for entry in self._cache:
            self._channel.write(entry)
        self._cache.clear()
