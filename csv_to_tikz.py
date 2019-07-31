import csv
import statistics

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

path_6hb_vrr_1 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e3a-20170329-160745.vrr'
path_6hb_vrr_2 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e4a-20170329-160745.vrr'
path_6hb_vrr_3 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e5a-20170329-160745.vrr'
path_6hb_vrr_4 = '../Paper1_data/Data/Figure_2/Origami Calibration/Calibration/ch4e6a-20170329-160745.vrr'

path_trm_example = '../Paper1_data/Data/Figure_2/48mer_Switching/ch4e3b-20170330-081510.trm'

path_staple = '../Paper1_data/Data/Figure_3/StapleHybridization/-02V to 02V 1Hz/Regeneration w 6HB_anchor/Functionalization/ch2e3b-20170327-173741.dyn'


class VrmPrinter():
    def __init__(self):
        self.voltage = None
        self.fluorescence = list()

        self.voltages = list()
        self.fluorescences = list()

    def add(self, voltage: float, fluorescence: float):
        if self.voltage is not None and self.voltage != voltage:
            self.voltages.append(self.voltage)
            self.fluorescences.append(statistics.mean(self.fluorescence))
            self.fluorescence.clear()
            self.voltage = None

        self.voltage = voltage
        self.fluorescence.append(fluorescence)

    def print(self):
        for v, f in zip(self.voltages, self.fluorescences):
            print(f'{v}\t\t{f}\\\\')

    def print_normalized(self):
        max_fluorescence = self.fluorescences[0]
        min_fluorescence = self.fluorescences[-1]
        for v, f in zip(self.voltages, self.fluorescences):
            # print(f'{v}\t\t{((f-min_fluorescence)/(max_fluorescence-min_fluorescence))}\\\\')
            print(f'{((f-min_fluorescence)/(max_fluorescence-min_fluorescence))}')


vrm_printer = VrmPrinter()

with open(path_6hb_vrr_4, encoding='iso-8859-1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # amplitude
            # print(f'{row[0]}\t\t{str(round(float(row[9])-float(row[10]),1))}\\\\')

            # upward motion after downward
            # print(f'{str(round(float(row[0])+0,2))}\t\t{row[3]}\\\\')

            # vrm
            vrm_printer.add(float(row[1]), float(row[2]))

            # raw
            # print(f'{row[0]}\t\t{row[1]}\\\\')

            line_count += 1
    vrm_printer.print_normalized()
    print(f'Processed {line_count} lines.')



