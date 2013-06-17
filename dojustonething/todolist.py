# encoding: utf-8
import cgi
import logging
from datetime import datetime, timedelta

from todolistitem import ToDoListItem
from user import User


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
        items = ToDoListItem.gql(
            "WHERE date_completed = NULL"
            " AND ANCESTOR IS :1"
            " LIMIT 10000",
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
        now = datetime.now()
        for item in self._items[1:-1]:
            if item.delay_until is None or item.delay_until <= now:
                return {
                    'task': cgi.escape(item.task),
                    'id': item.key().id(),
                }

        return {
            'task': "Click on the + symbol to add a thing",
            'id': None,
        }

    def get_thing_index(self, item_id):
        for index, item in enumerate(self._items):
            if item in [self._items[0], self._items[-1]]:
                continue
            if item_id == item.key().id():
                break
        if index == len(self._items) - 1:
            return None
        return index

    def delay_item(self, item_id):
        index = self.get_thing_index(item_id)
        if index is None:
            return
        done = self._items[index]
        done.delay_until = datetime.now() + timedelta(hours=4)
        done.save()

    def remove_item(self, item_id):
        index = self.get_thing_index(item_id)
        if index is None:
            return
        done = self._items[index]
        done.date_completed = datetime.now()
        done.save()
        self._items = self._items[:index] + self._items[index + 1:]

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
        logging.error("Adding task %s", task)
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
        if lower_bound >= upper_bound:
            logging.error(
                "Task %s has priorities backwards: (%s, %s) [%s, %s]",
                task['task'],
                lower_bound,
                upper_bound,
                task['lower_bound'],
                task['upper_bound'])
        assert lower_bound < upper_bound

        new_item = self.make_new_item(task)

        for i, item in enumerate(self._items):
            if item.urgency >= upper_bound:
                logging.error("upper bound task: %s" % item)
                upper_bound_index = i
            if item.urgency <= lower_bound:
                logging.error("lower bound task: %s" % item)
                lower_bound_index = i
                break
            else:
                logging.error("not lower bound task: %s", item)
                logging.error("(item.urgency <= lower_bound is %s <= %s is %s", item.urgency, lower_bound, item.urgency <= lower_bound)
        logging.error("all items: %s" % [(i, item.task, item.urgency) for i, item in enumerate(self._items)])

        if lower_bound_index - upper_bound_index > 1:
            halfway_point = (upper_bound_index + lower_bound_index) / 2
            logging.error("halfway point: %s" % halfway_point)
            logging.error("halfway item: %s" % self._items[halfway_point])
            raise AmbiguousUrgencyExeption(self._items[halfway_point])

        new_item.urgency = self.get_urgency_between(upper_bound_index, lower_bound_index)

        new_item.put()
        self._items.append(new_item)
        self._sort()
        self._recalculate_urgencies()

        for i, item in enumerate(self._items[:-1]):
            assert self._items[i].urgency > self._items[i + 1].urgency

    def _recalculate_urgencies(self):
        assert len(self._items) >= 4
        logging.error("recalculating...")
        logging.error("all items: %s" % [(i, item.task, item.urgency) for i, item in enumerate(self._items)])

        step = (2 ** 17) / (len(self._items) - 1)
        max_urgency = (2 ** 16) - step
        logging.error("step: %s", step)
        logging.error("max_urgency: %s", max_urgency)
        for i, item in enumerate(self._items[1:-1]):
            new_urgency = 1. * max_urgency - step * i
            logging.error("changing urgency for %s from %s to %s", item, item.urgency, new_urgency)
            item.urgency = new_urgency
            item.save()
