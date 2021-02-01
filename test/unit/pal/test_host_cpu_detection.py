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
Contains the unit tests of HostCPU class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.hostcpu import HostCPU

# Test data
TEST_DATA = \
{
    'python_version': '3.7.1.final.0 (64 bit)',
    'cpuinfo_version': (4, 0, 0),
    'arch': 'X86_64',
    'bits': 64,
    'count': 16,
    'raw_arch_string': 'x86_64',
    'vendor_id': 'GenuineIntel',
    'brand': 'Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz',
    'hz_advertised': '2.6000 GHz',
    'hz_actual': '2.6000 GHz',
    'hz_advertised_raw': (2600000000, 0),
    'hz_actual_raw': (2600000000, 0),
    'stepping': 7,
    'model': 45,
    'family': 6,
    'flags':
    [   'aes',
        'aperfmperf',
        'apic',
        'arat',
        'arch_perfmon',
        'avx',
        'bts',
        'clflush',
        'cmov',
        'constant_tsc',
        'cpuid',
        'cx16',
        'cx8',
        'de',
        'dtherm',
        'dts',
        'epb',
        'fpu',
        'fxsr',
        'ht',
        'hypervisor',
        'ida',
        'lahf_lm',
        'lm',
        'mca',
        'mce',
        'mmx',
        'msr',
        'mtrr',
        'nonstop_tsc',
        'nopl',
        'nx',
        'osxsave',
        'pae',
        'pat',
        'pcid',
        'pclmulqdq',
        'pebs',
        'pge',
        'pln',
        'pni',
        'popcnt',
        'pse',
        'pse36',
        'pti',
        'pts',
        'rdtscp',
        'sep',
        'ss',
        'sse',
        'sse2',
        'sse4_1',
        'sse4_2',
        'ssse3',
        'syscall',
        'tsc',
        'tsc_adjust',
        'tsc_deadline_timer',
        'tsc_reliable',
        'tscdeadline',
        'vme',
        'x2apic',
        'xsave',
        'xtopology'
    ],
    'l3_cache_size': '20480 KB',
    'l2_cache_size': '256 KB',
    'l1_data_cache_size': '32 KB',
    'l1_instruction_cache_size': '32 KB',
    'l2_cache_line_size': 6,
    'l2_cache_associativity': '0x100',
    'extended_model': 2
}

class TestCPUDetection:

    """
    Contains the unit tests of HostCPU class.
    """

    def test_creation(self):

        """
        Tests that the HostCPU object can be created without errors.
        """

        sut = HostCPU()

    def test_architecture_detection(self):

        """
        Tests that the host CPU architecture can be detected correctly.
        """

        # STEP #1 - Normal detection through cpuinfo
        sut = HostCPU()
        sut._detect_architecture(TEST_DATA)
        assert sut.Architecture in ('X86_64', 'AARCH64')

        # STEP #2 - Fallback detection through platform
        sut = HostCPU()
        sut._detect_architecture({})
        assert sut.Architecture in ('X86_64', 'AARCH64')

    def test_cpu_count_detection(self):

        """
        Tests that the amount of CPU cores can be detected correctly.
        """

        # STEP #1 - Normal detection through cpuinfo
        sut = HostCPU()
        sut._detect_cpu_count(TEST_DATA)
        assert sut.NumCores == 16
        assert sut.NumPhysicalCores != -1

        # STEP #2 - Fallback detection through multiprocessing
        sut = HostCPU()
        sut._detect_cpu_count({})
        assert sut.NumCores != -1
        assert sut.NumPhysicalCores != -1

    def test_cpu_type_detection(self):

        """
        Tests that the CPU type can be detected correctly.
        """

        # STEP #1 - Normal detection through cpuinfo
        sut = HostCPU()
        sut._detect_cpu_type(TEST_DATA)
        assert sut.VendorID == 'GenuineIntel'
        assert sut.Name == 'Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz'
        assert sut.Stepping == 7
        assert sut.Model == 45
        assert sut.ExtendedModel == 2
        assert sut.Family == 6

        # STEP #2 - Missing cpuinfo data
        sut = HostCPU()
        sut._detect_cpu_type({})
        assert sut.VendorID == 'UNKNOWN'
        assert sut.Name == 'UNKNOWN'
        assert sut.Stepping == -1
        assert sut.Model == -1
        assert sut.ExtendedModel == -1
        assert sut.Family == -1

    def test_cpu_speed_detection(self):

        """
        Tests that the CPU speed can be detected correctly.
        """

        # STEP #1 - Normal detection through cpuinfo
        sut = HostCPU()
        sut._detect_cpu_speed(TEST_DATA)
        assert sut.MaxSpeed == '2.6000 GHz'

        # STEP #2 - Detection with empty cpuinfo
        sut = HostCPU()
        sut._detect_cpu_speed({})
        assert sut.MaxSpeed == 'UNKNOWN'

    def test_cpu_cache_detection(self):

        """
        Tests that the CPU cache size can be detected correctly.
        """

        # STEP #1 - Normal detection through cpuinfo
        sut = HostCPU()
        sut._detect_cache_data(TEST_DATA)
        assert sut.L2CacheSize == '256 KB'

        # STEP #2 - Detection with empty cpuinfo
        sut = HostCPU()
        sut._detect_cache_data({})
        assert sut.L2CacheSize == 'UNKNOWN'
