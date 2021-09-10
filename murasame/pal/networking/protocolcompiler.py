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
Contains the implementation of the ProtocolCompiler class.
"""

# Runtime Imports
import os

# Dependency Imports
from grpc_tools import protoc

# Murasame Imports
from murasame.constants import MURASAME_GRPC_LOG_CHANNEL
from murasame.api import VFSAPI
from murasame.log import LogWriter
from murasame.utils import SystemLocator

class ProtocolCompiler(LogWriter):

    """Utility class that can compile proto files in a VFS directory.

    The compiler will take all proto files from the VFS node and compile them.
    The resulting Python files will be saved in the output directory.

    Attributes:

        _path (str): The path to the directory where the proto files are
            located.

        _output_path (output_path): Path to a real directory in the file
            system where the generated Python code is saved.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """The path to the VFS directory containing the proto files.

        Authors:
            Attila Kovacs
        """

        return  self._path

    @property
    def IncludePath(self) -> str:

        """Path to the include directory in the filesystem containing all files
        required during compilation.

        Authors:
            Attila Kovacs
        """

        return self._include_path

    @property
    def OutputPath(self) -> str:

        """Path to a directory in the file system where the generated code will
        be saved.

        Authors:
            Attila Kovacs
        """

        return  self._output_path

    def __init__(
        self,
        path: str,
        output_path: str,
        include_path: str = None) -> None:

        """Creates a new ProtocolCompiler instance.

        Args:
            path (str): The path to the VFS directory containing the proto
                files.

            output_path (path): Path to a directory in the file system where
                the generated code will be saved.

            include_path (str): Path to a file system directory containing
                include files that are required during compilation.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_GRPC_LOG_CHANNEL,
                         cache_entries=True)

        self._path = path
        self._include_path = include_path
        self._output_path = output_path

    def compile(self) -> bool:

        """Compiles all proto files in the source directory.

        Returns:
            bool: 'True' if the compilation was successful, 'False' otherwise.

        Raises:
            InvalidInputError: Raised when no VFS provider can be retrieved.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Compiling protocol files from VFS directory '
                   f'{self._path}.')

        # Pylint doesn't recognize the instance() member of Singleton
        #pylint: disable=no-member

        vfs = SystemLocator.instance().get_provider(VFSAPI)

        if not vfs:
            self.error('Failed to retrieve a VFS provider.')
            raise RuntimeError('Failed to retrieve a VFS provider.')

        file_list = vfs.get_all_files(node_name=self._path,
                                      filename_filter='.proto')

        result = True
        for file in file_list:

            # Get the directory of the file we're compiling. It needs to be
            # added as an include directory if it's not specified as include
            # directory already.
            file_directory = os.path.dirname(file.Latest.Descriptor.Path)

            # Compile the file
            if self._include_path is None \
                or self._include_path == file_directory:
                if protoc.main((
                    '',
                    f'-I{file_directory}',
                    f'--python_out={self._output_path}',
                    f'--grpc_python_out={self._output_path}',
                    f'{file.Latest.Descriptor.Path}')) != 0:
                    self.error(f'Failed to compile proto file {file}.')
                    result = False
            else:
                if protoc.main((
                    '',
                    f'-I{file_directory}',
                    f'-I{self._include_path}',
                    f'--python_out={self._output_path}',
                    f'--grpc_python_out={self._output_path}',
                    f'{file.Latest.Descriptor.Path}')) != 0:
                    self.error(f'Failed to compile proto file {file}.')
                    result = False

        return result
