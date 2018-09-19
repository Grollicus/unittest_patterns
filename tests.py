from unittest import TestCase

import unittest_patterns as patterns


class ExamplesTest(TestCase):
    def test_examples(self):

        from unittest_patterns import Any, Isinstance, OneOf, Regex

        self.assertEqual(42, OneOf(1, 42))
        self.assertEqual(OneOf(1, 42), 1)
        self.assertEqual(Regex('.* passing .*'), 'this is a passing assertion')
        complex_dict = {'complicated': {'data': ['structure', 'with'], 'many': 'items'}}
        self.assertEqual(complex_dict, {'complicated': {'data': Isinstance(list), 'many': Any()}})


class AnyTest(TestCase):
    def test_any(self):
        self.assertEqual(patterns.Any(), 'asdf')
        self.assertEqual(patterns.Any(), None)
        self.assertEqual(patterns.Any(), False)
        self.assertEqual(patterns.Any(), [])
        self.assertEqual(patterns.Any(), {})

        self.assertEqual([1, patterns.Any()], [1, 2])
        self.assertEqual({'a': 1, 'b': patterns.Any()}, {'a': 1, 'b': 2})

        with self.assertRaises(Exception):
            self.assertEqual({patterns.Any(): 1}, {'1': 1})
        with self.assertRaises(Exception):
            self.assertEqual(set(patterns.Any()), set('1'))

    def test_req(self):
        self.assertEqual('asdf', patterns.Any())
        self.assertEqual(None, patterns.Any())
        self.assertEqual(False, patterns.Any())
        self.assertEqual([], patterns.Any())
        self.assertEqual({}, patterns.Any())

        self.assertEqual([1, 2], [1, patterns.Any()])
        self.assertEqual({'a': 1, 'b': 2}, {'a': 1, 'b': patterns.Any()})

        with self.assertRaises(Exception):
            self.assertEqual({'1': 1}, {patterns.Any(): 1})
        with self.assertRaises(Exception):
            self.assertEqual(set('1'), set(patterns.Any()))


class MatchTest(TestCase):
    def test_strings(self):
        self.assertEqual(patterns.Regex('a'), 'a')
        with self.assertRaisesRegex(AssertionError, "'a' does not match the pattern 'b'"):
            self.assertEqual(patterns.Regex('b'), 'a')

        self.assertEqual(patterns.Regex('.'), 'a')
        self.assertEqual(patterns.Regex('.a.'), 'bab')
        with self.assertRaisesRegex(AssertionError, "'fbab' does not match the pattern '.a.'"):
            self.assertEqual(patterns.Regex('.a.'), 'fbab')
        self.assertEqual(patterns.Regex('.*a.'), 'fbab')

        with self.assertRaisesRegex(AssertionError, "'a' does not match the pattern b'b'"):
            self.assertEqual(patterns.Regex(b'b'), 'a')

    def test_bytes(self):
        self.assertEqual(patterns.Regex(b'a'), b'a')
        with self.assertRaisesRegex(AssertionError, "b'a' does not match the pattern b'b'"):
            self.assertEqual(patterns.Regex(b'b'), b'a')

        self.assertEqual(patterns.Regex(b'.'), b'a')
        self.assertEqual(patterns.Regex(b'.a.'), b'bab')
        with self.assertRaisesRegex(AssertionError, "b'fbab' does not match the pattern b'.a.'"):
            self.assertEqual(patterns.Regex(b'.a.'), b'fbab')
        self.assertEqual(patterns.Regex(b'.*a.'), b'fbab')

        with self.assertRaisesRegex(AssertionError, "b'a' does not match the pattern 'b'"):
            self.assertEqual(patterns.Regex('b'), b'a')


