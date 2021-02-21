import unittest

from cbrlib.model.FloatClass import FloatClass
from cbrlib.model.FloatObject import FloatObject


class TestFloatClass(unittest.TestCase):

    def setUp(self) -> None:
        self.float_class = FloatClass('FloatTest')

    def test_typename(self):
        self.assertEqual(self.float_class.get_typename(), 'float')

    def test_create_object(self):
        value_object = self.float_class.create_object(98.0)
        self.assertEqual(value_object, FloatObject(98.0))
        self.assertEqual(value_object.get_value(), 98.0)
        value_object = self.float_class.create_object(98)
        self.assertEqual(value_object, FloatObject(98.0))
        self.assertEqual(value_object.get_value(), 98.0)
        value_object = self.float_class.create_object('98.819')
        self.assertEqual(value_object, FloatObject(98.819))
        self.assertEqual(value_object.get_value(), 98.819)
        try:
            value_object = self.float_class.create_object('test')
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_read_object(self):
        value_object = self.float_class.read_object(98.0)
        self.assertEqual(value_object, FloatObject(98.0))
        self.assertEqual(value_object.get_value(), 98.0)
        value_object = self.float_class.read_object(98)
        self.assertEqual(value_object, FloatObject(98.0))
        self.assertEqual(value_object.get_value(), 98.0)
        value_object = self.float_class.read_object('98.819')
        self.assertEqual(value_object, FloatObject(98.819))
        self.assertEqual(value_object.get_value(), 98.819)
        try:
            value_object = self.float_class.read_object('test')
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_json(self):
        json_value = self.float_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'FloatTest')
        self.assertEqual(json_value.get('type'), 'float')


if __name__ == '__main__':
    unittest.main()
