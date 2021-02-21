import unittest
from datetime import date, datetime

from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.IntegerObject import IntegerObject


class TestIntegerClass(unittest.TestCase):

    def setUp(self) -> None:
        self.integer_class = IntegerClass('IntegerTest')

    def test_typename(self):
        self.assertEqual(self.integer_class.get_typename(), 'integer')

    def test_create_object(self):
        value_object = self.integer_class.create_object(1)
        self.assertEqual(value_object, IntegerObject(1))
        self.assertEqual(value_object.get_value(), 1)
        value_object = self.integer_class.create_object(99)
        self.assertEqual(value_object, IntegerObject(99))
        self.assertEqual(value_object.get_value(), 99)
        value_object = self.integer_class.create_object(-1001)
        self.assertEqual(value_object, IntegerObject(-1001))
        self.assertEqual(value_object.get_value(), -1001)
        value_object = self.integer_class.create_object('-1001')
        self.assertEqual(value_object, IntegerObject(-1001))
        self.assertEqual(value_object.get_value(), -1001)
        value_object = self.integer_class.create_object('99')
        self.assertEqual(value_object, IntegerObject(99))
        self.assertEqual(value_object.get_value(), 99)
        value_object = self.integer_class.create_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, IntegerObject(1614470400000))
        self.assertEqual(value_object.get_value(), 1614470400000)
        value_object = self.integer_class.create_object(datetime.fromisoformat('2021-02-28 18:05:42.924'))
        self.assertEqual(value_object, IntegerObject(1614535542924))
        self.assertEqual(value_object.get_value(), 1614535542924)
        try:
            value_object = self.integer_class.create_object('test')
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_read_object(self):
        value_object = self.integer_class.read_object(1)
        self.assertEqual(value_object, IntegerObject(1))
        self.assertEqual(value_object.get_value(), 1)
        value_object = self.integer_class.read_object(99)
        self.assertEqual(value_object, IntegerObject(99))
        self.assertEqual(value_object.get_value(), 99)
        value_object = self.integer_class.read_object(-1001)
        self.assertEqual(value_object, IntegerObject(-1001))
        self.assertEqual(value_object.get_value(), -1001)
        value_object = self.integer_class.read_object('-1001')
        self.assertEqual(value_object, IntegerObject(-1001))
        self.assertEqual(value_object.get_value(), -1001)
        value_object = self.integer_class.read_object('99')
        self.assertEqual(value_object, IntegerObject(99))
        self.assertEqual(value_object.get_value(), 99)
        value_object = self.integer_class.read_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, IntegerObject(1614470400000))
        self.assertEqual(value_object.get_value(), 1614470400000)
        value_object = self.integer_class.read_object(datetime.fromisoformat('2021-02-28 18:05:42.924'))
        self.assertEqual(value_object, IntegerObject(1614535542924))
        self.assertEqual(value_object.get_value(), 1614535542924)
        try:
            value_object = self.integer_class.read_object('test')
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_to_json(self):
        json_value = self.integer_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'IntegerTest')
        self.assertEqual(json_value.get('type'), 'integer')
        value_object = self.integer_class.create_object(99)
        json_value = value_object.to_serializable()
        self.assertEqual(json_value, 99)


if __name__ == '__main__':
    unittest.main()
