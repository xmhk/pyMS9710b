
def maketable(heading,liste):
    print heading
    for index,val in enumerate(liste):
        if index == 0:
            print"<table>"
        print "<tr>",
        for index2,ele in enumerate(val):
            if index == 0:
                print "<td><b>%s</b></td>"%(ele),
            else:
                if index2==0:
                    print "<td><b>%s</b></td>"%(ele),
                else:
                    print "<td>%s</td>"%(ele),
        print "</tr>"
        if index == len(liste)-1:
            print "</table>"



list_lowlevel = [['method', 'description','input type', 'input range','output type','output range'],
         ['Spectrometer.send_message(MSG)','send a message to the spectrometer','','','',''],
         [ 'Spectrometer.flush_buffer()'  ,'get the content of the buffer'     ,'','','',''],
         ['Spectrometer.set_verbose_level(self,val)','control the verbosity of the API ','INT','0,1,2,..','','',]

]

list_get_functions = [['method', 'description','input type', 'input range','output type','output range'],
                       ['Spectrometer.get_current_memory()','returns current memory bank','-','-','STRING','A, B'],
                       ['Spectrometer.get_current_trace()','returns current trace','-','-','STRING','A or B'],
                       ['Spectrometer.is_log()','check whether spectrometer is in log mode','-','-','BOOL','True, False'],
                       ['Spectrometer.get_optical_attenuator()','check wheter optical attenuator is on','-','-','BOOL','True, False'],
                       ['Spectrometer.get_sweep_average()','returns sweep average','-','-','INT','0=off, 2 .. 1000'],
                       ['Spectrometer.get_point_average()','returns point average','-','-','INT','0=off, 2 .. 1000'],
                       ['Spectrometer.get_center_wavelength()','returns center wavelength','-','-','FLOAT', '600.0  .. 1750.0 (in nm)'],
                       ['Spectrometer.get_log_scale()','returns log scaling','-','-','FLOAT','0.1 .. 10.0 (in UNIT?)'],
                       ['Spectrometer.get_linear_scale()','returns linear scaling','-','-','FLOAT','1e-12 .. 1.0 (in W/div ??? check unit)'],
                       ['Spectrometer.get_log_reference_level()','returns log reference level','-','-','FLOAT','-90.0 .. 30.0 (in UNIT?)'],
                      ['Spectrometer.get_resolution()','returns display resolution','-','-','FLOAT','[0.07,0.1,0.2,0.5,1.0] (in nm)'],
                      ['Spectrometer.get_measuring_points()','returns the number ofe measuring points','-','-','INT','[51,101,251,501,1001,2001,5001]'],
                      ['Spectrometer.get_span()','returns span','-','-','FLOAT','0.2 .. 1200.0 (in nm)'],
                      ['Spectrometer.get_start_wavelength()','returns start wavelength','-','-','FLOAT','600.0 .. 1750.0 (in nm)'],
                      ['Spectrometer.get_stop_wavelength()','returns stop wavelength','-','-','FLOAT','600.0 .. 1800.0 (in nm)'],
                      ['Spectrometer.get_VBW()','returns video bandwidth','-','-','FLOAT','[1e1,1e2,1e3,1e4,1e5,1e6] (in Hz)'],
                      ['Spectrometer.get_wavelength_vector()','returns the wavelenght vector calculated according to the actual settings','-','-','List of FLOAT','600.0 .. 800.0  (in nm)']
]

list_set_functions = [['method', 'description','input type', 'input range','output type','output range'],
                      ['Spectrometer.set_optical_attenuator(val)','set the optical attenuator','BOOL','True, False','',''],
                      ['Spectrometer.set_sweep_average(val)','set the sweep average','INT','0 (off), 2..1000','',''],
                      ['Spectrometer.set_point_average(val)','set the point average','INT','0 (off), 2..1000','',''],
                      ['Spectrometer.set_center_wavelength(val)','set the center wavelength','FLOAT','600.0 .. 1750.0  (in nm)','',''],
                      ['Spectrometer.set_linear_scale(val)','set the linear display scale','FLOAT','1.0e-12 .. 1.0 (in UNIT?)','',''],
                      ['Spectrometer.set_log_scale(val)','set the log display scale','FLOAT','0.1 .. 10.0 (in UNIT?)','',''],
                      ['Spectrometer.set_log_reference_level(val)','set the log reference level','FLOAT','-90.0..30.0 (in UNIT?)','',''],
                      ['Spectrometer.set_measuring_points(val)','set the number of measuring points','INT','[51,101,251,501,1001,2001,5001]','',''],
                      ['Spectrometer.set_resolution(val)','set the resolution','FLOAT','[0.07,0.1,0.2,0.5,1.0] (in nm)','',''],
                      ['Spectrometer.set_span(val)','set the sweep span','FLOAT','0.2 .. 1200.0  (in nm)','',''],
                      ['Spectrometer.set_start_wavelength(val)','set the start wavelength','FLOAT','600.0 .. 1750.0 (in nm)','',''],
                      ['Spectrometer.set_stop_wavelength(val)','set the stop wavelength','FLOAT','600.0 .. 1800.0 (in nm)','',''],
                      [' Spectrometer.set_VBW(val)','set the video bandwidth','FLOAT','[1e1,1e2,1e3,1e4,1e5,1e6] (in Hz)','','']
                      ]


maketable('### low level communication ', list_lowlevel)
maketable('### get functions ', list_get_functions)
maketable('### set functions ', list_set_functions)
