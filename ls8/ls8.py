#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# if sys.argv[1] is None:
#     print(sys.argv)
#     print('error')
#     sys.exit(1)
cpu.load(sys.argv[1])
cpu.run()
