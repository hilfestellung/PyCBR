import unittest

from cbrlib.model.EnumerationPredicate import EnumerationPredicate
from cbrlib.model.PredicateError import PredicateError
from cbrlib.model.StringClass import StringClass


class TestEnumerationPredicate(unittest.TestCase):

    def setUp(self) -> None:
        self.string_class = StringClass('EnumerationTest')
        self.value_range = [
            self.string_class.create_object('red'),
            self.string_class.create_object('green'),
            self.string_class.create_object('yellow'),
            self.string_class.create_object('blue')
        ]
        self.string_class.set_predicate(EnumerationPredicate(self.value_range))

    def test_read_object(self):
        self.assertIs(self.string_class.read_object('red'), self.value_range[0])
        self.assertIs(self.string_class.read_object('green'), self.value_range[1])
        self.assertIs(self.string_class.read_object('yellow'), self.value_range[2])
        self.assertIs(self.string_class.read_object('blue'), self.value_range[3])
        with self.assertRaises(PredicateError):
            self.string_class.read_object('pink')

    def test_to_serializable(self):
        json_value = self.string_class.to_serializable()
        self.assertEqual(json_value.get('enumeration'), ["blue", "green", "red", "yellow"])


if __name__ == '__main__':
    unittest.main()
