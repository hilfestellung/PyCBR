import unittest
from datetime import date, datetime

from cbrlib.utils.time import date_to_unixtimestamp, datetime_to_unixtimestamp


class MyTestCase(unittest.TestCase):

    def test_date_to_datetime(self):
        date_ = date.fromisoformat('2021-02-28')
        self.assertEqual(date_to_unixtimestamp(date_), 1614470400000)

    def test_datetime_to_datetime(self):
        datetime_ = datetime.fromisoformat('2021-02-28 18:05:42.924')
        self.assertEqual(datetime_to_unixtimestamp(datetime_), 1614535542924)


if __name__ == '__main__':
    unittest.main()
