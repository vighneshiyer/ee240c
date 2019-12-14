#!/usr/bin/env python3
from Stage import Stage
import numpy as np

class PipelineADC:
    def __init__(self, vrange: (float, float), offset_var: float):
        self.stages = [
                Stage(vrange, levels=4, gain=3, offset_var=offset_var, vin_signed=False),
                Stage(vrange, levels=4, gain=3, offset_var=offset_var, vin_signed=True),
                ]

    def output(self, vin:float):
        print("vin: ", vin)
        v = vin
        adc_codes = []
        #print("residuals")
        for s in self.stages:
            out = s.output(v)
            adc_codes.append(out[0])
            v = out[1]# - self.stages[0].mdac.midpoint
            #print(v)
        print("adc_codes, ", adc_codes[0], adc_codes[1])
        print(adc_codes[0]*4 + (adc_codes[1])*2)

if __name__ == "__main__":
    adc = PipelineADC((0, 1.2), 0)
    vals = np.linspace(0, 1.2, 100)
    out = [adc.output(x) for x in vals]
