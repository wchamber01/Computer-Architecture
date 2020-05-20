#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

try:
    cpu.load(sys.argv[1])
except:
    sys.exit("An exception occurred")

cpu.run()
