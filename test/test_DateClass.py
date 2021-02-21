import unittest
from datetime import date, datetime

from cbrlib.model.DateClass import DateClass
from cbrlib.model.DateObject import DateObject


class TestDateClass(unittest.TestCase):

    def setUp(self) -> None:
        self.date_class = DateClass('DateTest')

    def test_typename(self):
        self.assertEqual(self.date_class.get_typename(), 'date')

    def test_create_object(self):
        value_object = self.date_class.create_object('2021-02-15')
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-15')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-15'))
        value_object = self.date_class.create_object(1614470400000)
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-28')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-28'))
        value_object = self.date_class.create_object(datetime.fromisoformat('2021-02-26 18:30:12.567'))
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-26')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-26'))
        value_object = self.date_class.create_object(date.fromisoformat('2021-02-27'))
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-27')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-27'))
        try:
            value_object = self.date_class.create_object(dict())
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_read_object(self):
        value_object = self.date_class.read_object('2021-02-15')
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-15')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-15'))
        value_object = self.date_class.read_object(1614470400000)
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-28')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-28'))
        value_object = self.date_class.read_object(datetime.fromisoformat('2021-02-26 18:30:12.567'))
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-26')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-26'))
        value_object = self.date_class.read_object(date.fromisoformat('2021-02-27'))
        self.assertEqual(value_object, DateObject(date.fromisoformat('2021-02-27')))
        self.assertEqual(value_object.get_value(), date.fromisoformat('2021-02-27'))
        try:
            value_object = self.date_class.read_object(dict())
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_to_json(self):
        json_value = self.date_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'DateTest')
        self.assertEqual(json_value.get('type'), 'date')
        value_object = self.date_class.read_object('2021-02-15')
        json_value = value_object.to_serializable()
        self.assertEqual(json_value, date.fromisoformat('2021-02-15'))


if __name__ == '__main__':
    unittest.main()
