#!/usr/bin/env python3
import numpy as np

class ADC:
    # levels = number of distinct digital code values
    # levels = 2**bits
    # mid_step = makes the digital code transitions in the middle of each step
    def __init__(self, vrange: (float, float), levels: int, mid_step: bool = True, offset_var: float = 0) -> None:
        self.vrange = vrange
        self.levels = levels
        self.step = (vrange[1] - vrange[0]) / (levels-1)
        if not mid_step:
            self.transitions = [self.step*i for i in range(1, levels)]
        else:
            self.transitions = [(self.step*i - self.step/2) * np.random.normal(1, offset_var) for i in range(1, levels)]

    # returns (conversion result, residual)
    def convert(self, val: float) -> (int, float):
        result = None
        for i, tran in enumerate(self.transitions):
            if val < tran:
                result = i
                break
        if result is None:
            result = self.levels - 1
        equiv_voltage = result*self.step + self.vrange[0]
        return (result, equiv_voltage - val)

if __name__ == "__main__":
    vmin = 0
    vmax = 1.2
    adc = ADC((vmin, vmax), 2**2)
    vals = np.linspace(vmin, vmax, 1000)
    out = [adc.convert(x) for x in vals]
    print(adc.transitions)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2)
    ax[0].plot(vals, [x[0] for x in out])
    ax[1].plot(vals, [x[1] for x in out])
    ax[1].axhline(y=adc.step/2, color='r', linestyle='--')
    ax[1].axhline(y=-adc.step/2, color='r', linestyle='--')
    plt.show()
