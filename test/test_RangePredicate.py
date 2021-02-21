import unittest

from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.IntegerObject import IntegerObject
from cbrlib.model.PredicateError import PredicateError
from cbrlib.model.RangePredicate import RangePredicate


class TestRangePredicate(unittest.TestCase):

    def setUp(self) -> None:
        self.integer_class = IntegerClass('RangeTest')
        min_ = self.integer_class.create_object(10)
        max_ = self.integer_class.create_object(50)
        self.integer_class.set_predicate(RangePredicate(min_, max_))

    def test_read_object(self):
        self.assertEqual(self.integer_class.read_object(20), IntegerObject(20))
        self.assertEqual(self.integer_class.read_object(10), IntegerObject(10))
        self.assertEqual(self.integer_class.read_object(50), IntegerObject(50))
        with self.assertRaises(PredicateError):
            self.integer_class.read_object(9)
        with self.assertRaises(PredicateError):
            self.integer_class.read_object(51)

    def test_to_serializable(self):
        json_value = self.integer_class.to_serializable()
        self.assertDictEqual(json_value.get('range'), {'min': 10, 'max': 50})


if __name__ == '__main__':
    unittest.main()
