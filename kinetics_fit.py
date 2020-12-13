import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import os
from glob import glob
from csv_reader import *

reader = SimpleCsv()
base_path = "/Users/felixkroner/Documents/ScientificWork/Moving-DNA-Origami/ExperimentData/origami_dna_hybridization_data/"

cnl_a_b_96 = "073612_CrownOrigami_48merAnd96mer_50nMAnd125nM Hybridizationtest/C2/50nM cNL A and B96/"
cnl_a_b = "083526_CrownOrigami_48mer_50nM Hybridizationtest/C2/Autosampler cNL A and B/"

cnl_a_vs_b = "105046_CrownOrigami_48mer_HybridizationsAtDifferentPotentials/C1/"

cnl_a_b_ofb = "094809_CrownOrigami_48merVS96_HybridizationsAtDifferentPotentials_OrigamiBuffer/C1/Autosampler cNL A48+B48 OrigamiBuffer/"


def applied_potential_sort(folder_name):
    return float(folder_name.split("to ")[1].replace("0", "0.",1))

base_experiment = base_path+cnl_a_vs_b

potentials = list(name for name in os.listdir(base_experiment) if os.path.isdir(base_experiment+name))
print(potentials)

fig, (ax1) = plt.subplots(1)


def func(x, amplitude, rate_constant, offset):
    return amplitude * (1-np.exp(-rate_constant * x)) + offset


count = len(potentials)
potentials.sort(key=applied_potential_sort)
print(list(applied_potential_sort(p) for p in potentials))

print('')
print(f'\\addplot [color=mycolor1] table{{%')
for index, potential in enumerate(potentials):
    path = glob(base_experiment + potential + "/Regeneration w A+B/Functionalization/ch1e2a*.dyn")[0]
    reader.read(path, ';')

    x_data = np.array(list(reader.values(0)))
    y_data = list(reader.values(9))
    y_ref_points = y_data[0:10]
    y_ref = sum(y_ref_points)/len(y_ref_points)
    y_norm = np.array(list(y_value/y_ref for y_value in y_data))

    plt.plot(x_data, y_norm, 'b-', label='raw data')
    max_fit_index = 500
    min_fit_index = 22
    plt.plot(x_data[min_fit_index:max_fit_index], y_norm[min_fit_index:max_fit_index], 'r-', label='fit data')
    #plt.show()

    popt, pcov = curve_fit(func, x_data[min_fit_index:max_fit_index], y_norm[min_fit_index:max_fit_index], bounds=([.8, .002, -10.], [10., .1, 1.0]))
    amp, rate, offset = tuple(popt);
    time_constant = 1./rate
    plt.plot(x_data[min_fit_index:], func(x_data[min_fit_index:], *popt), 'r-', label='fit: amp=%5.3f, tc=%5.3f, offset=%5.3f' % (amp, time_constant, offset))
    plt.legend()
    plt.show()

    SimpleTikZPrinter.print([applied_potential_sort(potential)], [time_constant])
print("};\n")



