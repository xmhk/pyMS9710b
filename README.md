... this aims to be an interface for the anritsu ms9710b spectrometer.

connection is done via serial port (with an USB->RS232 dongle in our case).

spectroAPI.py provides the API

programs that make use of the API are planned.

=== dependencies ===
you will need the pyserial software package and python>2.7.3

!!! CAUTION: this software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE !!!


=== api functions ===


== low level communication ==

Spectrometer.send_message(MSG)          send a message to the spectrometer 
Spectrometer.flush_buffer()		get the content of the buffer
Spectrometer.set_verbose_level(self,val) control the verbosity of the API (0,1,2,...)

== get functions ==

Spectrometer.get_current_memory()       STRING     "A","B"
Spectrometer.get_current_trace()        STRING     "A","B"
Spectrometer.is_log()			BOOL	   
Spectrometer.get_optical_attenuator()   BOOL

Spectrometer.get_sweep_average()	INT   0=off, 2..1000
Spectrometer.get_point_average()	INT   0=off, 2..1000
Spectrometer.get_center_wavelength()    FLOAT 600 ..1750

== set functions == 
Spectrometer.set_optical_attenuator(val)   BOOL
Spectrometer.set_sweep_average(val)     INT val=0 (off), 2..1000
Spectrometer.set_point_average(val)	INT   0=off, 2..1000
Spectrometer.set_center_wavelength(val) FLOAT 600.1750

== control functions ==
Spectrometer.make_sweep()
