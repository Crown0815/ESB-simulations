from interlinking import Linker
from surfaces import *
import matplotlib.pyplot as plt
import tikzplotlib
import statistics
from math import sqrt
import tqdm
from csv_reader import SimpleCsv
import sys
from datetime import datetime


class LinkingSimulation:
    def __init__(self, link_length: float, linkable_length: float = 0, grid_width=500, grid_height=500,
                 grid_unit_length: float = 2.5, max_links: int = 1):
        self.link_length = link_length
        self.max_links = max_links
        self.linkable_length = linkable_length

        self.grid = HexagonalGrid(grid_unit_length)
        self.grid_width = grid_width
        self.grid_height = grid_height

    def run(self, spot_distance: float):
        surface = RandomSurface(self.grid)
        surface.initialize(self.grid_width, self.grid_height, spot_distance, verbose=False)

        linker = Linker(surface.coordinates_with_padding, self.max_links, self.linkable_length)
        linker.create_links(self.link_length)

        linkables = list(surface.coordinates_within(linker.interlinked,
                                                    x_max=self.grid_width,
                                                    y_max=self.grid_height))
        return LinkingSimulationResult(surface, linkables)


class LinkingSimulationResult:
    def __init__(self, surface, linkables):
        self.surface = surface
        self.linkables = linkables
        self.links = self.links_from(linkables)

    @staticmethod
    def links_from(linkables):
        links = list()
        for linkable in linkables:
            for link in linkable.links:
                if link not in links:
                    links.append(link)
        return links

    def count_of_links(self):
        return len(self.links)

    def count_of_closed_links(self):
        return sum(not link.is_open() for link in self.links)

    def count_of_open_links(self):
        return sum(link.is_open() for link in self.links)

    def ratio_closed_links(self):
        return self.count_of_closed_links() / len(self.links)

    def ratio_open_links(self):
        return 1 - self.ratio_closed_links()

    def count_of_linkables(self):
        return len(self.linkables)

    def count_of_linked_linkables(self, linked_threshold: int = 1):
        return sum(linkable.is_linked(linked_threshold) for linkable in self.linkables)

    def count_of_unlinked_linkables(self, linked_threshold: int = 1):
        return sum(not linkable.is_linked(linked_threshold) for linkable in self.linkables)

    def ratio_linked_linkables(self, linked_threshold: int = 1):
        return self.count_of_linked_linkables(linked_threshold) / len(self.linkables)

    def ratio_unlinked_linkables(self, linked_threshold: int = 1):
        return 1 - self.ratio_linked_linkables(linked_threshold)


class LinkingSimulationStatistics:
    def __init__(self):
        self.simulation_results = list()

    def append(self, item):
        self.simulation_results.append(item)

    def count_of_links(self):
        return self.mean(lambda x: x.count_of_links())

    def count_of_closed_links(self):
        return self.mean(lambda x: x.count_of_closed_links())

    def count_of_open_links(self):
        return self.mean(lambda x: x.count_of_open_links())

    def ratio_closed_links(self):
        return self.mean(lambda x: x.ratio_closed_links())

    def ratio_open_links(self):
        return self.mean(lambda x: x.ratio_open_links())

    def count_of_linkables(self):
        return self.mean(lambda x: x.count_of_linkables())

    def count_of_linked_linkables(self, linked_threshold: int = 1):
        return self.mean(lambda x: x.count_of_linked_linkables(linked_threshold))

    def count_of_unlinked_linkables(self, linked_threshold: int = 1):
        return self.mean(lambda x: x.count_of_unlinked_linkables(linked_threshold))

    def ratio_linked_linkables(self, linked_threshold: int = 1):
        return self.mean(lambda x: x.ratio_linked_linkables(linked_threshold))

    def ratio_unlinked_linkables(self, linked_threshold: int = 1):
        return self.mean(lambda x: x.ratio_unlinked_linkables(linked_threshold))

    def ratio_closed_links_stdev(self):
        return self.stdev(lambda x: x.ratio_closed_links())

    def ratio_open_links_stdev(self):
        return self.stdev(lambda x: x.ratio_open_links())

    def ratio_linked_linkables_stdev(self, linked_threshold: int = 1):
        return self.stdev(lambda x: x.ratio_linked_linkables(linked_threshold))

    def ratio_unlinked_linkables_stdev(self, linked_threshold: int = 1):
        return self.stdev(lambda x: x.ratio_unlinked_linkables(linked_threshold))

    def ratio_closed_links_stderr(self):
        return self.ratio_closed_links_stdev()/sqrt(self.count())

    def ratio_open_links_stderr(self):
        return self.ratio_open_links_stdev()/sqrt(self.count())

    def ratio_linked_linkables_stderr(self, linked_threshold: int = 1):
        return self.ratio_linked_linkables_stdev(linked_threshold)/sqrt(self.count())

    def ratio_unlinked_linkables_stderr(self, linked_threshold: int = 1):
        return self.ratio_unlinked_linkables_stdev(linked_threshold)/sqrt(self.count())

    def mean_with_stdev(self, resolver):
        return self.mean(resolver), self.stdev(resolver)

    def mean(self, resolver):
        return self.calculate_statistics(lambda x: statistics.mean(x), resolver)

    def stdev(self, resolver):
        return self.calculate_statistics(lambda x: statistics.stdev(x), resolver)

    def calculate_statistics(self, statistic, resolver):
        return statistic(resolver(x) for x in self.simulation_results)

    def count(self):
        return len(self.simulation_results)


