from math import *

tau = 1.6


def relative_electrode_charge(t):
    return 1 - exp(-t/tau)


if __name__ == "__main__":
    times = [x*0.1 for x in range(0, 101, 1)]  # potential range
    for time in times:
        print(f'{time:.2f}\t\t{relative_electrode_charge(time):.4f}\\\\')
