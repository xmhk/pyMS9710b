NO WARRANTY for NOTHING! still work in progress ... 
### low level communication 
<table>
<tr> <td><b>method</b></td> <td><b>description</b></td> <td><b>input type</b></td> <td><b>input range</b></td> <td><b>output type</b></td> <td><b>output range</b></td> </tr>
<tr> <td><b>Spectrometer.send_message(MSG)</b></td> <td>send a message to the spectrometer</td> <td></td> <td></td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.flush_buffer()</b></td> <td>get the content of the buffer</td> <td></td> <td></td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_verbose_level(self,val)</b></td> <td>control the verbosity of the API </td> <td>INT</td> <td>0,1,2,..</td> <td></td> <td></td> </tr>
</table>
### get functions 
<table>
<tr> <td><b>method</b></td> <td><b>description</b></td> <td><b>input type</b></td> <td><b>input range</b></td> <td><b>output type</b></td> <td><b>output range</b></td> </tr>
<tr> <td><b>Spectrometer.get_current_memory()</b></td> <td>returns current memory bank</td> <td>-</td> <td>-</td> <td>STRING</td> <td>A, B</td> </tr>
<tr> <td><b>Spectrometer.get_current_trace()</b></td> <td>returns current trace</td> <td>-</td> <td>-</td> <td>STRING</td> <td>A or B</td> </tr>
<tr> <td><b>Spectrometer.is_log()</b></td> <td>check whether spectrometer is in log mode</td> <td>-</td> <td>-</td> <td>BOOL</td> <td>True, False</td> </tr>
<tr> <td><b>Spectrometer.get_optical_attenuator()</b></td> <td>check wheter optical attenuator is on</td> <td>-</td> <td>-</td> <td>BOOL</td> <td>True, False</td> </tr>
<tr> <td><b>Spectrometer.get_sweep_average()</b></td> <td>returns sweep average</td> <td>-</td> <td>-</td> <td>INT</td> <td>0=off, 2 .. 1000</td> </tr>
<tr> <td><b>Spectrometer.get_point_average()</b></td> <td>returns point average</td> <td>-</td> <td>-</td> <td>INT</td> <td>0=off, 2 .. 1000</td> </tr>
<tr> <td><b>Spectrometer.get_center_wavelength()</b></td> <td>returns center wavelength</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>600.0  .. 1750.0 (in nm)</td> </tr>
<tr> <td><b>Spectrometer.get_log_scale()</b></td> <td>returns log scaling</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>0.1 .. 10.0 (in UNIT?)</td> </tr>
<tr> <td><b>Spectrometer.get_linear_scale()</b></td> <td>returns linear scaling</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>1e-12 .. 1.0 (in W/div ??? check unit)</td> </tr>
<tr> <td><b>Spectrometer.get_log_reference_level()</b></td> <td>returns log reference level</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>-90.0 .. 30.0 (in UNIT?)</td> </tr>
<tr> <td><b>Spectrometer.get_resolution()</b></td> <td>returns display resolution</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>[0.07,0.1,0.2,0.5,1.0] (in nm)</td> </tr>
<tr> <td><b>Spectrometer.get_measuring_points()</b></td> <td>returns the number ofe measuring points</td> <td>-</td> <td>-</td> <td>INT</td> <td>[51,101,251,501,1001,2001,5001]</td> </tr>
<tr> <td><b>Spectrometer.get_span()</b></td> <td>returns span</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>0.2 .. 1200.0 (in nm)</td> </tr>
<tr> <td><b>Spectrometer.get_start_wavelength()</b></td> <td>returns start wavelength</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>600.0 .. 1750.0 (in nm)</td> </tr>
<tr> <td><b>Spectrometer.get_stop_wavelength()</b></td> <td>returns stop wavelength</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>600.0 .. 1800.0 (in nm)</td> </tr>
<tr> <td><b>Spectrometer.get_VBW()</b></td> <td>returns video bandwidth</td> <td>-</td> <td>-</td> <td>FLOAT</td> <td>[1e1,1e2,1e3,1e4,1e5,1e6] (in Hz)</td> </tr>
<tr> <td><b>Spectrometer.get_wavelength_vector()</b></td> <td>returns the wavelenght vector calculated according to the actual settings</td> <td>-</td> <td>-</td> <td>List of FLOAT</td> <td>600.0 .. 800.0  (in nm)</td> </tr>
</table>
### set functions 
<table>
<tr> <td><b>method</b></td> <td><b>description</b></td> <td><b>input type</b></td> <td><b>input range</b></td> <td><b>output type</b></td> <td><b>output range</b></td> </tr>
<tr> <td><b>Spectrometer.set_optical_attenuator(val)</b></td> <td>set the optical attenuator</td> <td>BOOL</td> <td>True, False</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_sweep_average(val)</b></td> <td>set the sweep average</td> <td>INT</td> <td>0 (off), 2..1000</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_point_average(val)</b></td> <td>set the point average</td> <td>INT</td> <td>0 (off), 2..1000</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_center_wavelength(val)</b></td> <td>set the center wavelength</td> <td>FLOAT</td> <td>600.0 .. 1750.0  (in nm)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_linear_scale(val)</b></td> <td>set the linear display scale</td> <td>FLOAT</td> <td>1.0e-12 .. 1.0 (in UNIT?)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_log_scale(val)</b></td> <td>set the log display scale</td> <td>FLOAT</td> <td>0.1 .. 10.0 (in UNIT?)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_log_reference_level(val)</b></td> <td>set the log reference level</td> <td>FLOAT</td> <td>-90.0..30.0 (in UNIT?)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_measuring_points(val)</b></td> <td>set the number of measuring points</td> <td>INT</td> <td>[51,101,251,501,1001,2001,5001]</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_resolution(val)</b></td> <td>set the resolution</td> <td>FLOAT</td> <td>[0.07,0.1,0.2,0.5,1.0] (in nm)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_span(val)</b></td> <td>set the sweep span</td> <td>FLOAT</td> <td>0.2 .. 1200.0  (in nm)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_start_wavelength(val)</b></td> <td>set the start wavelength</td> <td>FLOAT</td> <td>600.0 .. 1750.0 (in nm)</td> <td></td> <td></td> </tr>
<tr> <td><b>Spectrometer.set_stop_wavelength(val)</b></td> <td>set the stop wavelength</td> <td>FLOAT</td> <td>600.0 .. 1800.0 (in nm)</td> <td></td> <td></td> </tr>
<tr> <td><b> Spectrometer.set_VBW(val)</b></td> <td>set the video bandwidth</td> <td>FLOAT</td> <td>[1e1,1e2,1e3,1e4,1e5,1e6] (in Hz)</td> <td></td> <td></td> </tr>
</table>
