... this aims to be an interface for the anritsu ms9710b spectrometer.

connection is done via serial port (with an USB->RS232 dongle in our case).

spectroAPI.py provides the API

programs that make use of the API are planned.

# dependencies 
you will need the pyserial software package and python>2.7.3

!!! CAUTION: this software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE !!!


# api functions 


### low level communication 

* **Spectrometer.send_message(MSG)**          send a message to the spectrometer
* **Spectrometer.flush_buffer()**		get the content of the buffer
* **Spectrometer.set\_verbose\_level(self,val)** control the verbosity of the API (0,1,2,...)

### get functions

* **Spectrometer.get\_current\_memory()**       STRING     "A","B"
* **Spectrometer.get\_current\_trace()**        STRING     "A","B"
* **Spectrometer.is_log()**			BOOL
* **Spectrometer.get\_optical\_attenuator()**   BOOL
* **Spectrometer.get_sweep_average()**	INT   0=off, 2..1000
* **Spectrometer.get\_point\_average()**	INT   0=off, 2..1000
* **Spectrometer.get\_center\_wavelength()**    FLOAT 600 ..1750
* **Spectrometer.get\_log\_scale()** FLOAT 0.1..10.0
* **Spectrometer.get\_log\_reference\_level()** FLOAT -90.0..30.0
* **Spectrometer.get\_resolution()** FLOAT [0.07,0.1,0.2,0.5,1.0]
* **Spectrometer.get\_measuring\_points()** INT [51,101,251,501,1001,2001,5001]
* **Spectrometer.get\_span()** FLOAT 0.2..1200.0
* **Spectrometer.get\_start\_wavelength()** FLOAT 600.0..1750.0
* **Spectrometer.get\_stop\_wavelength()** FLOAT 600.0..1800.0
* **Spectrometer.get\_VBW()** FLOAT [1e1,1e2,1e3,1e4,1e5,1e6]

### set functions  
* **Spectrometer.set\_optical\_attenuator(val)**   BOOL
* **Spectrometer.set\_sweep\_average(val)**     INT val=0 (off), 2..1000
* **Spectrometer.set\_point\_average(val)**	INT   0=off, 2..1000
* **Spectrometer.set\_center\_wavelength(val)** FLOAT 600.1750
* **Spectrometer.set\_linear\_scale(val)** FLOAT 1.0e-12..1.0 
* **Spectrometer.set\_log\_scale(val)** FLOAT 0.1..10.0
* **Spectrometer.set\_log\_reference\_level(val)** FLOAT -90.0..30.0
* **Spectrometer.set\_measuring\_points(val)** INT [51,101,251,501,1001,2001,5001]
* **Spectrometer.set\_resolution(val)** FLOAT [0.07,0.1,0.2,0.5,1.0]
* **Spectrometer.set\_span(val)** FLOAT 0.2..1200.0
* **Spectrometer.set\_start\_wavelength(val)** FLOAT 600.0..1750.0
* **Spectrometer.set\_stop\_wavelength(val)** FLOAT 600.0..1800.0
* **Spectrometer.set\_VBW(val)** FLOAT [1e1,1e2,1e3,1e4,1e5,1e6]

* **Spectrometer.get\_wavelength\_vector()** returns the wavelenght vector calculated according to the actual settings
### control functions 
* **Spectrometer.make\_sweep()**
