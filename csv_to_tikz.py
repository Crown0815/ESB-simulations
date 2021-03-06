from csv_reader import *
from glob import glob
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import optimize
from math import *
import numpy as np

TRM_TIME = 0
TRM_DOWN_NORM = 2
TRM_DOWN_SMOOTH = 3
TRM_UP_NORM = 6
TRM_UP_SMOOTH = 7

path_origami_03_01V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.3-0.1V/Functionalization/ch4e3a-20170329-093634.dyn'
path_origami_025_015V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.25-0.15V/Functionalization/ch4e3a-20170329-103229.dyn'
path_origami_02_02V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.2-0.2V/Functionalization/ch4e3a-20170329-083358.dyn'
path_origami_01_03V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.1-0.3V/Functionalization/ch4e3a-20170329-095453.dyn'
path_origami_0_04V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/0-0.4V/Functionalization/ch4e3a-20170329-105020.dyn'

path_4hb_vrr_1 = '../Origami_Paper2/TRM/4HB/ch2e2a-20180808-181034.vrr'
path_4hb_vrr_2 = '../Origami_Paper2/TRM/4HB/ch2e1a-20180808-181034.vrr'
path_4hb_vrr_3 = '../Origami_Paper2/TRM/4HB/ch1e2g-20180802-115801.vrr'
path_4hb_vrr_4 = '../Origami_Paper2/TRM/4HB/ch1e1g-20180802-115801.vrr'
path_4hb_vrm = '../Origami_Paper2/TRM/4HB/preparedVrmData.csv'

path_4hb_vrm_lukas_1 = '../Origami_Paper2/AdditionalDataLukas/4HB/Id0_AH315_20x_SF_-0.4+0.1V_0.5k.dat'
path_4hb_vrm_lukas_2 = '../Origami_Paper2/AdditionalDataLukas/4HB/Id1_AH315_20x_SF_-0.4+0.1V_0.5k.dat'
path_4hb_vrm_lukas_3 = '../Origami_Paper2/AdditionalDataLukas/4HB/Id2_AH315_20x_SF_-0.4+0.1V_0.5k.dat'
path_4hb_vrm_lukas_4 = '../Origami_Paper2/AdditionalDataLukas/4HB/Id3_AH315_20x_SF_-0.4+0.1V_0.5k.dat'

path_4hb_trm_1 = '../Origami_Paper2/TRM/4HB/ch2e1a-20180808-182721.trm'
path_4hb_trm_2 = '../Origami_Paper2/TRM/4HB/ch2e2a-20180808-182721.trm'
path_4hb_trm_3 = '../Origami_Paper2/TRM/4HB/ch2e1a-20180808-212204.trm'
path_4hb_trm_4 = '../Origami_Paper2/TRM/4HB/ch2e2a-20180808-212204.trm'

paths_4hb_mg_tit = sorted(glob("../Origami_Paper2/Mg_Titration/4HB/*.trm"))

path_6hb_vrr_1 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e3a-20170329-160745.vrr'
path_6hb_vrr_2 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e4a-20170329-160745.vrr'
path_6hb_vrr_3 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e5a-20170329-160745.vrr'
path_6hb_vrr_4 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e6a-20170329-160745.vrr'

path_6hb_trm_1 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e3a-20170329-171550.trm'
path_6hb_trm_2 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e4a-20170329-171550.trm'
path_6hb_trm_3 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e5a-20170329-171550.trm'
path_6hb_trm_4 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e6a-20170329-171550.trm'

paths_6hb_mg_tit = sorted(glob("../Origami_Paper2/Mg_Titration/6HB/ch4e3a-*.trm"))

path_48bp_trm_1 = '../Origami_Paper2/TRM/48bp/ch1e4g-20180829-170351.trm'
path_48bp_trm_2 = '../Origami_Paper2/TRM/48bp/ch1e3g-20180829-170351.trm'
path_48bp_trm_3 = '../Origami_Paper2/TRM/48bp/ch1e2g-20180829-170351.trm'
path_48bp_trm_4 = '../Origami_Paper2/TRM/48bp/ch1e1g-20180829-170351.trm'

path_48bp_vrr_1 = '../Paper1_data/Data/Figure_2/48mer Calibration/124618_Origami Buffer/ch1e3-20170410-124618.vrr'
path_48bp_vrr_2 = '../Paper1_data/Data/Figure_2/48mer Calibration/124738_Origami Buffer/ch1e4-20170410-124738.vrr'
path_48bp_vrr_3 = '../Paper1_data/Data/Figure_2/48mer Calibration/124908_Origami Buffer/ch1e5-20170410-124908.vrr'
path_48bp_vrr_4 = '../Paper1_data/Data/Figure_2/48mer Calibration/125023_Origami Buffer/ch1e6-20170410-125023.vrr'

