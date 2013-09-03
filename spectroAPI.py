#import sys
import serial
import struct
import time

# Version 2013-09-02

""" define some time constants: these are necessary sleep times between sending 
    some signal to the spectrometer and polling the answer (buffer fill time).
    They may have to be adjusted according to your RS232 connection speed """
CONST_TIME_SHORT  = 0.05 #seconds
CONST_TIME_MEDIUM = 0.1
CONST_TIME_LONG   = 1.0


class Spectrometer():
    #
    # functions for initialization and closing
    #
    def __init__(self, Vport, Vbaudrate, Vparity, Vstopbits, Vbytesize):
        """ initialize the interface to the spectrometer """
        self.device = serial.Serial( port=Vport,
                                     baudrate=Vbaudrate,
                                     parity=Vparity,
                                     stopbits=Vstopbits,
                                     bytesize=Vbytesize)
        self.VerboseLevel = 0    #keep calm and carry on
        self.flush_buffer()      #empty the buffer 

    def close(self): 
        """ close the serial port """
        self.device.close()

    #
    # interface misc
    #
    def set_verbose_level(self,val):
        """ set the verbose level of the interface output """
        self.VerboseLevel = val
	print "spectrometer verbosity now is %d"%val

    def __verbose_output(self, message, reflevel):
        """ print an output message when self.VerboseLevel >= reflevel """
        if self.VerboseLevel >= reflevel:
            print( message )

    #
    # low-level spectrometer communication 
    #
    def flush_buffer(self):
        """ empty the spectrometer buffer; return and show its content (the latter if if self.VerboseLevel >= 2) """
        out = ''
        self.__verbose_output( "flushing buffer", 2 )
        while 1:
            time.sleep(CONST_TIME_MEDIUM)
            numbytes = self.device.inWaiting()
            out += self.device.read(numbytes)
            time.sleep(CONST_TIME_MEDIUM)
            if self.device.inWaiting()==0:
                break
        self.__verbose_output( "... buffer contained the following:\n ---\n" + out + "\n --- \n",2 )
        return out.rstrip("\r\n")

    def send_message(self,message):
        """ send a message to the spectrometer """
        self.__verbose_output( ">>sending '%s' to spectrometer"%(message), 2 )
        self.device.write( message + "\r\n" )
        time.sleep(CONST_TIME_MEDIUM)          #short sleep time to prevent too many requests


    def make_sweep(self):
        """ make one single sweep """
        self.send_message("SSI") #make one sweep
        time.sleep(CONST_TIME_SHORT) #wait for spectrometer to finish sweep
        out = '1'
        self.__verbose_output( "sweeping ...", 1 )
        while out[0] != '0':
            self.send_message("MOD?")
            time.sleep(CONST_TIME_MEDIUM)
            self.__verbose_output("sweeping ...", 2)
            while self.device.inWaiting() > 2:                
                out =self.device.read(3)
        self.__verbose_output( "... sweep complete", 1)

    def query_float(self,query_string):
        """ returns the result of a Query (e.g. "STA?") as a float number """
        self.send_message(query_string)
        msg = self.flush_buffer()
        return float(msg)
    #
    # helper functions for syntax checking and parsing
    #
    def __is_int_or_float(self,val):
        """ check whether a value is an int or a float number """
        if isinstance(val,int) or isinstance(val,float):
            return True
        else:
            return False

    def __is_between(self, val, sta, sto):
        """ check whether sta<= val <= sto """ 
        if (val>=sta) and (val<=sto):
            return True
        else:
            return False

    def __byte_2_ascii(self,bdata):
        """ convert the binary response from 'DBA/B?' into float numbers """
        outdata = []  
        for i in range(0,len(bdata)-4,4):
            expbytes = bdata[i:i+2]     # 2 byte exponent
            manbytes = bdata[i+2:i+4]   # 2 byte mantissa
            expvalue = struct.unpack(">h",expbytes)
            manvalue = struct.unpack(">H",manbytes)
            psd_mW  = (manvalue[0])/10000.0*10**expvalue[0] #power spectral density in mW
            outdata.append(psd_mW)
        return outdata

    #
    # basic get and set functions
    #
    def is_log(self):
        """ check whether the spectrometer is in LOG mode; returns True or False """
        self.send_message("LVS?")
        msg = self.flush_buffer()
        if msg == "LOG":
            return True
        else:
            return False

        
    def set_optical_attenuator(self,val):
        """ set the optical attenuator """
        val = val.upper()
        if (val != "ON" ) and (val != "OFF"):
            print "error: set_optical_attenuator() - invalid argument"
        else:
            self.send_message("ATT %s"%val)

    def get_sweep_average(self):
        """ get the sweep average """
        self.send_message("AVS?")
        msg = self.flush_buffer()
        if msg=="OFF":
            return 0
        else:
            return int(msg)

    def set_sweep_average(self,val):
        """ set the sweep average """
        if self.__is_int_or_float(val) and self.__is_between(val,2,1000):
            self.send_message("AVS %d"%val)
        elif val == 0:
            self.send_message("AVS OFF")
        elif isinstance(val,str) and val.upper() == "OFF":
            self.send_message("AVS OFF")
        else:
            print "error: set_sweep_average() - invalid argument"

    def get_point_average(self):
        """ get the point average """
        self.send_message("AVT?")
        msg = self.flush_buffer()
        if msg=="OFF":
            return 0
        else:
            return int(msg)

    def set_point_average(self,val):
        """ set the point average """
        if self.__is_int_or_float(val) and self.__is_between(val,2,1000):
            self.send_message("AVT %d"%val)
        elif val == 0:
            self.send_message("AVT OFF")
        elif isinstance(val,str) and val.upper() == "OFF":
            self.send_message("AVT OFF")
        else:
            print "error: set_sweep_average() - invalid argument"
        
            
    def get_center_wavelength(self):
        """ get the center wavelength """
        return self.query_float("CNT?")

    def set_center_wavelength(self,val):
        """ set the center wavelength """
        if self.__is_int_or_float(val) and self.__is_between( val, 600, 1750):
            self.send_message("CNT %.2f"%val)
        else:
            print "error: set_center_wavelength() - invalid argument"
    
    def set_linear_scale(self,val):
        """ set the linear scale """
        if self.__is_int_or_float(val) and self.__is_between(val, 1e-12, 1.0):
            self.send_message( "LLV %f"%(val*1000))   #spectrometer expects values in mW!
        else:
            print "error: set_linear_scale() - invalid argument"

    def get_log_scale(self):
        """ get the log scale """
        return self.query_float("LOG?")

    def set_log_scale(self,val):
        """ set the log scale """
        if self.__is_int_or_float(val) and self.__is_between(val, 0.1, 10.0):
            self.send_message("LOG %.1f"%(val))
        else:
            print "error: set_log_scale() - invalid argument"

    def get_log_reference_level(self):
        """ get the log reference level """
        return self.query_float("RLV?")
    
    def set_log_reference_level(self,val):
        """ set the log reference level """
        if self.__is_int_or_float(val) and self.__is_between(val, -90.0, 30.0):
            self.send_message("RLV %.1f"%(val))
        else:
            print "error: set_log_reference_level() - invalid argument"

    def get_measuring_points(self):
        """ get the number of measuring points"""
        self.send_message( "MPT?")
        msg = self.flush_buffer()
        return int( msg )

    def set_measuring_points(self,val):
        """ set the number of measuring points"""
        if self.__is_int_or_float(val) and (val in [51,101,251,501,1001,2001,5001] ):
            self.send_message("MPT %d"%(val))
        else:
            print "error: set_measuring_points() - invalid argument"

    def get_resolution(self):
        """ get the resolution """
        return self.query_float("RES?")

    def set_resolution(self, val):
        """ set the resolution """
        if val == 1:
            val = 1.0
        if self.__is_int_or_float(val) and (val in [0.07, 0.1, 0.2, 0.5, 1.0] ):
            self.send_message("Res %.2f"%(val))
        else:
            print "error: set_resolution() - invalid argument"

    def get_span(self):
        """ get the span """
        self.query_float("SPN?")
    
    def set_span(self,val):
        """ set the span """
        if self.__is_int_or_float(val) and self.__is_between(val,0.2,1200.0):
            self.send_message("SPN %.1f"%val)
        else:
            print "error: set_span() - invalid argument"

    def get_start_wavelength(self):
        """ get the start wavelength """
        return self.query_float("STA?")

    def set_start_wavelength(self,val):
        """ set the start wavelength """
        if self.__is_int_or_float(val) and self.__is_between(val,600,1750):
            if val > self.get_stop_wavelength():
                print "error: start wavelength can not be set to > stop wavelength"
            else:
                self.send_message("STA %.1f"%(val))                
        else:
            print "error: set_start_wavelength() - invalid argument"


    def get_stop_wavelength(self):
        """ get the stop wavelength """
        return self.query_float("STO?")

    def set_stop_wavelength(self,val):
        """ set the stop wavelength """
        if self.__is_int_or_float(val) and self.__is_between(val,600,1800):
            if val < self.get_start_wavelength():
                print "error: stop wavelength can not be set to < start wavelength"
            else:
                self.send_message("STO %.1f"%(val))                
        else:
            print "error: set_stop_wavelength() - invalid argument"

    def get_VBW(self):
        """ get the video bandwidth (VBW) """
        self.send_message("VBW?")
        msg = self.flush_buffer()
        VBWdict = {"10HZ":10, "100HZ":100, "1KHZ":1000, "10KHZ":10000,"100KHZ":100000,"1MHZ":1000000}
        return VBWdict[msg]
        
    def set_VBW(self,val):
        """ set the video bandwidth (VBW) """
        if self.__is_int_or_float(val) and (val in [10, 1e2, 1e3, 1e4, 1e5, 1e6]):
                 self.send_message("VBW %d"%(val))        
        else: 
            print "error: set_VBW() - invalid argument"

            
    #
    # andvanced get functions
    #
    def get_wavelength_vector(self):
        """ get the wavelength vector, calculated from the current spectrometer settings"""
        startwl = self.get_start_wavelength()
        stopwl  = self.get_stop_wavelength()
        points = self.get_measuring_points()
        physres = (stopwl - startwl) / (points-1)
        wlvec = []
        for i in range(points):
            wlvec.append( i * physres + startwl )
        return wlvec

    def get_spectrum(self):
        """ pull one spectrum from the spectrometer """
        #check whether the spectrometer is in LOG display mode
        #if yes, store log variables and change to lin mode
        if self.is_log():
            waslog = True
            oldlogdiv = self.get_log_scale()
            oldlogref = self.get_log_reference_level()
            self.set_linear_scale(1e-3)
        else:
            waslog = False
        self.send_message("DBA?") #  request the data as binary (4 byte linear)
        time.sleep(CONST_TIME_MEDIUM)
        out = ""
        emptycounter = 0
        while 1:    #read the binary data from the buffer
            out += self.device.read(1)
            if self.device.inWaiting() < 2:
                emptycounter += 1
                if (emptycounter%10 == 0 ):
                    self.__verbose_output( "empty buffer. (already %d bytes read)"%(len(out)) , 2 )
                time.sleep(CONST_TIME_SHORT)
            if ord(out[len(out)-2]) == 13 and ord(out[len(out)-1]) == 10 and self.device.inWaiting() < 2:
                self.__verbose_output( "CRLF found after %i bytes."%len(out), 1)
                break
        spectrum = self.__byte_2_ascii(out) #convert the binary data
        #reset log mode if it was enabled before data request
        if waslog:
            self.set_log_scale(oldlogdiv)
            self.set_log_reference_level(oldlogref)
        return spectrum

    #
    # Functions that need to be tested
    #
    def get_current_memory(self):  #still untested!! what exactly is the difference between memory and trace?
        self.send_message("MSL?")
        msg = self.flush_buffer()
        return msg

    def set_current_memory(self,val): #still untested!!
        if val.upper() in ["A","B"]:
            self.send_message("MSL %s"%(val.upper))
        else: 
            print "error: set_current_memory - invalid argument"


    def get_current_trace(self):  #still untested!!
        self.send_message("TSL?")
        msg = self.flush_buffer()
        return msg

    def set_current_trace(self,val): #still untested!!
        if val.upper() in ["A","B"]:
            self.send_message("TSL %s"%(val.upper))
        else: 
            print "error: set_current_trace - invalid argument"

    def get_optical_attenuator(self):
        """ check whether the optical attenuator is on """
        self.send_message("ATT?")
        msg = self.flush_buffer()
        if msg=="ON":
            return True
        else:
            return False


    def get_linear_scale(self):
        """ get the linear scale """
        self.send_message("LLV?")
        msg = self.flush_buffer()
        if msg == "1.0W":
            return 1.0 #1.0W is the only (and highest) value with unit 'W'
        else:
            l = len(msg)
            unit = msg[l-2:l]
            value = float( msg[0:l-2])
            unitdict = {"MW":1e-3, "UW":1e-6, "NW":1e-9,"PW":1e-12}
            return value * unitdict[unit]
#            if unit == "MW":
#                return 1e-3 * value
#            elif unit == "UW":
#                return 1e-6 * value
#            elif unit == "NW":
#                return 1e-9 * value
#            elif unit == "PW":
#                return 1e-12 * value
    

#
# TODO
# -'set' functions shall return True if the input was valid, False otherwhise
# -(consistency) tests
# -memory "A" or "B" selection etc
#


s = Spectrometer('/dev/ttyUSB0',
                 9600,
                 serial.PARITY_NONE,
                 serial.STOPBITS_ONE,
                 serial.EIGHTBITS)

s.set_verbose_level(1)

s.set_sweep_average(0)
s.set_point_average(0)
s.set_VBW(1e3)
s.set_start_wavelength(800)
s.set_stop_wavelength(1500)
s.set_measuring_points(251)
s.make_sweep()
aa = s.get_spectrum()
print aa
print max(aa)
s.close()

