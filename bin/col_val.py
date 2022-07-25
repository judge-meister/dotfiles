#!/usr/bin/env python3

import sys

if len(sys.argv) > 1:
    col = sys.argv[1]
    try:
        for c in col.split(','):
            v = int(c)
            print("%02x" % v, end='')
        print()
    except ValueError:
        # convert hex back to 3 ints
        icol = []
        for i in [2,4,6]:
            icol.append("%d" % int(col[i-2:i], 16) )
        print(','.join(icol))

