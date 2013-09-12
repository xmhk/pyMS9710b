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
* **Spectrometer.set_verbose_level(self,val)** control the verbosity of the API (0,1,2,...)

### get functions

* **Spectrometer.get_current_memory()**       STRING     "A","B"
* **Spectrometer.get_current_trace()**        STRING     "A","B"
* **Spectrometer.is_log()**			BOOL
* **Spectrometer.get_optical_attenuator()**   BOOL

* **Spectrometer.get_sweep_average()**	INT   0=off, 2..1000
* **Spectrometer.get_point_average()**	INT   0=off, 2..1000
* **Spectrometer.get_center_wavelength()**    FLOAT 600 ..1750

* **Spectrometer.get_log_scale()** FLOAT 0.1..10.0
* **Spectrometer.get_log_reference_level()** FLOAT -90.0..30.0
* **Spectrometer.get_resolution()** FLOAT [0.07,0.1,0.2,0.5,1.0]

* **Spectrometer.get_measuring_points()** INT [51,101,251,501,1001,2001,5001]
* **Spectrometer.get_span()** FLOAT 0.2..1200.0
* **Spectrometer.get_start_wavelength()** FLOAT 600.0..1750.0
* **Spectrometer.get_stop_wavelength()** FLOAT 600.0..1800.0
* **Spectrometer.get_VBW()** FLOAT [1e1,1e2,1e3,1e4,1e5,1e6]

### set functions  
* **Spectrometer.set_optical_attenuator(val)**   BOOL
* **Spectrometer.set_sweep_average(val)**     INT val=0 (off), 2..1000
* **Spectrometer.set_point_average(val)**	INT   0=off, 2..1000
* **Spectrometer.set_center_wavelength(val)** FLOAT 600.1750
* **Spectrometer.set_linear_scale(val)** FLOAT 1.0e-12..1.0 
* **Spectrometer.set_log_scale(val)** FLOAT 0.1..10.0
* **Spectrometer.set_log_reference_level(val)** FLOAT -90.0..30.0
* **Spectrometer.set_measuring_points(val)** INT [51,101,251,501,1001,2001,5001]
* **Spectrometer.set_resolution(val)** FLOAT [0.07,0.1,0.2,0.5,1.0]
* **Spectrometer.set_span(val)** FLOAT 0.2..1200.0
* **Spectrometer.set_start_wavelength(val)** FLOAT 600.0..1750.0
* **Spectrometer.set_stop_wavelength(val)** FLOAT 600.0..1800.0
* **Spectrometer.set_VBW(val)** FLOAT [1e1,1e2,1e3,1e4,1e5,1e6]

* **Spectrometer.get_wavelength_vector()** returns the wavelenght vector calculated according to the actual settings
### control functions 
* **Spectrometer.make_sweep()**
