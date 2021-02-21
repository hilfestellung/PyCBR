import unittest

from cbrlib.model.BooleanClass import BooleanClass
from cbrlib.model.BooleanObject import BooleanObject


class TestBooleanClass(unittest.TestCase):

    def setUp(self) -> None:
        self.boolean_class = BooleanClass('BooleanTest')

    def test_typename(self):
        self.assertEqual(self.boolean_class.get_typename(), 'boolean')

    def test_create_object(self):
        value_object = self.boolean_class.create_object(True)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.create_object(False)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.create_object('True')
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.create_object('False')
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.create_object(0)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.create_object(-2381)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.create_object(99)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.create_object(None)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        some_object = dict()
        value_object = self.boolean_class.create_object(some_object)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.create_object(True)
        self.assertEqual(isinstance(value_object, BooleanObject), True)
        self.assertEqual(value_object.get_value(), True)
        value_object = self.boolean_class.create_object(False)
        self.assertEqual(isinstance(value_object, BooleanObject), True)
        self.assertEqual(value_object.get_value(), False)

    def test_read_object(self):
        value_object = self.boolean_class.read_object(True)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.read_object(False)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.read_object('True')
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.read_object('False')
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.read_object(0)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        value_object = self.boolean_class.read_object(-2381)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.read_object(99)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.read_object(None)
        self.assertEqual(value_object, BooleanClass.FalseObject)
        some_object = dict()
        value_object = self.boolean_class.read_object(some_object)
        self.assertEqual(value_object, BooleanClass.TrueObject)
        value_object = self.boolean_class.read_object(True)
        self.assertEqual(isinstance(value_object, BooleanObject), True)
        self.assertEqual(value_object.get_value(), True)
        value_object = self.boolean_class.read_object(False)
        self.assertEqual(isinstance(value_object, BooleanObject), True)
        self.assertEqual(value_object.get_value(), False)

    def test_to_json(self):
        json_value = self.boolean_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'BooleanTest')
        self.assertEqual(json_value.get('type'), 'boolean')
        value_object = self.boolean_class.create_object(True)
        json_value = value_object.to_serializable()
        self.assertEqual(json_value, True)


if __name__ == '__main__':
    unittest.main()
