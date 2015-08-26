#!/usr/bin/python
###################################################
# action_sequence_parser.py
# This script provides parsing of action sequence xml
# files including processing and display of contents/
#
# Ritchie Kay - 26/08/2015
###################################################
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import datetime
import re
import random
import sys
import glob
import os.path
from optparse import OptionParser

class ActionSequenceItem:

    def __init__(self):
        pass
    def get_type(self):
        return ''

class Command(ActionSequenceItem):

    def __init__(self, name, description):
        self.name = name
        self.type = 0
        self.subtype = 0
        self.description = description

        p = re.compile('\[([0-9]+);([0-9]+)\]')
    
        m = p.findall(description)
        if m:
            self.type = int(m[0][0])
            self.subtype = int(m[0][1])

            self.description = description[0:description.index('[')]
        self.parameters = []

    def add_parameter(self, p):
        self.parameters.append(p)

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_parameters(self):
        return self.parameters

    def get_tc(self):
        if self.type == 0 and self.subtype == 0:
            return 'TC'
        else:
            return 'TC(' + str(self.type) + ',' + str(self.subtype) + ')'

    def get_type(self):
        return 'TC'

    def __str__(self):
        return self.description

class Parameter:

    def __init__(self, name, description, value):
        self.name = name
        self.description = description 
        self.value = value

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_value(self):
        return self.description

    def __str__(self):
        return self.description + ' : ' + self.value

class Wait(ActionSequenceItem):

    def __init__(self, time):

        d = datetime.datetime.strptime(time, '00%H:%M:%S.%f')
        delta = datetime.timedelta(hours = d.hour, minutes = d.minute, seconds = d.second, microseconds = d.microsecond)

        self.seconds = delta.total_seconds()
 
    def get_seconds(self):
        return self.seconds

    def get_type(self):
        return 'WAIT'

    def __str__(self):
        return 'WAIT ' + str(self.seconds)

class ActionSequenceCall(ActionSequenceItem):

    def __init__(self, id):
        self.id = int(id)

    def get_id(self):
        return int(self.id)

    def get_type(self):
        return 'ACSEQ'

    def __str__(self):
        return 'ACSEQ(' + str(self.id) + ')'

