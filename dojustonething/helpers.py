from unittest import TestCase
from pprint import pformat
import uuid


def make_random_string(length=10):
    return str(uuid.uuid4()).replace("-", "")[:length]


class DJOTTestCase(TestCase):
    def assert_equal(self, first, second, message=None):
        message = (message if message else "%s was not equal to %s" % (first, second))
        self.assertTrue(first == second, message)

    def assert_not_equal(self, first, second, message=None):
        message = (message if message else "%s was equal to %s" % (first, second))
        self.assertTrue(first != second, message)

    def assert_less(self, first, second, message=None):
        message = (message if message
            else "%s not less than %s" % (first, second))
        self.assertTrue(first < second, message)

    def assert_less_equal(self, first, second, message=None):
        message = (message if message
            else "%s not less than or equal to %s" % (first, second))
        self.assertTrue(first <= second, message)

    def assert_greater(self, first, second, message=None):
        message = (message if message
            else "%s not greater than %s" % (first, second))
        self.assertTrue(first > second, message)

    def assert_greater_equal(self, first, second, message=None):
        message = (message if message
            else "%s not greater than or equal to %s" % (first, second))
        self.assertTrue(first >= second, message)

    def assert_none(self, item, message=None):
        message = (message if message
            else "%s should have been None" % pformat(item))
        self.assertTrue(item is None, message)

    def assert_not_none(self, item, message=None):
        message = (message if message
            else "%s should not have been None" % pformat(item))
        self.assertFalse(item is None, message)

    def assert_excepts(self, exception_type, func, *args, **kwargs):
        excepted = False
        try:
            val = func(*args, **kwargs)
            print ("assert_excepts: Crap. That wasn't supposed to work."
                " Here's what I got: ", pformat(val))
        except exception_type, e:
            print ("assert_excepts: Okay, %s failed the way it was supposed"
                " to: %s" % (func, e))
            excepted = True
        self.assertTrue(excepted, "assert_excepts: calling %s didn't raise %s"
            % (func, exception_type))

    def assert_in(self, needle, haystack, message=None):
        return self.assert_contains(haystack, needle, message)

    def assert_not_in(self, needle, haystack, message=None):
        return self.assert_not_contains(haystack, needle, message)

    def assert_contains(self, haystack, needle, message=None):
        displaystack = self._format(haystack)
        message = (message if message
            else "%s not found in %s" % (needle, displaystack))

        its_in_there = False
        try:
            if needle in haystack:
                its_in_there = True
        except:
            pass

        try:
            if not its_in_there and haystack in needle:
                print "! HEY !" * 5
                print "HEY! it looks like you called assert_contains backwards"
                print "! HEY !" * 5
        except:
            pass

        self.assertTrue(needle in haystack, message)

    def _format(self, haystack):
        return haystack

    def assert_not_contains(self, haystack, needle, message=None):
        displaystack = self._format(haystack)
        message = (message if message
            else "%s not wanted but found in %s" % (needle, displaystack))
        self.assertFalse(needle in haystack, message)

    def assert_any(self, conditions, message=None):
        message = (message if message
            else "%s were all False" % pformat(conditions))
        self.assertTrue(any(conditions), message)

    def assert_not_any(self, conditions, message=None):
        message = (message if message
            else "%s was not all False" % pformat(conditions))
        self.assertFalse(any(conditions), message)

    def assert_startswith(self, haystack, needle, message=None):
        displaystack = self._format(haystack)
        message = (message if message
            else "%s should have been at the beginning of %s"
            % (needle, displaystack))
        self.assertTrue(haystack.startswith(needle), message)

    def assert_endswith(self, haystack, needle, message=None):
        displaystack = self._format(haystack)
        message = (message if message
            else "%s should have been at the end of %s"
            % (needle, displaystack))
        self.assertTrue(haystack.endswith(needle), message)

    def assert_not_startswith(self, haystack, needle, message=None):
        displaystack = self._format(haystack)
        message = (message if message
            else "%s should not have been at the beginning of %s"
            % (needle, displaystack))
        self.assertFalse(haystack.startswith(needle), message)

    def assert_is(self, expected, actual, message=None):
        message = message if message else "%s is not %s" % (expected, actual)
        self.assertTrue(expected is actual)

    def assert_is_not(self, expected, actual, message=None):
        message = message if message else "%s is %s" % (expected, actual)
        self.assertTrue(expected is not actual)
