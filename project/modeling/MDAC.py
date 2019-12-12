#!/usr/bin/env python3
import numpy as np

class MDAC:
    def __init__(self, vrange: (float, float), levels: int, gain: float) -> None:
        self.vrange = vrange
        self.levels = levels
        self.step = (vrange[1] - vrange[0]) / (levels-1)
        self.gain = gain

    def gen_output(self, adc_code: int, vin: float) -> float:
        equiv_voltage = adc_code*self.step + self.vrange[0]
        return self.gain * (vin - equiv_voltage)
