#/usr/bin/python


class ISOcal:

    def __init__(self):
        self.initialise()

    def initialise(self):
        self.c0 = 0
        self.c1 = 0

    def process_octet(self, octet, hexa = True):
        if hexa:  
            self.c0 += int(str(octet),16) 
        else:
            self.c0 += int(str(octet) )
#        print 'Process %(a)02X' % {'a':int(str(octet),16)}
        self.c0 %= 255
        self.c1 += self.c0 
        self.c1 %= 255


    def calculate(self):
        ck1 = -((self.c0 + self.c1) % 255) 
        ck2 = self.c1

        if ck1 < 0:
            ck1 += 255

        if ck1 == 0:
            ck1 = 255
        if ck2 == 0:
            ck2 = 255

        return '%(val1)02X%(val2)02X' % {'val1':ck1, 'val2':ck2}

