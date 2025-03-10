from libhackrf import *
from pylab import *     # for plotting

hackrf = HackRF()

# Adjust LNA and VGA gain settings
hackrf.set_lna_gain(1i8) # Start with a moderate gain
hackrf.set_vga_gain(18) # Adjust based on the outcomes

hackrf.sample_rate = 20e6
hackrf.center_freq = 2.437e9

samples = hackrf.read_samples(650000)

import pdb; pdb.set_trace()

# use matplotlib to estimate and plot the PSD
psd(np.log(10, samples), NFFT=1024, Fs=hackrf.sample_rate/1e6, Fc=hackrf.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')
show()
