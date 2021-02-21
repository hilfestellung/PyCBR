import unittest

from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.SetClass import SetClass
from cbrlib.model.SetObject import SetObject


class TestSetClass(unittest.TestCase):

    def setUp(self) -> None:
        self.integer_class = IntegerClass('Price')
        self.set_class = SetClass('SetTest', self.integer_class)

    def test_create_object(self):
        value_object = self.set_class.create_object([42, 101])
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))
        value_object = self.set_class.create_object({42, 101})
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))
        value_object = self.set_class.create_object((42, 101))
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))

    def test_read_object(self):
        value_object = self.set_class.read_object([42, 101])
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))
        value_object = self.set_class.read_object({42, 101})
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))
        value_object = self.set_class.read_object((42, 101))
        self.assertEqual(value_object,
                         SetObject({self.integer_class.create_object(42), self.integer_class.create_object(101)}))

    def test_to_serializable(self):
        serializable = self.set_class.to_serializable()
        self.assertEqual(serializable.get('id'), 'SetTest')
        self.assertEqual(serializable.get('type'), 'set')
        self.assertEqual(serializable.get('elementClass'), 'Price')
        value_object = self.set_class.create_object({42, 101})
        serializable = value_object.to_serializable()
        self.assertListEqual(serializable, [42, 101])


if __name__ == '__main__':
    unittest.main()
