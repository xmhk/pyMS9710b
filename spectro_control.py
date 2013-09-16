from testfunctions import *
from spectroAPI import *




s = Spectrometer('/dev/ttyUSB0',
                 9600,
                 serial.PARITY_NONE,
                 serial.STOPBITS_ONE,
                 serial.EIGHTBITS)

s.set_verbose_level(0)

#print test_resolution(s)
alltests(s)
s.close()