class Comment(ActionSequenceItem):

    def __init__(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def __str__(self):
        return self.text

    def get_type(self):
        return 'CMT'

class ActionSequence:

    def __init__(self, name = '' , id = 0):

        self.name = name
        self.id = id
        self.items = []
        self.real_items = []
        self.time = 0

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def __hash__(self):
        return hash(str(id) + self.name)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_id(self, id):
        self.id = int(id)

    def get_id(self):
        return int(self.id)

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def add_item(self, item):
        self.items.append({'type':item.__class__.__name__, 'item':item})
        if item.__class__.__name__ != 'Comment':
            self.real_items.append({'type':item.__class__.__name__, 'item':item})

    def __len__(self):
        return len(self.real_items)

    def __getitem__(self, id):
        return self.real_items[id]['item']

  
class EventHandler(ContentHandler):

   def __init__ (self):
       self._inComment = False
       self._inCommand = False 
       self._comment = ''
       self._command = None
       self._actionSequence = None

   def setActionSequence(self, a):
       self._actionSequence = a

   def startElement(self, name, attrs):
       #print name, xtraAttrs

       if name == 'actionsequence:STATEMENT':
           type = attrs.getValueByQName('xsi:type')
           if type == 'actionsequence:BodyWaitType':
               duration = attrs.getValueByQName('Duration')
               self._actionSequence.add_item(Wait(duration))
           elif type == 'actionsequence:CallActionSequenceType':
               id = attrs.getValueByQName('ID')
               self._actionSequence.add_item(ActionSequenceCall(id))
           elif type == 'actionsequence:CommentType':
               self._inComment = True
               self._comment = ''
           elif type == 'actionsequence:SendCommandType':
               self._inCommand = True 

       elif name == 'actionsequence:HighLevelData':
              self._actionSequence.set_name(attrs.getValueByQName('Name'))
              self._actionSequence.set_id(attrs.getValueByQName('ID'))


       if self._inCommand and name == 'actionsequence:Command':
           name = attrs.getValueByQName('Mnemonic')
           description = attrs.getValueByQName('Description')
           self._command = Command(name, description)
       elif self._inCommand and name == 'actionsequence:Parameter':
           name = attrs.getValueByQName('Mnemonic')
           description = attrs.getValueByQName('Description')
           value = attrs.getValueByQName('Value')
           self._command.add_parameter(Parameter(name, description, value))

   def characters(self, data):
       if self._inComment:
           self._comment += data.strip()

   def endElement(self, name):

       if self._inComment and name == 'actionsequence:CommentType':
           self._actionSequence.add_item(Comment(self._comment))
       if self._inCommand and name == 'actionsequence:Command':
           self._actionSequence.add_item(self._command)

       if name == 'actionsequence:STATEMENT':
           self._inComment = False
           self._inCommand = False
#
#
class AcseqParser:

    def __init__(self):

        self.parser = make_parser()
        self.curHandler = EventHandler()
        self.parser.setContentHandler(self.curHandler)


    def parse(self, file):

        a = ActionSequence()
        fh = open(file)
        self.curHandler.setActionSequence(a)
        self.parser.parse(fh)
        fh.close()

        return a

class Nesting:

    def __init__(self, c):
        self.level = 0
        self.c = c

    def increment(self):
        self.level += 1

    def decrement(self):
        self.level -= 1

    def get_level(self):
        return self.level

    def __str__(self):
        return self.c*self.level

class ActionSequenceProcessor:

    def __init__(self, action_sequences, verbose, nesting):
        self.action_sequences = action_sequences
        self.verbose = verbose
        self.nesting = Nesting(nesting)


        for a in action_sequences.keys():
            self.initialise()
            self.process_action_sequence(a, True)

        self.initialise()

    def initialise(self):
        self.spacing = 0
        self.time = 0

    def process_action_sequence(self, id, silent = False):

        self.nesting.increment()

        action_sequence = self.action_sequences[id]

        if not silent:
            print '%(t)8.1fs %(s)s %(id)3d %(name)s' %  {'t': self.time, 's':self.nesting, 'id': action_sequence.get_id(), 'name' : action_sequence.get_name()}


        for item in action_sequence:
            if item.get_type() == 'ACSEQ':
                self.process_action_sequence(item.get_id(), silent)
            elif item.get_type() == 'WAIT': 
               self.time += item.get_seconds() 
            elif item.get_type() == 'TC' and not silent:
                self.nesting.increment()
                if (self.verbose == 1 or (self.verbose > 1 and len(item.get_parameters()) == 0)): 
                    print '%(t)8.1fs %(s)s %(TC)s %(name)s' %  {'t':self.time, 'TC':item.get_tc(), 's':self.nesting, 'id': item.get_name(), 'name' : item.get_description()}
                elif item.get_type() == 'TC' and self.verbose > 1: 
                    p_str = ' : '.join([str(p) for p in item.get_parameters()]) 
                    if not silent:
                        print '%(t)8.1fs %(s)s %(TC)s %(name)s' %  {'t':self.time, 'TC':item.get_tc(), 's':self.nesting, 'id': item.get_name(), 'name' : item.get_description() + ' (' + p_str + ' )'}
                self.nesting.decrement()

        self.nesting.decrement()  

        if self.nesting.get_level() == 0:
            action_sequence.set_time(self.time)
            if not silent:
                print '%(t)8.1fs' %  {'t':self.time}


def main():

    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dir", help="XML directory")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default = False, help="Verbose. Show TCs sent from action sequences.")
    parser.add_option("-V", "--Verbose", dest="Verbose", action="store_true", default = False, help="Very Verbose. Show TCs and their parameter sent from action sequences.")
    parser.add_option("-i", "--id", dest="id", type="int",  help="Action sequence id")
    parser.add_option("-l", "--list", dest="list", action="store_true", default = True,  help="List action sequences")
    parser.add_option("-n", "--nesting", dest="nesting", default =  '   ',  help="String to be used to mark nesting level.")
    parser.add_option("-s", "--separator", dest="separator", default =  ' ',  help="String to be used as delimiter in list.")
    parser.add_option("-A", "--all", dest="all", action='store_true', default =  False,  help="Details of all action sequences")

    (options, args) = parser.parse_args()

    if not options.dir or not os.path.isdir(options.dir):
        parser.error('No directory specified or directory not valid. See help for.usage')

    action_sequences = {}

    for f in glob.glob(options.dir + '/*.xml'):
        a = AcseqParser().parse(f)
        action_sequences[int(a.get_id())] = a

    verbosity = 0
    if options.verbose: verbosity+= 1
    if options.Verbose: verbosity+= 2

    p = ActionSequenceProcessor(action_sequences, verbosity, options.nesting)

    if options.id:

        p.process_action_sequence(int(options.id))

    elif options.all:

        for id in action_sequences.keys():
            print 'ID = %(id)03d   TITLE = %(title)s' % {'id':id, 'title':action_sequences[id].get_name()}
            p.process_action_sequence(int(id))
            print ''
            print ''

    elif options.list:
        for a in action_sequences.keys():
            print ('ID = %(id)3d' + options.separator + '%(time)8.1fs' + options.separator + '%(name)s') %  {'id':a, 'name':action_sequences[a].get_name(), 'time':action_sequences[a].get_time()}

if __name__ == '__main__':
    main()