paths_48bp_mg_tit = sorted(glob("../Origami_Paper2/Mg_Titration/48mer/*.trm"))

path_96bp_trm_1 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e3a-20180816-153502.trm'
path_96bp_trm_2 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e4a-20180816-153502.trm'
path_96bp_trm_3 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e5a-20180816-153502.trm'
path_96bp_trm_4 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e6a-20180816-153502.trm'

path_96bp_vrr_1 = '../Origami_Paper2/TRM/96bp/ch1e3b-20180925-111215.vrr'
path_96bp_vrr_2 = '../Origami_Paper2/TRM/96bp/ch1e4b-20180925-111215.vrr'
path_96bp_vrr_3 = '../Origami_Paper2/TRM/96bp/ch1e5b-20180925-111215.vrr'
path_96bp_vrr_4 = '../Origami_Paper2/TRM/96bp/ch1e6b-20180925-111215.vrr'

paths_96bp_mg_tit = sorted(glob("../Origami_Paper2/Mg_Titration/96mer/*.trm"))


path_trm_example = '../Paper1_data/Data/Figure_2/48mer_Switching/ch4e3b-20170330-081510.trm'

path_staple = '../Paper1_data/Data/Figure_3/StapleHybridization/-02V to 02V 1Hz/Regeneration w 6HB_anchor/Functionalization/ch2e3b-20170327-173741.dyn'

path_incubation_vs_live = '../OrigamiUnpublished/IncubationVsLiveImmobilization.csv'
path_real_time_binding_dr = '../OrigamiUnpublished/RealTimeBindingInDynamicResponse.csv'
path_size_comparison = '../OrigamiUnpublished/SizeComparisons.csv'



# vrm_printer = VrmPrinter()
# csv_average = CsvAverage()

# csv_average.add_source(path_4hb_trm_1)
# csv_average.add_source(path_4hb_trm_2)
# csv_average.add_source(path_4hb_trm_3)
# csv_average.add_source(path_4hb_trm_4)

# csv_average.print(0, 3)
# x = list(csv_average.values(TRM_TIME, -499.5)) + list(csv_average.values(TRM_TIME))
# y = list(csv_average.values(TRM_DOWN_NORM)) + list(csv_average.values(TRM_UP_NORM))

# y_smooth = savgol_filter(y, 11, 5)
# SimpleTikZPrinter.print(x, y_smooth)
# csv_average.print(0, 7)

reader = SimpleCsv()

path = path_size_comparison
reader.read(path, ',')

fig, (ax1) = plt.subplots(1)

for index in range(0, 10, 2):
    x = list(reader.values(index+0))
    y = list(reader.values(index+1))

    print('')
    print('\\addplot [color=mycolor1] table{%')
    SimpleTikZPrinter.print(x, y)
    print("};\n")

    ax1.plot(x, y)

# Fit for observable rate of Anti-Her2

# fitfunc = lambda p, var: ((var > p[2]) * p[0] * (1-np.exp(p[1] * (var-p[2])))) + p[3]  # Target function
# errfunc = lambda p, var, fix: fitfunc(p, var) - fix  # Distance to the target function
# p0 = (350, -0.3, 20, 1650.)  # Initial guess for the parameters
# p1, success = optimize.leastsq(errfunc, p0[:], args=(x, y))
# y_fit = [fitfunc(p1, x_i) for x_i in x]
# ax1.plot(x, y_fit)
# print(p1)
#
# print('\\addplot [color=mycolor1] table{%')
# SimpleTikZPrinter.print(x, y_fit)
# print("};\n")

plt.show()


# paths = paths_96bp_mg_tit
# fig, (ax1, ax2) = plt.subplots(2)
# for index, path in enumerate(paths, start=1):
#     if index % 2 == 0:
#         continue
#     reader.read(path)
#     color = "mycolor1!"+str(100*index/len(paths))+"!mycolor2"
#     print('\\addplot [color='+color+'] table{%')
#     x = list(reader.values(TRM_TIME, -100)) + list(reader.values(TRM_TIME))
#     y = list(reader.values(TRM_DOWN_NORM)) + list(reader.values(TRM_UP_NORM))
#
#     y_smooth = savgol_filter(y, 7, 1)
#     SimpleTikZPrinter.print(x, y_smooth)
#     print("};\n")
#
#     ax1.plot(x, y)
#     ax2.plot(x, y_smooth)
# plt.show()
