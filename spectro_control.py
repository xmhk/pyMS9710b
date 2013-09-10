from testfunctions import *
from spectroAPI import *




s = Spectrometer('/dev/ttyUSB0',
                 9600,
                 serial.PARITY_NONE,
                 serial.STOPBITS_ONE,
                 serial.EIGHTBITS)


#print tdict

#s.set_current_memory("B")
#s.make_sweep()
#print s.get_spectrum("A")
#s.set_verbose_level(1)

state = Spectrometer_state(s)
state.printt()

s.close()

