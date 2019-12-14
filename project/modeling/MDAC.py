#!/usr/bin/env python3
import numpy as np

class MDAC:
    def __init__(self, vrange: (float, float), levels: int, gain: float, vin_signed: bool) -> None:
        self.vrange = vrange
        self.levels = levels
        self.step = (vrange[1] - vrange[0]) / (levels-1)
        self.gain = gain
        self.midpoint = (self.vrange[1] - self.vrange[0]) / 2
        self.vin_signed = vin_signed

    def gen_residual(self, adc_code: int, vin: float) -> float:
        equiv_voltage = adc_code*self.step + self.vrange[0]
        #if not self.vin_signed:
            #raw_val = (self.gain * (equiv_voltage - vin)) + self.midpoint
        #else:
        raw_val = (self.gain * (equiv_voltage - vin)) + (self.vrange[1] - self.vrange[0])/2
        return np.clip(raw_val, self.vrange[0], self.vrange[1])
        #return self.gain * (vin - equiv_voltage)
