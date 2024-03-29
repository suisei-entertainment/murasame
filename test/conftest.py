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
Contains unit test configuration.
"""

# Runtime Imports
import os
import shutil
import py
import socket

# Dependency Imports
import pytest
from py.xml import html
from xprocess import XProcess

# Test Imports
from test.constants import TEST_FILES_DIRECTORY
from test.testdata import initialize_test_data

def pytest_html_report_title(report):
   report.title = 'Murasame Test Report'

def pytest_sessionstart(session):
   initialize_test_data()

def pytest_sessionfinish(session, exitstatus):

   # Shut down all running XProcess processes
   tw = py.io.TerminalWriter()
   rootdir = session.config.rootdir.join(".xprocess").ensure(dir=1)
   xproc = XProcess(session.config, rootdir)
   xproc._xkill(tw)

   # Kill the socket server if it's still running (e.g. due to the server
   # socket test not running)
   try:
      sock = socket.socket()
      sock.connect(('localhost', 11492))
      message = 'kill' + os.linesep
      sock.sendall(message)
   except socket.error:
      pass
