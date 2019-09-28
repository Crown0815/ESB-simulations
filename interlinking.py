from surfaces import *
import random


class Linkable(Coordinate):
    def __init__(self, coordinate, max_links: int = 1):
        self.x = coordinate.x
        self.y = coordinate.y
        self.x_index = coordinate.x_index
        self.y_index = coordinate.y_index
        self.max_links = max_links
        self.links = list()

    def can_link(self):
        return not self.is_full()

    def is_full(self):
        return len(self.links) >= self.max_links

    def link_with(self, other):
        if not self.can_link():
            raise Exception("too many links on self already")
        if not other is None and not other.can_link():
            raise Exception("too many links on other already")
        if other == self:
            raise Exception("can not link to itself")
        link = Link(self, other)
        self.links.append(link)
        if other is not None: other.links.append(link)
        return link

    def try_link_with(self, other):
        if not self.can_link() or self == other:
            return False
        self.link_with(other)
        return True

    def open_links_count(self):
        return sum(link.is_open() for link in self.links)

    def connected_links(self):
        return sum(not link.is_open() for link in self.links)

    def is_linked(self, threshold=1):
        if threshold < 1:
            raise Exception("'at_least' may not be smaller than 1")
        return self.connected_links() >= threshold

    def find_partner(self, linkables, max_distance):
        closest_neighbor = self.closest_neighbor(linkables)
        if closest_neighbor is None: return None
        if self.distance_to(closest_neighbor) > max_distance: return None

        return closest_neighbor

    def linked_partners(self):
        return list(link.other(self) for link in self.links)


class Link:
    def __init__(self, linkable1, linkable2):
        if linkable1 is None and linkable2 is None:
            raise Exception("Link has to be connected to at least one linkable")
        self.linked1 = linkable1
        self.linked2 = linkable2

    def is_open(self):
        return self.linked1 is None or self.linked2 is None

    def other(self, linkable):
        if linkable == self.linked1: return self.linked2
        if linkable == self.linked2: return self.linked1
        raise Exception("requested linkable is not linked by this link")


class Linker:
    def __init__(self, coordinates, max_links: int, linkable_length: float, unique_links: bool = True):
        self.linkables = list(Linkable(c, max_links) for c in coordinates)
        self.interlinked = list()
        self.links = list()
        self.linkable_length = linkable_length
        self.unique_links = unique_links

    def create_links(self, linker_length: float, linker_count: int = nan):
        while isnan(linker_count) or linker_count > 0:
            if self.are_all_linked(): break
            self.create_random_link(linker_length)
            linker_count -= 1
        return linker_count

    def create_random_link(self, linker_length: float):
        linkable = random.choice(self.linkables)
        self.create_link(linkable, linker_length)

    def create_link(self, linkable, linker_length: float):
        partner = linkable.find_partner(self.valid_partners_for(linkable), self.link_range(linker_length))
        self.links.append(linkable.link_with(partner))

        self.move_to_interlinked_if_full(linkable)
        self.move_to_interlinked_if_full(partner)

    def link_range(self, linker_length):
        return linker_length + 2 * self.linkable_length

    def valid_partners_for(self, linkable):
        if not self.unique_links:
            return self.linkables
        return list(l for l in self.linkables if l not in linkable.linked_partners())

    def move_to_interlinked_if_full(self, linkable):
        if linkable is None: return
        if not linkable.is_full(): return

        self.linkables.remove(linkable)
        self.interlinked.append(linkable)

    def are_all_linked(self):
        return len(self.linkables) == 0


if __name__ == '__main__':
    grid = HexagonalGrid(2.5)
    surface = RandomSurface(grid)
    surface.initialize(2000, 2000, 60)
    f, ax = surface.visualization()

    linker = Linker(surface.coordinates_with_padding, 2, 16)
    linker.create_links(32)

    links = linker.links
    for current_link in links:
        if current_link.is_open(): continue
        linkables = [current_link.linked1, current_link.linked2]
        if len(list(surface.coordinates_within(linkables, 0, 2000, 0, 2000))) == 0: continue

        x_values = list(c.x for c in linkables)
        y_values = list(c.y for c in linkables)
        ax.plot(x_values, y_values, marker="o", color="red")
    plt.show()
