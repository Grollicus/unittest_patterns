"""
Provides placeholders that can be used with `assertEqual()` of python's `unittest`.

Examples::

    self.assertEqual(42, OneOf(1, 42))
    self.assertEqual(OneOf(1, 42), 1)
    self.assertEqual(Regex('.* passing .*'), 'this is a passing assertion')
    complex_dict = {'complicated': {'data': ['structure', 'with'], 'many': 'items'}}
    self.assertEqual(complex_dict, {'complicated': {'data': Isinstance(list), 'many': Any()}})


Notes::

* In error messages the pattern will always be on the left side
* Using Patterns on the right hand side with objects on the left hand side that define their own equals operator will break

"""


import re


class Pattern(object):
    def __req__(self, lhs):
        return self.__eq__(lhs)

    __hash__ = None


class Any(Pattern):
    """ Equals everything """

    def __eq__(self, rhs):
        return True


class Regex(Pattern):
    """ Requires a `pattern`. Equals everyhting that `re.match`es the `pattern`. """
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, rhs):
        try:
            if re.match(self.pattern, rhs) is None:
                raise AssertionError('%r does not match the pattern %r' % (rhs, self.pattern))
            return True
        except TypeError as e:
            raise AssertionError('%r does not match the pattern %r' % (rhs, self.pattern)) from e


class Isinstance(Pattern):
    """ requires a `class`. Equals everything that is an instance of `class`. """
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, rhs):
        if not isinstance(rhs, self.cls):
            raise AssertionError('%r is not an instance of %r' % (rhs, self.cls))
        return True


class OneOf(Pattern):
    """ requires zero or more parameters. Equals everything that equals at least one of the parameters. """
    def __init__(self, *args):
        self.options = args

    def __eq__(self, rhs):
        if not any(opt == rhs for opt in self.options):
            raise AssertionError('%r is not one of %r' % (rhs, self.options))
        return True


class AllOf(Pattern):
    """ requires zero or more parameters. Equals everything that equals all of the parameters. """
    def __init__(self, *args):
        self.options = args

    def __eq__(self, rhs):
        for opt in self.options:
            if not (opt == rhs):
                raise AssertionError('%r != %r' % (opt, rhs))
        return True


class CheckAttributes(Pattern):
    """ requires one or more keyword parameter. Equals everything that has every keyword parameter's name as attribute and it's value as the attribute's value. """
    def __init__(self, **attributes):
        self.attributes = attributes

    def __eq__(self, rhs):
        for (attr_name, expected_value) in self.attributes.items():
            if not hasattr(rhs, attr_name):
                raise AssertionError('%r has no attribute %r' % (rhs, attr_name))
            current_value = getattr(rhs, attr_name)
            if not (expected_value == current_value):
                raise AssertionError('%r != %r' % (expected_value, current_value))
        return True


class Callback(Pattern):
    """ requires a callback as parameter. Equals everything for that the callback returns `True` """
    def __init__(self, function: callable):
        self.function = function

    def __eq__(self, rhs):
        if not self.function(rhs):
            raise AssertionError('Callback returned false for %r' % (rhs,))
        return True


__all__ = ['Any', 'Regex', 'Isinstance', 'OneOf', 'AllOf', 'CheckAttributes', 'Callback']
