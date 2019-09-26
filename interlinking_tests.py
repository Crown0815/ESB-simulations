from unittest import TestCase
from interlinking import *


class LinkableTests(TestCase):
    @staticmethod
    def create_test_instance(max_links: int = 1):
        coordinate = Coordinate.default()
        return Linkable(coordinate, max_links)

    @staticmethod
    def create_instance_at_position(x: float, y: float):
        coordinate = Coordinate(x, y, 0, 0)
        return Linkable(coordinate)

    def test_is_full(self):
        instance = self.create_test_instance()

        self.assertEqual(instance.max_links, 1)
        self.assertFalse(instance.is_full())
        instance.links.append(None)
        self.assertTrue((instance.is_full()))

    def test_link_with_other_link_links_both_and_returns_link(self):
        instance = self.create_test_instance()
        other = self.create_test_instance()

        link = instance.link_with(other)

        self.assertTrue(link in instance.links)
        self.assertTrue(link in other.links)
        self.assertEqual(link.linked1, instance)
        self.assertEqual(link.linked2, other)

    def test_link_with_self_raises_exception(self):
        instance = self.create_test_instance()
        with self.assertRaises(Exception):
            instance.link_with(instance)

    def test_link_with_already_full_raises_exception(self):
        instance = self.create_test_instance()
        instance.links.append(None)

        self.assertTrue(instance.is_full())
        with self.assertRaises(Exception):
            instance.link_with(None)

    def test_link_with_already_full_other_raises_exception(self):
        instance = self.create_test_instance()

        other = self.create_test_instance()
        other.links.append(None)

        self.assertTrue(other.is_full())
        with self.assertRaises(Exception):
            instance.link_with(other)

    def test_link_with_None_links_instance_returns_link_with_None(self):
        instance = self.create_test_instance()

        link = instance.link_with(None)

        self.assertTrue(link in instance.links)
        self.assertEqual(link.linked1, instance)
        self.assertEqual(link.linked2, None)

    def test_is_linked_with_more_closed_links_than_threshold_returns_true(self):
        instance = self.create_test_instance(2)
        instance.link_with(self.create_test_instance())
        instance.link_with(self.create_test_instance())

        self.assertTrue(instance.is_linked(1))
        self.assertTrue(instance.is_linked(2))

    def test_is_linked_threshold_below_1_throws(self):
        instance = self.create_test_instance(2)
        with self.assertRaises(Exception):
            instance.is_linked(-1)
        with self.assertRaises(Exception):
            instance.is_linked(0)

    def test_find_partner_with_linkables_in_range_returns_closest(self):
        instance = self.create_test_instance()
        expected = self.create_instance_at_position(1, 0)
        others = [expected, self.create_instance_at_position(2, 0), self.create_instance_at_position(3, 0)]

        result = instance.find_partner(others, 2.5)
        self.assertEqual(result, expected)

    def test_find_partner_with_linkables_exactly_in_range_successful(self):
        instance = self.create_test_instance()
        expected = self.create_instance_at_position(1, 0)

        result = instance.find_partner([expected], 1)
        self.assertEqual(result, expected)

    def test_find_partner_with_empty_linkables_returns_None(self):
        instance = self.create_test_instance()

        result = instance.find_partner([], 1)
        self.assertEqual(result, None)


class LinkTests(TestCase):
    @staticmethod
    def create_test_instance(linkable1, linkable2):
        return Link(linkable1, linkable2)

    @staticmethod
    def create_test_linkable():
        return Linkable(Coordinate.default())

    def test_is_open_with_one_linkable_None_returns_true(self):
        instance = self.create_test_instance(self.create_test_linkable(), None)
        self.assertTrue(instance.is_open())

        instance = self.create_test_instance(None, self.create_test_linkable())
        self.assertTrue(instance.is_open())

    def test_constructor_both_linkables_None_raises_exception(self):
        with self.assertRaises(Exception):
            Link(None, None)

    def test_other_returns_none_given_linkable(self):
        l1 = self.create_test_linkable()
        l2 = self.create_test_linkable()
        instance = self.create_test_instance(l1, l2)

        self.assertEqual(instance.other(l1), l2)
        self.assertEqual(instance.other(l2), l1)

    def test_other_argument_not_linked_by_link_raises_exception(self):
        l1 = self.create_test_linkable()
        l2 = self.create_test_linkable()
        instance = self.create_test_instance(l1, l2)
        with self.assertRaises(Exception):
            instance.other(self.create_test_linkable())


class LinkerTests(TestCase):
    @staticmethod
    def create_test_instance(max_links=1, linkable_length=0, unique_links=True):
        return Linker(LinkerTests.create_test_coordinates(), max_links, linkable_length, unique_links)

    @staticmethod
    def create_test_coordinates():
        yield Coordinate(0, 0)
        yield Coordinate(1, 0)
        yield Coordinate(0, 1)
        yield Coordinate(1, 1)

    def test_create_random_link_with_too_short_link(self):
        instance = self.create_test_instance()
        instance.create_random_link(0.5)

        self.assertEqual(len(instance.links), 1)
        self.assertTrue(instance.links[0].is_open())

    def test_create_random_link_with_long_enough_link(self):
        instance = self.create_test_instance()
        instance.create_random_link(1)

        self.assertEqual(len(instance.links), 1)
        self.assertFalse(instance.links[0].is_open())

    def test_create_links_only_length_input_links_up_all(self):
        instance = self.create_test_instance()
        remains = instance.create_links(1)

        self.assertEqual(len(instance.links), 2)
        self.assertTrue(isnan(remains))
        self.assertFalse(instance.links[0].is_open())
        self.assertFalse(instance.links[1].is_open())

    def test_create_links_too_many_links_returns_remaining(self):
        instance = self.create_test_instance()
        remains = instance.create_links(1, 4)

        self.assertEqual(len(instance.links), 2)
        self.assertEqual(remains, 2)

    def test_create_random_link_with_long_enough_link_including_linkable_length(self):
        instance = self.create_test_instance(linkable_length=0.25)
        instance.create_random_link(0.5)

        self.assertEqual(len(instance.links), 1)
        self.assertFalse(instance.links[0].is_open())

    def test_create_link_no_duplicate_links(self):
        instance = self.create_test_instance(max_links=2)
        linkable = instance.linkables[0]
        instance.create_link(linkable, 1)
        instance.create_link(linkable, 1)

        self.assertEqual(len(instance.links), 2)
        self.assertNotEqual(instance.links[0].linked2, instance.links[1].linked2)

    def test_create_link_non_unique_links_creates_duplicate_links(self):
        instance = self.create_test_instance(max_links=2, unique_links=False)
        linkable = instance.linkables[0]
        instance.create_link(linkable, 1)
        instance.create_link(linkable, 1)

        self.assertEqual(len(instance.links), 2)
        self.assertEqual(instance.links[0].linked2, instance.links[1].linked2)
