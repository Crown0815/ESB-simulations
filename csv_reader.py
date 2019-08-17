import csv
import statistics


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
            print(f'{v}\t\t{((f-min_fluorescence)/(max_fluorescence-min_fluorescence))}\\\\')
            # print(f'{((f-min_fluorescence)/(max_fluorescence-min_fluorescence))}')

    def read(self, path: str, delimiter: str=';', encoding: str = 'iso-8859-1'):
        with open(path, encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            rows = [row for row in reader]
            line_count = 0
            for row in rows:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                else:
                    self.add(float(row[1]), float(row[2]))
                line_count += 1
            print(f'Read {line_count} lines.')


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


class SimpleCsv:
    def __init__(self):
        self.rows = list()

    def read(self, path: str, delimiter: str=';', encoding: str = 'iso-8859-1', show_read_line_count=False):
        with open(path, encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            self.rows = [row for row in reader]

            if show_read_line_count:
                print(f'Read {len(self.rows)} lines.')

    def print(self, col1: int=0, col2: int=1, x_offset: float=0, row_separator: str="", print_every_nth: int=1, show_column_names: bool=False):
            line_count = 0
            for row in self.rows:
                if line_count == 0:
                    if show_column_names:
                        print(f'Column names are {", ".join(row)}')
                elif line_count % print_every_nth != 0:
                    line_count += 1
                    continue
                else:
                    print(f'{float(row[col1])+x_offset:.2f}\t\t{row[col2]}{row_separator}')
                line_count += 1
