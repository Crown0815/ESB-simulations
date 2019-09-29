from interlinking import Linker
from surfaces import RandomSurface, HexagonalGrid
import matplotlib.pyplot as plt
import tikzplotlib


class LinkingSimulation:
    def __init__(self, link_length: float, linkable_length: float = 0, grid_side_length=500,
                 grid_unit_length: float = 2.5, max_links: int = 1):
        self.surface = None
        self.linker = None
        self.links = list()
        self.linkables = list()

        self.link_length = link_length
        self.max_links = max_links
        self.linkable_length = linkable_length

        self.grid = HexagonalGrid(grid_unit_length)
        self.grid_side_length = grid_side_length

    def run(self, spot_distance: float):
        surface = RandomSurface(self.grid)
        surface.initialize(self.grid_side_length, self.grid_side_length, spot_distance)

        linker = Linker(surface.coordinates_with_padding, self.max_links, self.linkable_length)
        linker.create_links(self.link_length)

        self.linkables = list(surface.coordinates_within(linker.interlinked,
                                                         x_max=self.grid_side_length,
                                                         y_max=self.grid_side_length))
        self.links = self.links_from(self.linkables)
        self.surface = surface
        self.linker = linker

    @staticmethod
    def links_from(linkables):
        links = list()
        for linkable in linkables:
            for link in linkable.links:
                if link not in links:
                    links.append(link)
        return links

    def count_of_closed_links(self):
        return sum(not link.is_open() for link in self.links)

    def count_of_open_links(self):
        return sum(link.is_open() for link in self.links)

    def count_of_linked_linkables(self, linked_threshold: int = 1):
        return sum(linkable.is_linked(linked_threshold) for linkable in self.linkables)

    def count_of_unlinked_linkables(self, linked_threshold: int = 1):
        return sum(not linkable.is_linked(linked_threshold) for linkable in self.linkables)

    def ratio_closed_links(self):
        return self.count_of_closed_links() / len(self.links)

    def ratio_open_links(self):
        return 1 - self.ratio_closed_links()

    def ratio_linked_linkables(self, linked_threshold: int = 1):
        return self.count_of_linked_linkables(linked_threshold) / len(self.linkables)

    def ratio_unlinked_linkables(self, linked_threshold: int = 1):
        return 1 - self.ratio_linked_linkables(linked_threshold)


class Analyzer:

    @staticmethod
    def report(simulation):
        sim = simulation
        print()
        print("----------------------------")
        print("Linkables:")
        linkable_count = len(sim.linkables)
        print("Linked = {}/{} (ratio: {:.1%})".format(sim.count_of_linked_linkables(), linkable_count,
                                                      sim.ratio_linked_linkables()))
        print("Unlinked = {}/{} (ratio: {:.1%})".format(sim.count_of_unlinked_linkables(), linkable_count,
                                                        sim.ratio_unlinked_linkables()))

        print("Links:")
        link_count = len(sim.links)
        print("Closed = {}/{} (ratio: {:.1%})".format(sim.count_of_closed_links(), link_count,
                                                      sim.ratio_closed_links()))
        print("Open = {}/{} (ratio: {:.1%})".format(sim.count_of_open_links(), link_count, sim.ratio_open_links()))

    @staticmethod
    def visualization(simulation):
        sim = simulation
        figure, axis = sim.surface.visualization()
        dots = list()
        for link in sim.links:
            if link.is_open(): continue
            linkables = [link.linked1, link.linked2]
            dots = dots + linkables

            x_values = sim.surface.x_of(linkables)
            y_values = sim.surface.y_of(linkables)
            axis.plot(x_values, y_values, color="red")

        dots_to_draw = list(d for d in dots if d in sim.linkables)
        x_values = sim.surface.x_of(dots_to_draw)
        y_values = sim.surface.y_of(dots_to_draw)
        axis.plot(x_values, y_values, 'o', color="red")

        x_to_draw = list(d for d in dots if d not in sim.linkables)
        x_values = sim.surface.x_of(x_to_draw)
        y_values = sim.surface.y_of(x_to_draw)
        axis.plot(x_values, y_values, 'x', color="red")

        return figure, axis


if __name__ == '__main__':
    linking_simulation = LinkingSimulation(32, 16, 2000, max_links=3)

    for _ in range(1):
        linking_simulation.run(60)
        Analyzer.report(linking_simulation)
        f, ax = Analyzer.visualization(linking_simulation)
        tikzplotlib.save("./test.tex", figure=f)

    plt.show()
