from rtlsdr import *
from numpy import *
rfPower = 0

def getPowerReading(device):
        rfPower = 0
        try:
            sdr = RtlSdr()
            print ("geting power readings")
		    # configure device
            sdr.sample_rate = 2.048e6  # Hz
            sdr.center_freq = 70e6     # Hz
            sdr.freq_correction = 60   # PPM
            sdr.gain = 'auto'
            samples = sdr.read_samples(256*1024)
            #self.lblname = wx.StaticText(self, label='relative power: %0.1f dB' % (10*log10(var(samples))), pos=(20,60))
#           self.editname = wx.TextCtrl(self, value="Enter here your name", pos=(150, 60), size=(140,-1))
           
            print(samples)
            print ('relative power: %0.1f dB' % (10*log10(var(samples))))
            sdr.close()
            rfPower = 10*log10(var(samples))
            return rfPower
        except Exception as e:
            print("Oops!  RTL SDR not avalable.  Try again...")   

            
def main():
     print ("Start main")
     powerReading = getPowerReading(0)
     print ("rf power = ",powerReading)
     
if __name__ == "__main__":
    main()     
     
     
