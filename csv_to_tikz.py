import csv

path_origami_03_01V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.3-0.1V/Functionalization/ch4e3a-20170329-093634.dyn'
path_origami_025_015V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.25-0.15V/Functionalization/ch4e3a-20170329-103229.dyn'
path_origami_02_02V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.2-0.2V/Functionalization/ch4e3a-20170329-083358.dyn'
path_origami_01_03V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/-0.1-0.3V/Functionalization/ch4e3a-20170329-095453.dyn'
path_origami_0_04V_g = '../Paper1_data/Data/Figure_3/OrigamiHybridization/0-0.4V/Functionalization/ch4e3a-20170329-105020.dyn'

path_trm_example = '../Paper1_data/Data/Figure_2/48mer_Switching/ch4e3b-20170330-081510.trm'

path_staple = '../Paper1_data/Data/Figure_3/StapleHybridization/-02V to 02V 1Hz/Regeneration w 6HB_anchor/Functionalization/ch2e3b-20170327-173741.dyn'

with open(path_trm_example, encoding='iso-8859-1') as csv_file:
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
            print(f'{str(round(float(row[0])+0,2))}\t\t{row[3]}\\\\')

            # raw
            # print(f'{row[0]}\t\t{row[3]}\\\\')
            line_count += 1
    print(f'Processed {line_count} lines.')
