#from spectroAPI import *
def test_memory_select(spec):
    oldmem = spec.get_current_memory()
    spec.set_current_memory("A")
    passed =  spec.get_current_memory()=="A"
    spec.set_current_memory("B")
    passed = passed and spec.get_current_memory()=="B"
    spec.set_current_memory(oldmem)
    return passed

def test_current_trace_select():
    oldtrace = s.get_current_trace()
    s.set_current_trace("A")
    passed = "A"==s.get_current_trace()
    s.set_current_trace("B")
    passed = passed and "B" == spec.get_current_trace()
    s.set_current_trace(oldtrace)
    return passed


def alltests():
    print "Memory select test:",test_memory_select(s)
    print "Trace select test:",test_memory_select(s)

def test1():

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
