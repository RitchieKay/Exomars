#!/usr/bin/python
import sys
import re
import os.path

class acq_processor:

    def __init__(self, action_sequences):
        self.action_sequences = action_sequences
        self.initialise()

    def initialise(self):
        self.spacing = 0
        self.time = 0
        self.nesting = 0

    def process_action_sequence(self, id):

        self.nesting += 1
        spacing = 4 * self.nesting

        action_sequence = self.action_sequences[id]

        print '%(t)8.1fs %(s)s %(id)3d %(name)s' %  {'t': self.time, 's':'-'*spacing, 'id': action_sequence.get_id(), 'name' : action_sequence.get_name()}

        for line in action_sequence:
            if line.get_type() == 'ACSEQ':
                self.process_action_sequence(line.get_other())
            elif line.get_type() == 'WAIT': 
                self.time += 1.0 * line.get_other()/1000

#        print ' '*self.spacing, action_sequence.get_id(), action_sequence.get_name()
        self.nesting -= 1
        if self.nesting == 0:
            action_sequence.set_time(self.time)
            print '%(t)8.1fs' %  {'t': self.time}


def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<file name>'
        sys.exit(-1)

    f = open(sys.argv[1])

    action_sequences = {}

    p1 = re.compile('Action Sequence ID = ([0-9]+) - ([A-Z_ 0-9]+)')
    p2 = re.compile('INDEX = ')

    a = None

    for line in f:
        m = p1.match(line.strip())
        if m:
            a = actionSequence(int(m.groups()[0]), m.groups()[1])
            action_sequences[a.get_id()] = a

        if p2.search(line.strip()):
            a.add_line(line.strip())

    p = acq_processor(action_sequences)

    for key in action_sequences.keys():

        if not action_sequences[key].get_standalone():
            p.initialise()
            print ''
            print 'ACTION SEQUENCE ID = %(id)3d - %(name)s' % {'id':key, 'name':action_sequences[key].get_name()}
            print '----------------------------------------------------------------------------------------------------'
            p.process_action_sequence(key)

    f.close()

    print ''
    print ''
    print 'Full list with timings'
    print ''
    print ''
  

    for key in action_sequences.keys():
            print '%(id)3d,%(name)s,%(time)d' % {'id':key, 'name':action_sequences[key].get_name(), 'time':action_sequences[key].get_time()}

        

class actionSequenceLine:

    def __init__(self, line):
        p1 = re.compile('INDEX = ([0-9]+) TYPE =\s*([A-Z]+)(.+)')
        s = p1.findall(line)
        self.index = s[0][0]
        self.type = s[0][1]

        if self.type == 'ACSEQ':
            p2 = re.compile('ACQ\(([0-9]+)\)')
            self.other = int(p2.findall(line)[0])
            self.standalone = False

        elif self.type == 'WAIT':
            p2 = re.compile('WAIT : ([0-9]+)')
            self.other = int(p2.findall(line)[0])


    def get_index(self):
        return self.index

    def get_type(self):
        return self.type

    def get_other(self):
        return self.other


class actionSequence:

    def __init__(self, id, name):
        self.lines = []
        self.id = id
        self.name = name
        self.time = 0
        self.standalone = True
 
    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def add_line(self, line):
        l = actionSequenceLine(line.strip())
        self.lines.append(l)
        if l.get_type() == 'ACSEQ':
            self.standalone = False
        elif l.get_type() == 'WAIT':
            self.time += l.get_other()

    def get_standalone(self):
        return self.standalone

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

if __name__ == '__main__':
    main()
