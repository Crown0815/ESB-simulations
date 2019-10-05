from interlinking import Linker
from surfaces import RandomSurface, HexagonalGrid, create_surface
import matplotlib.pyplot as plt
import tikzplotlib
import statistics
from math import sqrt
import tqdm
from csv_reader import SimpleCsv


class LinkingSimulation:
    def __init__(self, link_length: float, linkable_length: float = 0, grid_side_length=500,
                 grid_unit_length: float = 2.5, max_links: int = 1):
        self.link_length = link_length
        self.max_links = max_links
        self.linkable_length = linkable_length

        self.grid = HexagonalGrid(grid_unit_length)
        self.grid_side_length = grid_side_length

    def run(self, spot_distance: float):
        surface = RandomSurface(self.grid)
        surface.initialize(self.grid_side_length, self.grid_side_length, spot_distance, verbose=False)

        linker = Linker(surface.coordinates_with_padding, self.max_links, self.linkable_length)
        linker.create_links(self.link_length)

        linkables = list(surface.coordinates_within(linker.interlinked,
                                                    x_max=self.grid_side_length,
                                                    y_max=self.grid_side_length))
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

        print("Links:")
        print(r"Closed ratio: {:.1%} ± {:.1%})".format(sim.ratio_closed_links(), sim.ratio_closed_links_stdev()))
        print(r"Open ratio: {:.1%} ± {:.1%})".format(sim.ratio_open_links(), sim.ratio_open_links_stdev()))
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


def create_linked_surface(grid_size, size, distance, link_length, linkable_length, max_links, figure_size, show_plot=False):
    linking_simulation = LinkingSimulation(link_length, linkable_length, size, grid_size, max_links)
    result = linking_simulation.run(distance)
    Analyzer.report(result)
    Analyzer.visualization(result)
    tikzplotlib.save("./generated/linking_g{}_d{}_x{}_y{}_l{}_c{}_f{}.tex".format(grid_size, distance, size, size,
                                                                        link_length + 2 * linkable_length,
                                                                        max_links, figure_size))
    if show_plot: plt.show()


def create_statistics(grid_size, size, distance, link_length, linkable_length, max_links, run_count):
    simulation = LinkingSimulation(link_length, linkable_length, size, grid_size, max_links)
    simulation_statistics = LinkingSimulationStatistics()
    for _ in tqdm.tqdm(range(run_count)):
        simulation_statistics.append(simulation.run(distance))

    if simulation_statistics.count() < 1: return
    if simulation_statistics.count() == 1:
        Analyzer.report(simulation_statistics)
    else:
        Analyzer.report_statistics(simulation_statistics)


def with_args_from_file(method, file_path, header_rows=1):
    reader = SimpleCsv()
    reader.read(file_path, ",")
    for index, row in enumerate(reader.rows):
        if index < header_rows: continue
        method(*list(eval(x) for x in row))


if __name__ == '__main__':
    with_args_from_file(create_surface, "./simulation_parameters/surface_plots.csv")
    with_args_from_file(create_linked_surface, "./simulation_parameters/interlinking_plots.csv")
    with_args_from_file(create_statistics, "./simulation_parameters/interlinking_statistics.csv")
    
    # plt.show()