class IsinstanceTest(TestCase):
    def test_isinstance(self):
        self.assertEqual(patterns.Isinstance(str), 'a')
        with self.assertRaisesRegex(AssertionError, "'a' is not an instance of <class 'int'>"):
            self.assertEqual(patterns.Isinstance(int), 'a')

        self.assertEqual([1, patterns.Isinstance(int)], [1, 2])
        with self.assertRaisesRegex(AssertionError, "'a' is not an instance of <class 'int'>"):
            self.assertEqual([1, patterns.Isinstance(int)], [1, 'a'])

        self.assertEqual({'a': patterns.Isinstance(int)}, {'a': 42})
        with self.assertRaisesRegex(AssertionError, "'a' is not an instance of <class 'int'>"):
            self.assertEqual({1: patterns.Isinstance(int)}, {1: 'a'})


class OneOfTest(TestCase):
    def test_oneof(self):
        with self.assertRaisesRegex(AssertionError, r'1 is not one of \(\)'):
            self.assertEqual(patterns.OneOf(), 1)

        self.assertEqual(patterns.OneOf(1, 2), 1)
        self.assertEqual(patterns.OneOf(1, 2), 2)
        with self.assertRaisesRegex(AssertionError, r'3 is not one of \(1, 2\)'):
            self.assertEqual(patterns.OneOf(1, 2), 3)

        self.assertEqual(patterns.OneOf('1', b'1'), '1')
        self.assertEqual(patterns.OneOf('1', b'1'), b'1')
        with self.assertRaisesRegex(AssertionError, "1 is not one of \\('1', b'1'\\)"):
            self.assertEqual(patterns.OneOf('1', b'1'), 1)

        self.assertEqual([1, patterns.OneOf(1, 2)], [1, 1])
        self.assertEqual([1, patterns.OneOf(1, 2)], [1, 2])
        with self.assertRaisesRegex(AssertionError, r'3 is not one of \(1, 2\)'):
            self.assertEqual([1, patterns.OneOf(1, 2)], [1, 3])

        self.assertEqual({1: patterns.OneOf(1, 2)}, {1: 1})
        self.assertEqual({1: patterns.OneOf(1, 2)}, {1: 2})

        with self.assertRaisesRegex(AssertionError, r'3 is not one of \(1, 2\)'):
            self.assertEqual({1: patterns.OneOf(1, 2)}, {1: 3})


class AllOfTest(TestCase):
    def test_allof(self):
        self.assertEqual(patterns.AllOf(), 1)
        self.assertEqual(patterns.AllOf(1), 1)
        with self.assertRaisesRegex(AssertionError, '2 != 1'):
            self.assertEqual(patterns.AllOf(1, 2), 1)

        with self.assertRaisesRegex(AssertionError, '2 != 1'):
            self.assertEqual(1, patterns.AllOf(1, 2))

        self.assertEqual(patterns.AllOf(
            patterns.Regex('.*s.*'),
            patterns.Regex('as.*'),
            patterns.Regex('.*df$'),
        ), 'asdf')


class CheckAttributesTest(TestCase):
    def test_checkattributes(self):
        class Foo(object):
            def __init__(self):
                self.foo = 1
                self.bar = 'a'
        f = Foo()

        self.assertEqual(patterns.CheckAttributes(foo=1), f)
        self.assertEqual(patterns.CheckAttributes(bar='a'), f)
        self.assertEqual(patterns.CheckAttributes(foo=1, bar=patterns.Any()), f)

        f.foo = 2
        with self.assertRaisesRegex(AssertionError, '1 != 2'):
            self.assertEqual(patterns.CheckAttributes(foo=1), f)
        with self.assertRaisesRegex(AssertionError, ".* has no attribute 'baz'"):
            self.assertEqual(patterns.CheckAttributes(baz=1), f)


class CallbackTest(TestCase):
    def test_callback(self):
        self.assertEqual(patterns.Callback(lambda x: x == 1), 1)

        with self.assertRaisesRegex(AssertionError, 'Callback returned false for 1'):
            self.assertEqual(patterns.Callback(lambda x: x == 2), 1)