class Analyzer:

    @staticmethod
    def report(simulation):
        sim = simulation
        print()
        print("----------------------------")
        print("Linkables:")
        linkable_count = sim.count_of_linkables()
        print("Linked = {}/{} (ratio: {:.1%})".format(sim.count_of_linked_linkables(), linkable_count,
                                                      sim.ratio_linked_linkables()))
        print("Unlinked = {}/{} (ratio: {:.1%})".format(sim.count_of_unlinked_linkables(), linkable_count,
                                                        sim.ratio_unlinked_linkables()))

        print("Links:")
        link_count = sim.count_of_links()
        print("Closed = {}/{} (ratio: {:.1%})".format(sim.count_of_closed_links(), link_count,
                                                      sim.ratio_closed_links()))
        print("Open = {}/{} (ratio: {:.1%})".format(sim.count_of_open_links(), link_count, sim.ratio_open_links()))

    @staticmethod
    def report_statistics(simulation):
        sim = simulation
        print()
        print("----------------------------")
        print("Uncertainties as standard deviations")
        print()
        print("Linkables:")
        print(r"Linked ratio: {:.1%} ± {:.1%})".format(sim.ratio_linked_linkables(), sim.ratio_linked_linkables_stdev()))
        print(r"Unlinked ratio: {:.1%} ± {:.1%})".format(sim.ratio_unlinked_linkables(), sim.ratio_unlinked_linkables_stdev()))
        print()
        linked = sim.ratio_linked_linkables_stdev()
        print(r"Formatted: (X,  {:.1%})  +- ({:.1%}, {:.1%}))".format(sim.ratio_linked_linkables(), linked, linked))
        print(r"Formatted: (X,  {:.1%}))".format(sim.ratio_unlinked_linkables()))
        print()
        print("Links:")
        closed = sim.ratio_closed_links_stdev()
        print(r"Closed ratio: {:.1%} ± {:.1%})".format(sim.ratio_closed_links(), closed))
        print(r"Open ratio: {:.1%} ± {:.1%})".format(sim.ratio_open_links(), sim.ratio_open_links_stdev()))
        print()
        print(r"Formatted: (X,  {:.1%})  +- ({:.1%}, {:.1%}))".format(sim.ratio_closed_links(), closed, closed))
        print(r"Formatted: (X,  {:.1%}))".format(sim.ratio_open_links()))
        print()
        print("----------------------------")
        print()

    @staticmethod
    def visualization(simulation):
        sim = simulation
        figure, axis = sim.surface.visualization()
        dots = list()

        # draw links between interlinked linkables
        for link in sim.links:
            if link.is_open(): continue
            linkables = [link.linked1, link.linked2]
            dots = dots + linkables

            x_values = sim.surface.x_of(linkables)
            y_values = sim.surface.y_of(linkables)
            axis.plot(x_values, y_values, color="red")

        # draw non-padding linkables
        dots_to_draw = list(d for d in dots if d in sim.linkables)
        x_values = sim.surface.x_of(dots_to_draw)
        y_values = sim.surface.y_of(dots_to_draw)
        axis.plot(x_values, y_values, 'o', color="red")

        # draw padding linkables
        x_to_draw = list(d for d in dots if d not in sim.linkables)
        x_values = sim.surface.x_of(x_to_draw)
        y_values = sim.surface.y_of(x_to_draw)
        axis.plot(x_values, y_values, 'x', color="red")

        return figure, axis


