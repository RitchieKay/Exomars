#!/usr/bin/python
from iso_checksum import *

import sys

calc = ISOcal()

if len(sys.argv) < 3:
    print 'Usage:', sys.argv[0], '<input file>', '<output file>'
    sys.exit(-1)


f = open (sys.argv[1])
o = open (sys.argv[2], "w")
c = open (sys.argv[2] + '_corrections', 'w')

corrections = 0
patch_commands = 0
xs = 0
in_patch_command = False
command_records = []
first_line = True


for line in f:

    records = line.strip().split('|')

    if first_line:
        print >> c, line.strip()
        first_line = False

    if records[0] == 'C':
        if records[1] in ['HUA06028', 'HUT06028', 'BPU29008'] :
            command_records = []
            in_patch_command = True
            patch_commands += 1
            calc.initialise()
        else:
            in_patch_command = False

    if in_patch_command:
        command_records.append(records)
        if records[0] in ['HUA6206L', 'HUT6206L', 'BPU2906L']:
            print records
            if records[5] == 'r':
                records[5] = '0'
            calc.process_octet(records[5], False)
        
        elif records[0] in ['HUA6205X', 'HUT6206X', 'BPU2905L']:
            xs = calc.calculate()

            if int(xs, 16) != int(records[5]):
                corrections += 1 
                print corrections
                records[5] = str(int(xs, 16)) 
#                command_records[-1][5] = records[5]
                for r in command_records: 
                    if r[0] in ['HUA6206X', 'HUT6206X', 'BPU2905L']:
                        r[5] = records[5]
                    print >> c, '|'.join(r)
#                print 'Calculated value =', xs
                print 'Commanded  value = %(val)04X' % {'val': int(records[5])}


    print >> o, '|'. join(records)

f.close()
o.close()
c.close()

print 'Stack file', sys.argv[1], 'processed.', corrections, 'checksum correction made.', patch_commands, ' commands in total.'
