#!/usr/bin/python
from iso_checksum import *

import sys


class Srec:

    def __init__(self):
        pass

    def read_line(self, line):
        if line[0:2] == 'S3':
            length = int(line[2:4], 16)
            address = int(line[4:12], 16)
            last_address = address
            bytes = []
            for i in range(length - 5):
                bytes.append(line[12+i*2:12+i*2+2])
                last_address += 1
            checksum = int(line[4+length*2-4:], 16)
            return {'start':address, 'end':last_address - 1, 'data':bytes, 'checksum':checksum}
        else:
            return None
          

calc = ISOcal()

if len(sys.argv) < 2:
    print 'Usage:', sys.argv[0], '<input file>'
    sys.exit(-1)


f = open (sys.argv[1])

first_line = True

s = Srec()

check = -1
iso = ISOcal()
first = True
start = 0
end   = 0

for line in f:

    rec = s.read_line(line.strip())

    if rec:

        if first:
            start = rec['start']

        if check != rec['start'] and not first:
           print 'Start address = %(s)08X, End address = %(e)08X, xs = %(x)04X' % {'s':start, 'e':end,'x': int(iso.calculate(),16) }
           iso.initialise()
           start = rec['start']
        first = False
        for d in rec['data']:
            iso.process_octet(d)
        end = rec['end']
        check = rec['end'] + 1             

print 'Start address = %(s)08X, End address = %(e)08X, xs = %(x)04X' % {'s':start, 'e':end,'x': int(iso.calculate(),16) }

f.close()

