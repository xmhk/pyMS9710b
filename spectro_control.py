from testfunctions import *
from spectroAPI import *




s = Spectrometer('/dev/ttyUSB0',
                 9600,
                 serial.PARITY_NONE,
                 serial.STOPBITS_ONE,
                 serial.EIGHTBITS)

s.set_verbose_level(1)

s.set_log_scale( 5.0)

#print test_linear_scale_setting(s)

alltests(s)

#print s.is_log()
#print "alt :", s.get_linear_scale()
#s.set_linear_scale(1e-3)
#print "neu : ",s.get_linear_scale()
#print s.is_log()
#function_wrapper(s.get_measuring_points,None)

#print tdict

#s.set_current_memory("B")
#s.make_sweep()
#print s.get_spectrum("A")
#s.set_verbose_level(1)

#state = Spectrometer_state(s)
#state.printt()

s.close()

