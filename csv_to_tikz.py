from csv_reader import *

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

path_4hb_trm_1 = '../Origami_Paper2/TRM/4HB/ch2e1a-20180808-182721.trm'
path_4hb_trm_2 = '../Origami_Paper2/TRM/4HB/ch2e2a-20180808-182721.trm'
path_4hb_trm_3 = '../Origami_Paper2/TRM/4HB/ch2e1a-20180808-212204.trm'
path_4hb_trm_4 = '../Origami_Paper2/TRM/4HB/ch2e2a-20180808-212204.trm'

path_6hb_vrr_1 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e3a-20170329-160745.vrr'
path_6hb_vrr_2 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e4a-20170329-160745.vrr'
path_6hb_vrr_3 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e5a-20170329-160745.vrr'
path_6hb_vrr_4 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e6a-20170329-160745.vrr'

path_6hb_trm_1 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e3a-20170329-171550.trm'
path_6hb_trm_2 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e4a-20170329-171550.trm'
path_6hb_trm_3 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e5a-20170329-171550.trm'
path_6hb_trm_4 = '../Paper1_data/Data/Figure_2/Origami Switching/ch4e6a-20170329-171550.trm'

path_48bp_trm_1 = '../Origami_Paper2/TRM/48bp/ch1e4g-20180829-170351.trm'
path_48bp_trm_2 = '../Origami_Paper2/TRM/48bp/ch1e3g-20180829-170351.trm'
path_48bp_trm_3 = '../Origami_Paper2/TRM/48bp/ch1e2g-20180829-170351.trm'
path_48bp_trm_4 = '../Origami_Paper2/TRM/48bp/ch1e1g-20180829-170351.trm'

path_48bp_vrr_1 = '../Paper1_data/Data/Figure_2/48mer Calibration/124618_Origami Buffer/ch1e3-20170410-124618.vrr'
path_48bp_vrr_2 = '../Paper1_data/Data/Figure_2/48mer Calibration/124738_Origami Buffer/ch1e4-20170410-124738.vrr'
path_48bp_vrr_3 = '../Paper1_data/Data/Figure_2/48mer Calibration/124908_Origami Buffer/ch1e5-20170410-124908.vrr'
path_48bp_vrr_4 = '../Paper1_data/Data/Figure_2/48mer Calibration/125023_Origami Buffer/ch1e6-20170410-125023.vrr'

path_96bp_trm_1 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e3a-20180816-153502.trm'
path_96bp_trm_2 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e4a-20180816-153502.trm'
path_96bp_trm_3 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e5a-20180816-153502.trm'
path_96bp_trm_4 = '../Origami_Paper2/TRM/96bp/TRM_old/ch1e6a-20180816-153502.trm'

path_96bp_vrr_1 = '../Origami_Paper2/TRM/96bp/ch1e3b-20180925-111215.vrr'
path_96bp_vrr_2 = '../Origami_Paper2/TRM/96bp/ch1e4b-20180925-111215.vrr'
path_96bp_vrr_3 = '../Origami_Paper2/TRM/96bp/ch1e5b-20180925-111215.vrr'
path_96bp_vrr_4 = '../Origami_Paper2/TRM/96bp/ch1e6b-20180925-111215.vrr'


path_trm_example = '../Paper1_data/Data/Figure_2/48mer_Switching/ch4e3b-20170330-081510.trm'

path_staple = '../Paper1_data/Data/Figure_3/StapleHybridization/-02V to 02V 1Hz/Regeneration w 6HB_anchor/Functionalization/ch2e3b-20170327-173741.dyn'


# vrm_printer = VrmPrinter()
# csv_average = CsvAverage()

# csv_average.add_source(path_96bp_trm_1)
# csv_average.add_source(path_96bp_trm_2)
# csv_average.add_source(path_96bp_trm_3)
# csv_average.add_source(path_96bp_trm_4)

# csv_average.print(0, 3, -100, True)
# csv_average.print(0, 7)



