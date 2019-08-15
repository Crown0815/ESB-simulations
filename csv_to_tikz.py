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


path_trm_example = '../Paper1_data/Data/Figure_2/48mer_Switching/ch4e3b-20170330-081510.trm'

path_staple = '../Paper1_data/Data/Figure_3/StapleHybridization/-02V to 02V 1Hz/Regeneration w 6HB_anchor/Functionalization/ch2e3b-20170327-173741.dyn'


class VrmPrinter:
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


class CsvAverage:
    def __init__(self, encoding='iso-8859-1', delimiter=';'):
        self.encoding = encoding
        self.delimiter = delimiter
        self.average = list()
        self.sources = list()
        self.line_count = None

    def add_source(self, path: str):
        with open(path, encoding=self.encoding) as file:
            count = sum(1 for _ in csv.reader(file))

        if self.line_count is None:
            self.line_count = count
        elif self.line_count != count:
            raise Exception("Files must contain same number of lines")

        self.sources.append(path)

    def print(self, col1: int = 0, col2: int = 1, x_offset: float = 0, show_column_names: bool = False):
        files = [open(source, encoding=self.encoding) for source in self.sources]
        readers = [csv.reader(file, delimiter=self.delimiter) for file in files]
        iterators = [iter(reader) for reader in readers]

        row_index = 0
        while row_index < self.line_count:
            rows = [next(iterator) for iterator in iterators]
            if row_index == 0:
                if show_column_names:
                    print(f'Column names are {rows[0][col1]} and {rows[0][col2]}')
            else:
                val1 = statistics.mean([float(row[col1]) for row in rows])
                val2 = statistics.mean([float(row[col2]) for row in rows])
                print(f'{val1+x_offset:.2f}\t\t{val2:.4f}\\\\')
            row_index += 1


vrm_printer = VrmPrinter()
csv_average = CsvAverage()

# csv_average.add_source(path_96bp_trm_1)
# csv_average.add_source(path_96bp_trm_2)
# csv_average.add_source(path_96bp_trm_3)
# csv_average.add_source(path_96bp_trm_4)

# csv_average.print(0, 3, -100, True)
# csv_average.print(0, 7)


with open(path_4hb_trm_1, encoding='iso-8859-1') as csv_file:
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
            # print(f'{float(row[0])-499.5:.2f}\t\t{row[2]}\\\\')

            # vrm
            # vrm_printer.add(float(row[1]), float(row[2]))

            # raw
            print(f'{row[0]}\t\t{row[6]}\\\\')

            line_count += 1
    # vrm_printer.print_normalized()
    print(f'Processed {line_count} lines.')
