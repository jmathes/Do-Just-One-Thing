# encoding: utf-8
# chr(33) through chr(126)
# !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
import helpers
from todolist import ToDoList, AmbiguousUrgencyExeption, all_chars


class FakeItem(object):
    def __init__(self):
        pass

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.__dict__)


class ToDoListTestCase(helpers.DJOTTestCase):
    def setUp(self):
        self.username = helpers.make_random_string()
        self.list = ToDoList(item_type=FakeItem,
                             username=self.username)
        self.middle_char = all_chars[len(all_chars) / 2]
        print self.list

    def test_some_properties_about_all_chars(self):
        self.assert_greater(len(all_chars), 90)
        self.assertEqual('!', all_chars[0])
        self.assertEqual('}', all_chars[-1])

        for i in xrange(len(all_chars) - 1):
            self.assert_less(chr(i), chr(i + 1))

        for i in xrange(len(all_chars)):
            self.assertEqual(chr(i + 33), all_chars[i])
            self.assertEqual(i + 33, ord(all_chars[i]))

    def test_newly_created_list_has_extremes_of_allchars_as_first_and_last_elements(self):
        self.assertEqual(self.list._items[0].urgency, all_chars[-1])
        self.assertEqual(self.list._items[-1].urgency, all_chars[0])

    def test_newly_created_list_takes_username(self):
        self.assertEqual(self.username, self.list.username)

    def test_inserting_item_preserves_content(self):
        self.assertTrue(self.list.empty)

        self.list.insert("Do\ntaxes")

        self.assertEqual(1, self.list.length)
        item = self.list[0]
        self.assertEqual("Do\ntaxes", item.content)

    def test_inserting_item_adds_username(self):
        self.assertTrue(self.list.empty)

        self.list.insert("Do\ntaxes")

        self.assertEqual(1, self.list.length)
        item = self.list[0]
        self.assertEqual(self.username, item.username)

    def test_insert_to_empty_list_gets_middle_priority(self):
        self.assertTrue(self.list.empty)

        self.list.insert("Pay those bills\nThe ones on my desk")

        self.assertEqual(1, self.list.length)
        item = self.list[0]

        self.assertEqual(item.urgency, self.middle_char)

    def test_insert_into_list_with_item_requires_bounds(self):
        self.list.insert("Finish writing this app")
        self.assertEqual(1, self.list.length)
        try:
            self.list.insert("Do something else")
            self.fail("Should have excepted")
        except AmbiguousUrgencyExeption as e:
            self.assertEqual("Finish writing this app", e.benchmark.content)

    def test_insert_into_list_when_existing_item_is_less_urgent(self):
        self.list.insert("High priority thing")
        self.assertEqual(1, self.list.length)
        first_item = self.list[0]
        self.list.insert("Higher priority thing", lower_bound=first_item.urgency)
        self.assertEqual(2, self.list.length)

        high_priority_item = self.list[0]
        low_priority_item = self.list[1]

        self.assertEqual("Higher priority thing", high_priority_item.content)
        self.assertEqual("High priority thing", low_priority_item.content)
        self.assert_greater(high_priority_item.urgency, low_priority_item.urgency)

    def test_insert_into_list_when_existing_item_is_more_urgent(self):
        self.list.insert("High priority thing")
        self.assertEqual(1, self.list.length)
        high_priority_item = self.list[0]

        self.list.insert("Low priority thing",
                         upper_bound=high_priority_item.urgency)
        self.assertEqual(2, self.list.length)

        high_priority_item = self.list[0]
        low_priority_item = self.list[1]

        self.assertEqual("Low priority thing", low_priority_item.content)

        self.assertEqual("High priority thing", high_priority_item.content)

        self.assert_greater(high_priority_item.urgency, low_priority_item.urgency)

    def test_insert_into_list_between_two_things_that_start_with_gap_letters_ends_up_with_middle(self):
        self.list._test_force(("top", "A"), ("bottom", "C"))
        print self.list

        self.list.insert("middle", upper_bound='C', lower_bound='A')

        self.assertEqual(3, self.list.length)
        self.assertEqual('B', self.list[1].urgency)

    def test_insert_into_list_of_three_things_with_priority_between_top_and_bottom_but_ambiguous_with_middle(self):
        self.list._test_force(("top", "A"), ("middle", "B"), ("bottom", "C"))
        self.assertEqual(3, self.list.length)
        print self.list._items
        try:
            self.list.insert("middle2", upper_bound='C', lower_bound='A')
            self.fail("should have excepted")
        except AmbiguousUrgencyExeption as e:
            self.assertEqual("middle", e.benchmark.content)

    def test_insert_into_list_between_two_items_with_adjacent_urgencies_takes_first_one_and_adds_a_letter(self):
        self.list._test_force(("top", "A"), ("bottom", "B"))
        print self.list

        self.list.insert("middle", upper_bound='B', lower_bound='A')
        print self.list

        self.assertEqual(3, self.list.length)
        self.assertEqual('A' + self.middle_char, self.list[1].urgency)
        self.assertTrue(self.list[0].urgency > self.list[1].urgency > self.list[2].urgency)

    def test_insert_into_list_between_two_items_with_same_first_few_letters_does_the_right_thing(self):
        self.list._test_force(("top", "blahblahZZX"), ("bottom", "blahblahAAAAA"))
        print self.list

        self.list.insert("middle", upper_bound='blahblahZZX', lower_bound='blahblahAAAAA')
        print self.list

        self.assertEqual(3, self.list.length)
        self.assert_startswith(self.list[1].urgency, 'blahblah')
        self.assertEqual('top', self.list[0].content)
        self.assertEqual('middle', self.list[1].content)
        self.assertEqual('bottom', self.list[2].content)
        self.assertTrue(self.list[0].urgency > self.list[1].urgency > self.list[2].urgency)

    def test_insert_into_list_thats_lower_than_lowest_possible_item_rejiggers_list(self):
        self.list._test_force(("lowest_possible", all_chars[1]))
        print self.list

        self.list.insert("lower_than_low", upper_bound=all_chars[1])
        print self.list
        self.assertEqual('lowest_possible', self.list[0].content)
        self.assertEqual('lower_than_low', self.list[1].content)
        for i in xrange(self.list.length):
            self.assert_not_startswith(self.list[i].urgency, all_chars[0])
            self.assert_not_startswith(self.list[i].urgency, all_chars[-1])
        self.assertTrue(self.list[0].urgency > self.list[1].urgency > all_chars[0])
