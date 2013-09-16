#import sys
import serial
import struct
import time

# Version 2013-09-10

""" define some time constants: these are necessary sleep times between sending 
    some signal to the spectrometer and polling the answer (buffer fill time).
    They may have to be adjusted according to your RS232 connection speed """
CONST_TIME_SHORT  = 0.05 #seconds
CONST_TIME_MEDIUM = 0.15
CONST_TIME_LONG   = 1.0


class Spectrometer_state():
    """ it's up to you to use this or make your own state variable(s)"""
    def __init__(self,s):
        self.state = self.update(s)
        
    def update(self,s):
        state={'is_log':s.is_log()}
        state.update({'optical_attenuator':s.get_optical_attenuator()})
        state.update({'sweep_average':s.get_sweep_average()})
        state.update({'point_average':s.get_point_average()})
        state.update({'center_wavelength':s.get_center_wavelength()})
        state.update({'current_memory':s.get_current_memory()})
        state.update({'center_wavelength':s.get_center_wavelength()})        
        state.update({'current_trace':s.get_current_trace()})
        state.update({'center_wavelength':s.get_center_wavelength()})        
        state.update({'measuring_points':s.get_measuring_points()})
        state.update({'center_wavelength':s.get_center_wavelength()})        
        state.update({'resolution':s.get_resolution()})
        state.update({'span':s.get_span()})
        state.update({'start_wavelength':s.get_start_wavelength()})
        state.update({'stop_wavelength':s.get_stop_wavelength()})
        state.update({'start_wavelength':s.get_start_wavelength()})
        state.update({'start_wavelength':s.get_start_wavelength()})
        state.update({'VBW':s.get_VBW()})
        return state
    def printt(self):
        print "\n\n ---- spectrometer state --- \n"
        for key in self.state.iterkeys():
            print "%s - "%(key), self.state[key]
        
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
    def flush_buffer(self):     #tested and documented
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

    def send_message(self,message):   #tested and documtented
        """ send a message to the spectrometer """
        self.__verbose_output( ">>sending '%s' to spectrometer"%(message), 2 )
        self.device.write( message + "\r\n" )
        time.sleep(CONST_TIME_MEDIUM)          #short sleep time to prevent too many requests


    def make_sweep(self):  # documented
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

    def __query_float(self,query_string): 
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
    def is_log(self): #tested and documtented
        """ check whether the spectrometer is in LOG mode; returns True or False """
        self.send_message("LVS?")
        msg = self.flush_buffer()
        if msg == "LOG":
            return True
        else:
            return False

    def get_sweep_average(self):       #tested and documented
        """ get the sweep average """
        self.send_message("AVS?")
        msg = self.flush_buffer()
        if msg=="OFF":
            return 0
        else:
            return int(msg)

    def set_sweep_average(self,val):   #tested and documented
        """ set the sweep average """
        if self.__is_int_or_float(val) and self.__is_between(val,2,1000):
            self.send_message("AVS %d"%val)
        elif val == 0:
            self.send_message("AVS OFF")
        elif isinstance(val,str) and val.upper() == "OFF":
            self.send_message("AVS OFF")
        else:
            self.__verbose_output( "error: set_sweep_average() - invalid argument",1)

    def get_point_average(self):        #tested and documented
        """ get the point average """
        self.send_message("AVT?")
        msg = self.flush_buffer()
        if msg=="OFF":
            return 0
        else:
            return int(msg)

    def set_point_average(self,val):    #tested
        """ set the point average """
        if self.__is_int_or_float(val) and self.__is_between(val,2,1000):
            self.send_message("AVT %d"%val)
        elif val == 0:
            self.send_message("AVT OFF")
        elif isinstance(val,str) and val.upper() == "OFF":
            self.send_message("AVT OFF")
        else:
            self.__verbose_output("error: set_sweep_average() - invalid argument",1)
        
            
    def get_center_wavelength(self):     #tested and documented
        """ get the center wavelength """
        return self.__query_float("CNT?")

    def set_center_wavelength(self,val): #tested and documented
        """ set the center wavelength """
        if self.__is_int_or_float(val) and self.__is_between( val, 600, 1750):
            self.send_message("CNT %.2f"%val)
        else:
            self.__verbose_output("error: set_center_wavelength() - invalid argument",1)

    def get_current_memory(self):  #tested and documented
        self.send_message("MSL?")
        msg = self.flush_buffer()
        return msg

    def set_current_memory(self,val): #tested and documented
        if val.upper() in ["A","B"]:
            self.send_message("MSL %s"%(val.upper()))
            time.sleep(CONST_TIME_LONG) #spectrometer needs some time to switch 
        else: 
            self.__verbose_output("error: set_current_memory - invalid argument",1)

    def get_current_trace(self): #tested and documented
        self.send_message("TSL?")
        msg = self.flush_buffer()
        return msg

    def set_current_trace(self,val):  #tested documented
        if val.upper() in ["A","B"]:
            self.send_message("TSL %s"%(val.upper()))
            time.sleep(CONST_TIME_LONG)
        else: 
            self.__verbose_output("error: set_current_trace - invalid argument",1)
    
    def get_linear_scale(self): # tested and documented
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

    def set_linear_scale(self,val): #documented
        """ set the linear scale """
        if self.__is_int_or_float(val) and self.__is_between(val, 1e-12, 1.0):
            self.send_message( "LLV %.9f"%(val*1000))   #spectrometer expects values in mW!
        else:
            self.__verbose_output("error: set_linear_scale() - invalid argument",1)

    def get_log_scale(self):  # documented
        """ get the log scale """
        return self.__query_float("LOG?")

    def set_log_scale(self,val): # documented
        """ set the log scale """
        if self.__is_int_or_float(val) and self.__is_between(val, 0.1, 10.0):
            self.send_message("LOG %.1f"%(val))
        else:
            self.__verbose_output("error: set_log_scale() - invalid argument",1)

    def get_log_reference_level(self):  #documented
        """ get the log reference level """
        return self.__query_float("RLV?")
    
    def set_log_reference_level(self,val): #documented
        """ set the log reference level """
        if self.__is_int_or_float(val) and self.__is_between(val, -90.0, 30.0):
            self.send_message("RLV %.1f"%(val))
        else:
            self.__verbose_output( "error: set_log_reference_level() - invalid argument",1 )

    def get_measuring_points(self): # tested and documented
        """ get the number of measuring points"""
        self.send_message( "MPT?")
        msg = self.flush_buffer()
        return int( msg )

    def set_measuring_points(self,val): #tested and documented
        """ set the number of measuring points"""
        if self.__is_int_or_float(val) and (val in [51,101,251,501,1001,2001,5001] ):
            self.send_message("MPT %d"%(val))
        else:
            self.__verbose_output( "error: set_measuring_points() - invalid argument",1)

    def set_optical_attenuator(self,val): # tested and documented
        if isinstance(val,bool):
            if val==True:
                self.send_message("ATT ON")
            else: 
                self.send_message("ATT OFF")
        else:
                 self.__verbose_output( "error: set_optical_attenuator() - invalid argument",1)

    def get_optical_attenuator(self): #tested and documented
        """ check whether the optical attenuator is on """
        self.send_message("ATT?")
        msg = self.flush_buffer()
        if msg=="ON":
            return True
        else:
            return False

    def get_resolution(self): #documented
        """ get the resolution """
        return self.__query_float("RES?")

    def set_resolution(self, val): #documented
        """ set the resolution """
        if val == 1:
            val = 1.0
        if self.__is_int_or_float(val) and (val in [0.07, 0.1, 0.2, 0.5, 1.0] ):
            self.send_message("Res %.2f"%(val))
        else:
            self.__verbose_output( "error: set_resolution() - invalid argument",1)

    def get_span(self): #documented
        """ get the span """
        return self.__query_float("SPN?")
    
    def set_span(self,val): #documented
        """ set the span """ 
        if self.__is_int_or_float(val) and self.__is_between(val,0.2,1200.0):
            self.send_message("SPN %.1f"%val)
        else:
            self.__verbose_output( "error: set_span() - invalid argument",1)

    def get_start_wavelength(self):  # documented
        """ get the start wavelength """
        return self.__query_float("STA?")

    def set_start_wavelength(self,val): #documented
        """ set the start wavelength """
        if self.__is_int_or_float(val) and self.__is_between(val,600,1750):
            if val > self.get_stop_wavelength():
                self.__verbose_output( "error: start wavelength can not be set to > stop wavelength",1)
            else:
                self.send_message("STA %.1f"%(val))                
        else:
            self.__verbose_output( "error: set_start_wavelength() - invalid argument",1)


    def get_stop_wavelength(self): #documented
        """ get the stop wavelength """
        return self.__query_float("STO?")

    def set_stop_wavelength(self,val): #documented
        """ set the stop wavelength """
        if self.__is_int_or_float(val) and self.__is_between(val,600,1800):
            if val < self.get_start_wavelength():
                self.__verbose_output(  "error: stop wavelength can not be set to < start wavelength",1)
            else:
                self.send_message("STO %.1f"%(val))                
        else:
            self.__verbose_output( "error: set_stop_wavelength() - invalid argument",1)

    def get_VBW(self):  # documented
        """ get the video bandwidth (VBW) """
        self.send_message("VBW?")
        msg = self.flush_buffer()
        VBWdict = {"10HZ":10, "100HZ":100, "1KHZ":1000, "10KHZ":10000,"100KHZ":100000,"1MHZ":1000000}
        return VBWdict[msg]
        
    def set_VBW(self,val): #documented
        """ set the video bandwidth (VBW) """
        if self.__is_int_or_float(val) and (val in [10, 1e2, 1e3, 1e4, 1e5, 1e6]):
                 self.send_message("VBW %d"%(val))        
        else: 
            self.__verbose_output( "error: set_VBW() - invalid argument",1)

            
    #
    # andvanced get functions
    #
    def get_wavelength_vector(self): #documented
        """ get the wavelength vector, calculated from the current spectrometer settings"""
        startwl = self.get_start_wavelength()
        stopwl  = self.get_stop_wavelength()
        points = self.get_measuring_points()
        physres = (stopwl - startwl) / (points-1)
        wlvec = []
        for i in range(points):
            wlvec.append( i * physres + startwl )
        return wlvec

    def get_spectrum(self,membank):
        """ pull one spectrum from the spectrometer """

        if not membank in ["A","B"]:
            print "get_spectrum argument error!"
            return 0
        else: membank = membank.upper()
        #check whether the spectrometer is in LOG display mode
        #if yes, store log variables and change to lin mode
        if self.is_log():
            waslog = True
            oldlogdiv = self.get_log_scale()
            oldlogref = self.get_log_reference_level()
            self.set_linear_scale(1e-3)
        else:
            waslog = False
        self.send_message("DB%s?"%(membank)) #  request the data as binary (4 byte linear)
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


