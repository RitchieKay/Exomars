#!/usr/bin/python

import re

f = open ('a')

p = re.compile('self.acseq_ids\[([0-9]+)\]')

m = {}

for line in f:
     s = p.search(line.strip())
     if s:
         m[int(s.groups()[0])] = line.strip()

     
for k in m.keys():

    print m[k]

f.close()
