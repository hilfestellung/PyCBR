import unittest
from datetime import date, datetime

from cbrlib.model.StringClass import StringClass
from cbrlib.model.StringObject import StringObject


class TestStringClass(unittest.TestCase):

    def setUp(self) -> None:
        self.string_class = StringClass('StringTest')
        self.helloWorldObject = StringObject('Hello World')

    def test_typename(self):
        self.assertEqual(self.string_class.get_typename(), 'string')

    def test_create_object(self):
        value_object = self.string_class.create_object('Hello World')
        self.assertEqual(value_object, StringObject('Hello World'))
        self.assertEqual(value_object.get_value(), 'Hello World')
        value_object = self.string_class.create_object(1)
        self.assertEqual(value_object, StringObject('1'))
        self.assertEqual(value_object.get_value(), '1')
        value_object = self.string_class.create_object(1.0)
        self.assertEqual(value_object, StringObject('1.0'))
        self.assertEqual(value_object.get_value(), '1.0')
        value_object = self.string_class.create_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, StringObject('2021-02-28'))
        self.assertEqual(value_object.get_value(), '2021-02-28')
        value_object = self.string_class.create_object(datetime.fromisoformat('2021-02-28 18:30:27.456'))
        self.assertEqual(value_object, StringObject('2021-02-28T18:30:27.456000'))
        self.assertEqual(value_object.get_value(), '2021-02-28T18:30:27.456000')
        try:
            value_object = self.string_class.create_object(dict())
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_read_object(self):
        value_object = self.string_class.read_object('Hello World')
        self.assertEqual(value_object, StringObject('Hello World'))
        self.assertEqual(value_object.get_value(), 'Hello World')
        value_object = self.string_class.read_object(1)
        self.assertEqual(value_object, StringObject('1'))
        self.assertEqual(value_object.get_value(), '1')
        value_object = self.string_class.read_object(1.0)
        self.assertEqual(value_object, StringObject('1.0'))
        self.assertEqual(value_object.get_value(), '1.0')
        value_object = self.string_class.read_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, StringObject('2021-02-28'))
        self.assertEqual(value_object.get_value(), '2021-02-28')
        value_object = self.string_class.read_object(datetime.fromisoformat('2021-02-28 18:30:27.456'))
        self.assertEqual(value_object, StringObject('2021-02-28T18:30:27.456000'))
        self.assertEqual(value_object.get_value(), '2021-02-28T18:30:27.456000')

        with self.assertRaises(ValueError):
            value_object = self.string_class.read_object(dict())

    def test_to_json(self):
        json_value = self.string_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'StringTest')
        self.assertEqual(json_value.get('type'), 'string')
        value_object = self.string_class.read_object('The JSON test string')
        json_value = value_object.to_serializable()
        self.assertEqual(json_value, 'The JSON test string')


if __name__ == '__main__':
    unittest.main()
