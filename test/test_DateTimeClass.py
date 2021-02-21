import unittest
from datetime import datetime, date

from cbrlib.model.DateTimeClass import DateTimeClass
from cbrlib.model.DateTimeObject import DateTimeObject


class TestDateTimeClass(unittest.TestCase):

    def setUp(self) -> None:
        self.datetime_class = DateTimeClass('DateTimeTest')

    def test_typename(self):
        self.assertEqual(self.datetime_class.get_typename(), 'datetime')

    def test_create_object(self):
        value_object = self.datetime_class.create_object(datetime.fromisoformat('2021-02-28 18:30:27.456'))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        value_object = self.datetime_class.create_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 00:00:00.000')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 00:00:00.000'))
        value_object = self.datetime_class.create_object(1614533427456)
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        value_object = self.datetime_class.create_object(float(1614533427456))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        try:
            value_object = self.datetime_class.create_object(dict())
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_read_object(self):
        value_object = self.datetime_class.read_object(datetime.fromisoformat('2021-02-28 18:30:27.456'))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        value_object = self.datetime_class.read_object(date.fromisoformat('2021-02-28'))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 00:00:00.000')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 00:00:00.000'))
        value_object = self.datetime_class.read_object(1614533427456)
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        value_object = self.datetime_class.read_object(float(1614533427456))
        self.assertEqual(value_object, DateTimeObject(datetime.fromisoformat('2021-02-28 18:30:27.456')))
        self.assertEqual(value_object.get_value(), datetime.fromisoformat('2021-02-28 18:30:27.456'))
        try:
            value_object = self.datetime_class.read_object(dict())
        except ValueError:
            value_object = 'Expression before should fail'
        self.assertEqual('Expression before should fail', value_object)

    def test_to_json(self):
        json_value = self.datetime_class.to_serializable()
        self.assertEqual(json_value.get('id'), 'DateTimeTest')
        self.assertEqual(json_value.get('type'), 'datetime')
        value_object = self.datetime_class.read_object('2021-02-28 18:30:27.456')
        json_value = value_object.to_serializable()
        self.assertEqual(json_value, datetime.fromisoformat('2021-02-28 18:30:27.456'))


if __name__ == '__main__':
    unittest.main()
