from rtlsdr import *
from numpy import *

@limit_calls(9)
def power_meter_callback(samples, sdr):
    print ('relative power: %0.1f dB' % (10*log10(var(samples))))
       
sdr = RtlSdr()

sdr.sample_rate = 1.2e6
sdr.center_freq = 145.950e6
sdr.gain = 63
sdr.freq_correction = 60
#sdr.gain = 'auto'
#set_bandwidth
#set_direct_sampling()
#samples = sdr.read_samples(256*1024)
#sdr.close()
#set_direct_sampling
#sdr.read_samples_async(power_meter_callback)
