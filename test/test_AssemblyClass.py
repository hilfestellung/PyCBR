import unittest

from cbrlib.model.AssemblyClass import AssemblyClass
from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.model.Attribute import Attribute
from cbrlib.model.EnumerationPredicate import EnumerationPredicate
from cbrlib.model.FloatClass import FloatClass
from cbrlib.model.FloatObject import FloatObject
from cbrlib.model.RangePredicate import RangePredicate
from cbrlib.model.StringClass import StringClass
from cbrlib.model.StringObject import StringObject


class TestAssemblyClass(unittest.TestCase):

    def setUp(self) -> None:
        color_class = StringClass('SimpleColor')
        self.colors = [
            color_class.create_object('red'),
            color_class.create_object('green'),
            color_class.create_object('yellow'),
            color_class.create_object('blue')
        ]
        color_class.set_predicate(EnumerationPredicate(self.colors))
        price_class = FloatClass('Price')
        price_class.set_predicate(RangePredicate(price_class.create_object(0), price_class.create_object(100000)))
        attributes = [
            Attribute('id', StringClass('Identifier')),
            Attribute('color', color_class),
            Attribute('price', price_class),
        ]
        self.assembly_class = AssemblyClass('AssemblyTest', attributes)

    def test_create_object(self):
        value_object = self.assembly_class.create_object([('color', 'red'), ('price', 999.9), ('id', '1')])
        value_object.__class__ = AssemblyObject
        self.assertEqual(value_object.get_attribute_value('id'), StringObject('1'))
        self.assertIs(value_object.get_attribute_value('color'), self.colors[0])
        self.assertEqual(value_object.get_attribute_value('price'), FloatObject(999.9))

        value_object = self.assembly_class.create_object({'color': 'yellow', 'price': 10000.24, 'id': '2'})
        value_object.__class__ = AssemblyObject
        self.assertEqual(value_object.get_attribute_value('id'), StringObject('2'))
        self.assertIs(value_object.get_attribute_value('color'), self.colors[2])
        self.assertEqual(value_object.get_attribute_value('price'), FloatObject(10000.24))

        value_object = self.assembly_class.create_object((('color', 'green'), ('price', 50000), ('id', '3')))
        value_object.__class__ = AssemblyObject
        self.assertEqual(value_object.get_attribute_value('id'), StringObject('3'))
        self.assertIs(value_object.get_attribute_value('color'), self.colors[1])
        self.assertEqual(value_object.get_attribute_value('price'), FloatObject(50000))

    def test_to_serializable(self):
        serializable = self.assembly_class.to_serializable()
        self.assertEqual(serializable.get('id'), 'AssemblyTest')
        self.assertEqual(serializable.get('type'), 'assembly')
        self.assertIsInstance(serializable.get('attributes'), list)
        try:
            color = filter(lambda a: a.get('id') == 'color', serializable.get('attributes')).__next__()
            self.assertEqual(color['class']['id'], 'SimpleColor')
            self.assertListEqual(color['class']['enumeration'], ['blue', 'green', 'red', 'yellow'])
        except StopIteration:
            self.assertEqual('color must be found.', 'color was not found.')
        value_object = self.assembly_class.create_object((('color', 'green'), ('price', 50000), ('id', '3')))
        serializable = value_object.to_serializable()
        self.assertEqual(serializable.get('color'), 'green')
        self.assertEqual(serializable.get('id'), '3')
        self.assertEqual(serializable.get('price'), 50000.0)


if __name__ == '__main__':
    unittest.main()
