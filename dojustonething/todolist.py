# encoding: utf-8
# chr(33) through chr(126)
# !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
import logging


class AmbiguousUrgencyExeption(Exception):
    def __init__(self, benchmark):
        self.benchmark = benchmark

all_chars = """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"""
middle_char = all_chars[len(all_chars) / 2]


class ToDoList(object):

    def __init__(self, username, db, item_type=None):
        if item_type is None:
            from todolistitem import ToDoListItem
            item_type = ToDoListItem
        self.db = db
        self.username = username
        self.item_type = item_type
        self.reset()
        items = self.item_type.gql("WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10000",
                            self.key())
        for item in items:
            self._items.append(item)
        self._sort()

    def __getitem__(self, index):
        items = self._items[1:-1]
        return items[index]

    def __repr__(self):
        return "<%s's %s: %s>" % (
            self.username,
            self.__class__.__name__,
            self._items[1:-1])

    def key(self):
        return self.db.Key.from_path('ToDoList', self.username)

    def get_length(self):
        return len(self._items) - 2
    length = property(get_length)

    def is_empty(self):
        return self.length == 0
    empty = property(is_empty)

    def reset(self):
        fake_lowest_item = self.make_new_item("(hidden lowest priority item)")
        fake_lowest_item.urgency = all_chars[0]
        fake_highest_item = self.make_new_item("(hidden highest priority item)")
        fake_highest_item.urgency = all_chars[-1]
        self._items = [fake_highest_item, fake_lowest_item]

    def _test_force(self, *args):
        self.reset()
        for task, urgency in args:
            new_item = self.item_type()
            new_item.task = task
            new_item.urgency = urgency
            new_item.username = self.username
            self._items.append(new_item)
        self._sort()

    def _sort(self):
        self._items.sort(key=lambda item: item.urgency, reverse=True)

    def make_new_item(self, task):
        new_item = self.item_type(parent=self.key())
        new_item.task = task
        new_item.username = self.username
        return new_item

    def get_lexicographic_midpoint(self, high, low):
        first_low = low[0] if low else all_chars[0]
        first_high = high[0] if high else all_chars[-1]
        if ord(first_high) == ord(first_low) + 1:
            first_high = first_low
        if first_low == first_high:
            halfway = first_low + self.get_lexicographic_midpoint(high[1:], low[1:])
            return halfway
        else:
            return chr((ord(first_low) + ord(first_high)) / 2)

    def get_urgency_between(self, high_index, low_index):
        high_urgency = self._items[high_index].urgency
        low_urgency = self._items[low_index].urgency
        middle_urgency = self.get_lexicographic_midpoint(high_urgency, low_urgency)

        if middle_urgency[0] in (all_chars[0], all_chars[-1]):
            for item in self._items[1:-1]:
                item.urgency = middle_char + item.urgency

        high_urgency = self._items[high_index].urgency
        low_urgency = self._items[low_index].urgency
        middle_urgency = self.get_lexicographic_midpoint(high_urgency, low_urgency)
        return middle_urgency

    def insert(self, task, upper_bound=None, lower_bound=None):
        if upper_bound is None or upper_bound > self._items[0].urgency:
            upper_bound = self._items[0].urgency
        if lower_bound is None or lower_bound < self._items[-1].urgency:
            lower_bound = self._items[-1].urgency
        assert lower_bound < upper_bound

        new_item = self.make_new_item(task)

        for i, item in enumerate(self._items):
            if upper_bound > item.urgency:
                break
            upper_bound_index = i

        for i in xrange(len(self._items) - 1, -1, -1):
            if lower_bound < self._items[i].urgency:
                break
            lower_bound_index = i

        if lower_bound_index - upper_bound_index > 1:
            halfway_point = (upper_bound_index + lower_bound_index) / 2
            raise AmbiguousUrgencyExeption(self._items[halfway_point])

        new_item.urgency = self.get_urgency_between(upper_bound_index, lower_bound_index)
        logging.debug("putting")
        new_item.put()
        self._items.append(new_item)
        self._sort()

        for i, item in enumerate(self._items[:-1]):
            assert self._items[i].urgency > self._items[i + 1].urgency
