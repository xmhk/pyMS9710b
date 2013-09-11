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
        function_wrapper( setfunction, v)
        passed = passed and v == function_wrapper( getfunction, None)
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

def alltests(s):
#    print "Memory select test:",test_memory_select(s)
#    print "Trace select test:",test_memory_select(s)
#    print "Optical Att. test:",test_optical_attenuator(s)
#    print "test setting measuring points:",test_measuring_points(s)
    print "sweep average: ",test_sweep_average(s)
#    print "point average : ",test_sweep_average(s)
#    print "center wavelength",test_center_wavelength(s)