def create_linked_surface(grid_size, width, height, distance, link_length, linkable_length, max_links, figure_size, show_plot=True):
    if figure_size == 0: return
    linking_simulation = LinkingSimulation(link_length, linkable_length, width, height, grid_size, max_links)
    result = linking_simulation.run(distance)
    Analyzer.report(result)
    Analyzer.visualization(result)
    tikzplotlib.save("./generated/linking_g{}_d{}_x{}_y{}_l{}_c{}_f{}.tex".format(grid_size, distance, width, height,
                                                                        link_length + 2 * linkable_length,
                                                                        max_links, figure_size))
    if show_plot: plt.show()


def create_statistics(grid_size, width, height, distance, link_length, linkable_length, max_links, run_count):
    simulation = LinkingSimulation(link_length, linkable_length, width, height, grid_size, max_links)
    simulation_statistics = LinkingSimulationStatistics()
    for _ in tqdm.tqdm(range(run_count)):
        simulation_statistics.append(simulation.run(distance))

    if simulation_statistics.count() < 1: return
    if simulation_statistics.count() == 1:
        Analyzer.report(simulation_statistics)
    else:
        Analyzer.report_statistics(simulation_statistics)


def create_surface_from_drop_statistics(grid_size, simulation_area, total_area, volume, concentration, immobilization_probability, figure_size):
    grid = HexagonalGrid(grid_size)
    surface = RandomSurface(grid)
    means = list()
    stdevs = list()

    number_of_targets = volume * concentration * constants.Avogadro * immobilization_probability

    sys.stdout = open(fr'generated/surface_from_drop_with_{number_of_targets:.0}_targets.csv', 'w')

    print("surface, label, distance_average, distance_stddev")
    surface_count = 10
    for index in range(surface_count):
        surface.distribute_targets_from_liquid_drop(simulation_area, total_area, volume, concentration, immobilization_probability)
        closest_neighbors = surface.distances_to_closest_neighbor()
        # print(fr"Distances: {closest_neighbors}")
        print(fr"{index:3}, {index:3}, {statistics.mean(closest_neighbors):.2f}, {statistics.stdev(closest_neighbors):.2f}")
        means.append(statistics.mean(closest_neighbors))
        stdevs.append(statistics.stdev(closest_neighbors))

    print(fr"{surface_count+1}, mean, {statistics.mean(means):.2f}, {statistics.mean(stdevs):.2f}")
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    # print(fr"stddev, {statistics.stdev(means):.2f}, {statistics.stdev(stdevs):.2f}")
    surface.visualization(figure_size)
    tikzplotlib.save(f"./generated/surface_from_drop_g{grid_size}_sa{simulation_area}_d{sqrt(total_area / pi / 2) * 2}_"
                     f"n{number_of_targets:.0}.tex")


def with_args_from_file(method, file_path, header_rows=1):
    reader = SimpleCsv()
    reader.read(file_path, ",")
    for index, row in enumerate(reader.rows):
        print(row)
        if index < header_rows: continue
        method(*list(eval(x) for x in row))


if __name__ == '__main__':
    # sys.stdout = open('generated/interlinking_simulation.txt', 'w')
    print("Simulation started at ", datetime.now())
    # with_args_from_file(create_surface, "./simulation_parameters/surface_plots.csv")
    with_args_from_file(create_surface_from_drop_statistics, "./simulation_parameters/surface_from_drop_plots.csv")
    # with_args_from_file(create_linked_surface, "./simulation_parameters/interlinking_plots.csv")
    # with_args_from_file(create_statistics, "./simulation_parameters/interlinking_statistics.csv")
    # sys.stdout.close()
    # plt.show()
