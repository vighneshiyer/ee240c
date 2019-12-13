#!/usr/bin/env python3
from ADC import ADC
from MDAC import MDAC
import numpy as np

class Stage:
    def __init__(self, vrange: (float, float), levels: int, gain: float):
        self.adc = ADC(vrange, levels, mid_step=True)
        self.mdac = MDAC(vrange, levels, gain)

    def output(self, vin: float) -> (int, float):
        adc_code = self.adc.convert(vin)[0]
        residual = self.mdac.gen_residual(adc_code, vin)
        return (adc_code, residual)

if __name__ == "__main__":
    vrange = (0, 1.2)
    s = Stage(vrange, levels=2**2, gain=2**2)
    fs = 25e6
    #vals = [np.sin(2*np.pi*100e3*i/fs) for i in range(1024)]
    #vals_norm = [x* 0.6 + 0.6 for x in vals]
    vals_norm = np.linspace(0, 1.2, 1000)
    out = [s.output(x) for x in vals_norm]
    import matplotlib.pyplot as plt
    fig,ax = plt.subplots(1, 2)
    ax[0].plot(vals_norm, '.')
    ax[0].plot([x[1] for x in out], '.')
    ax[1].plot([x[0] for x in out], '.')
    plt.show()

