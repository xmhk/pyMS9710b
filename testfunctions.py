def function_wrapper(f,x):
    """ call a function with argument x, without argment when x==None"""
    if x==None:
        return f()
    else:
        return f(x)

def test_vals( getfunction, setfunction, validvals, invalidvals):
    """ test getting and setting for valid and invalid arguments"""
    oldval = function_wrapper(getfunction, None)
    passed = True
    for v in validvals:
        #print "v = ",v
        function_wrapper( setfunction, v)
        result = function_wrapper( getfunction, None)
        if isinstance(result,float): #prevent failure due to rounding errors
            if abs(result-v)/v < 1e-6:
                result = v
        passed = passed and v == result
        #print passed
    print "\n--- below : intentional errors ... ---"
    for iv in invalidvals:
        function_wrapper( setfunction, iv)
        passed = passed and iv != function_wrapper( getfunction, None)
    print "--------------------------------------"
    function_wrapper(setfunction, oldval)
    return passed 

def test_memory_select(spec):
    oldmem = spec.get_current_memory()
    spec.set_current_memory("A")
    passed =  spec.get_current_memory()=="A"
    spec.set_current_memory("B")
    passed = passed and spec.get_current_memory()=="B"
    spec.set_current_memory(oldmem)
    return passed

def test_current_trace_select(s):
    oldtrace = s.get_current_trace()
    s.set_current_trace("A")
    passed = "A"==s.get_current_trace()
    s.set_current_trace("B")
    passed = passed and "B" == spec.get_current_trace()
    s.set_current_trace(oldtrace)
    return passed

def test_optical_attenuator(s):
    oldstate = s.get_optical_attenuator()
    passed = True
    s.set_optical_attenuator(True)
    passed = passed and s.get_optical_attenuator()
    s.set_optical_attenuator(False)
    passed = passed and not  s.get_optical_attenuator()
    s.set_optical_attenuator(oldstate)
    return passed


def test_measuring_points(s):
    return test_vals( s.get_measuring_points,
                      s.set_measuring_points,
                      [51,101,251,501,1001,2001,5001],
                      [102])

def test_sweep_average(s):
    return test_vals( s.get_sweep_average,
                      s.set_sweep_average,
                      [0,2,500,1000],
                      [1,1001,-10])

def test_point_average(s):
    return test_vals( s.get_point_average,
                      s.set_point_average,
                      [0,2,500,1000],
                      [1,1001,-10])

def test_center_wavelength(s):
    return test_vals( s.get_center_wavelength,
                      s.set_center_wavelength,
                      [600,900,1750],
                      [500,-10,2000])


def test_linear_scale_setting(s):
    #test whether log
    waslog = False
    if s.get_is_log:
        oldlogscale = s.get_log_scale()
        oldlogref = s.get_log_reference_level()
        waslog = True
#        print "\n __ was log __ "
    RV = test_vals(  s.get_linear_scale,
                      s.set_linear_scale,
                      [1e-12,2e-11,3e-10,4e-9,5e-8,6e-7,7e-6,8e-5,9e-4,8e-3,7e-2,6e-1,1],
                      [10,1e-13])
    if waslog:
        s.set_log_scale( oldlogscale)
        s.set_log_reference_level( oldlogref)
    return RV


def test_log_scale_settings(s):
    #test whether is lin
    waslin = False
    if s.get_is_log() == False:
        oldlinscale = s.get_linear_scale()
    else:
        oldlogref = s.get_log_reference_level()
        oldlogscale = s.get_log_scale()
    RV = test_vals( s.get_log_scale,
                    s.set_log_scale,
                    [0.1,2,7.0,10.0],
                    [-0.2,11])
    RV2 = test_vals( s.get_log_reference_level,
                     s.set_log_reference_level,
                     [-90.0,-45.0,10,30],
                     [-91.0, 31.0])
    if waslin:
        s.set_linear_scale(oldlinscale)
    else:
        s.set_log_reference_level(oldlogref)
        s.set_log_scale(oldlogscale)    
    return RV and RV2

def test_resolution(s):
    oldres = s.get_resolution()
    RV = test_vals( s.get_resolution,
                    s.set_resolution,
                    [0.07,0.1,0.2,0.5,1.0],
                    [3,7])
    return RV


def test_span(s):
    oldspan = s.get_span()
    oldctr = s.get_center_wavelength()
    RV = test_vals( s.get_span,
                    s.set_span,
                    [0.20,1000.0,1200.0],
                    [0.1,1201.0])
    s.set_span(oldspan)
    s.set_center_wavelength(oldctr)
    return RV

def test_VBW(s):
    oldvbw = s.get_VBW()
    RV = test_vals( s.get_VBW,
                    s.set_VBW,
                    [10,1e2,1e3, 1e4, 1e5, 1e6],
                    [1,1e7])
    s.set_VBW(oldvbw)
    return RV

def alltests(s):
#    print "Memory select test:",test_memory_select(s)
#    print "Trace select test:",test_memory_select(s)
#    print "Optical Att. test:",test_optical_attenuator(s)
#    print "test setting measuring points:",test_measuring_points(s)
#    print "sweep average: ",test_sweep_average(s)
    print "point average : ",test_sweep_average(s)
#    print "center wavelength",test_center_wavelength(s)
#    print "lin. scale settings",test_linear_scale_setting(s)
#    print "log scale settings",test_log_scale_settings(s)
#    print "test resolutions settings", test_resolution(s) 
    print "span test", test_span(s)
    print "VBW test ",test_VBW(s)
    pass


