# encoding: utf-8
# chr(33) through chr(125)
# !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
# chr(32) is ' '; chr(126) is '~'
import logging
import cgi

from todolistitem import ToDoListItem


class AmbiguousUrgencyExeption(Exception):
    def __init__(self, benchmark):
        self.benchmark = benchmark

HIGHEST_URGENCY = float(2 ** 16)
LOWEST_URGENCY = -1 * HIGHEST_URGENCY


class ToDoList(object):

    def __init__(self, username, db):
        self.db = db
        self.username = username
        self.reset()
        items = ToDoListItem.gql("WHERE ANCESTOR IS :1 "
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
        fake_highest_item = self.make_new_item("(hidden highest priority item)")
        fake_highest_item.urgency = HIGHEST_URGENCY
        fake_lowest_item = self.make_new_item("(hidden lowest priority item)")
        fake_lowest_item.urgency = LOWEST_URGENCY
        self._items = [fake_highest_item, fake_lowest_item]

    def get_top_item(self):
        if len(self._items) == 2:
            return "Click on the + symbol to add a thing"
        return cgi.escape(self._items[1].task)

    def _test_force(self, *args):
        self.reset()
        for task, urgency in args:
            new_item = ToDoListItem()
            new_item.task = task
            new_item.urgency = urgency
            new_item.username = self.username
            self._items.append(new_item)
        self._sort()

    def _sort(self):
        self._items.sort(key=lambda item: item.urgency, reverse=True)

    def make_new_item(self, task):
        new_item = ToDoListItem(parent=self.key())
        new_item.task = task
        new_item.username = self.username
        return new_item

    def get_urgency_between(self, high_index, low_index):
        high_urgency = self._items[high_index].urgency
        low_urgency = self._items[low_index].urgency
        middle_urgency = (high_urgency + low_urgency) / 2.
        return middle_urgency

    def insert(self, task, upper_bound=None, lower_bound=None):
        if isinstance(task, dict):
            upper_bound = task.get('upper_bound')
            lower_bound = task.get('lower_bound')
            task = task['task']
        if upper_bound is None:
            upper_bound = self._items[0].urgency
        assert upper_bound <= self._items[0].urgency
        if lower_bound is None:
            lower_bound = self._items[-1].urgency
        assert lower_bound >= self._items[-1].urgency
        assert lower_bound < upper_bound

        new_item = self.make_new_item(task)

        for i, item in enumerate(self._items):
            if item.urgency >= upper_bound:
                upper_bound_index = i
            if item.urgency <= lower_bound:
                lower_bound_index = i
                break

        if lower_bound_index - upper_bound_index > 1:
            halfway_point = (upper_bound_index + lower_bound_index) / 2
            raise AmbiguousUrgencyExeption(self._items[halfway_point])

        new_item.urgency = self.get_urgency_between(upper_bound_index, lower_bound_index)
        new_item.put()
        self._items.append(new_item)
        self._sort()

        for i, item in enumerate(self._items[:-1]):
            assert self._items[i].urgency > self._items[i + 1].urgency
