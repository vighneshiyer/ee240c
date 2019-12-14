#!/usr/bin/env python3
from ADC import ADC
from MDAC import MDAC
import numpy as np
import sys

class Stage:
    def __init__(self, vrange: (float, float), levels: int, gain: float, offset_var: float, vin_signed: bool):
        self.adc = ADC(vrange, levels, mid_step=True, offset_var=offset_var)
        self.mdac = MDAC(vrange, levels, gain, vin_signed)
        self.vin_signed = vin_signed

    def output(self, vin: float) -> (int, float):
        adc_code = self.adc.convert(vin)[0]
        if self.vin_signed:
            adc_code = adc_code - 2
        residual = self.mdac.gen_residual(adc_code, vin)
        return (adc_code, residual)

if __name__ == "__main__":
    vrange = (0, 1.2)
    levels = 2**12
    s = Stage(vrange, levels=levels, gain=2, offset_var=0, vin_signed=False)
    fs = 25e6
    N = 2**12
    fsig = fs * 1223/N

    k = 1.38e-23
    T = 300
    Cs = 512e-15
    Cf = Cs / 2
    beta = Cf / (Cs + Cf)
    Cout_eff = Cs + (1 - beta)*Cf
    gamma = 2/3
    settling_time = 1/fs / 2
    gm1 = -(Cout_eff*np.log(1.2/levels)) / (beta*settling_time)
    gm3 = gm1
    samp_noise = k * T / Cs
    ota_noise = 2* (4*k*T*gamma / gm1) + 2*(4 *k*T*gamma*gm3 / gm1**2)
    ota_noise_fb = ota_noise * gm1 / (4*Cout_eff*beta**2)
    print(gm1, gm3)
    print(samp_noise)
    print(ota_noise, ota_noise_fb)
    term = samp_noise + ota_noise_fb
    noise_tot = samp_noise + (term)/2**2 + term/2*2**2 + term/3*2**2
    print(noise_tot)

    power = 1.2*gm1/(2/0.2)
    print(power*4)
    sys.exit(1)

    vals = [np.sin(2*np.pi*fsig*i/fs) + np.random.normal(0, np.sqrt(noise_tot)) for i in range(N)]
    vals = [x* 0.6 + 0.6 for x in vals]
    #vals = np.linspace(0, 1.2, 100)
    out = [s.output(x) for x in vals]
    #out = [[x, ''] for x in vals]
    import matplotlib.pyplot as plt
    #fig,ax = plt.subplots(1, 2)
    #ax[0].plot(vals, '.')
    #ax[0].plot([x[1] for x in out], '.')
    #ax[0].plot([-(x[1]-s.mdac.midpoint)/2 + x[0]*s.adc.step for x in out], '.')
    #ax[1].plot([x[0] for x in out], '.')
    #print(vals)
    #print(out)
    #plt.show()
    #sys.exit(1)

    data = [x[0] for x in out]
    #data_noise = [x + np.random.normal(0, noise_tot) for x in data]
    FS = levels
    raw_fft = np.abs(np.fft.fft(data))
    raw_fft = raw_fft[:int(N/2)]
    fft = 20*np.log10(2*raw_fft/N/FS)
    f = np.array(range(0, int(N/2))) / N * fs / 1e6
    plt.plot(f, fft)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Amplitude (dBFS)')
    plt.ylim([-180, 0])
    #plt.show()
    plt.savefig('noisy.pdf')

    maxbin = np.argmax(raw_fft[1:]) + 1 # make sure to ignore DC
    maxfreq = f[maxbin]
    sigpower = raw_fft[maxbin]**2
    noisepower = [0 if (i == 0 or i == maxbin) else raw_fft[i]**2 for i in range(len(raw_fft))]
    noisepower = np.sum(noisepower)

    sndr = sigpower/noisepower
    print(sndr)
    print(10*np.log10(sndr))
