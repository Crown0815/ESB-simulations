import os
from glob import glob
from scipy.signal import savgol_filter

from csv_reader import *
import matplotlib.pyplot as plt

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

count = len(potentials)
potentials.sort(key=applied_potential_sort)
print(list(applied_potential_sort(p) for p in potentials))
for index, potential in enumerate(potentials):
    path = glob(base_experiment + potential + "/Regeneration w A+B/Functionalization/ch1e2a*.dyn")[0]
    reader.read(path, ';')

    x = list(reader.values(0))
    y = list(reader.values(9))
    y_ref_points = y[0:10]
    y_ref = sum(y_ref_points)/len(y_ref_points)
    y_norm = list(y_value/y_ref for y_value in y)
    y_smooth = savgol_filter(y_norm, 11, 3)

    print('')
    print(f'\\addplot [color=mycolor2!{100.0/(count-1)*(index)}!mycolor1] table{{%')
    SimpleTikZPrinter.print(x, y_smooth)
    print("};\n")

    ax1.plot(x, y_smooth)

plt.show()