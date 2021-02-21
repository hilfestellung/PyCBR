import unittest

from cbrlib.evaluation.LookupTableEvaluator import LookupTableEvaluator
from cbrlib.model.IntegerObject import IntegerObject


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.table = {
            10: {
                20: 0.4,
                30: 0.3
            },
            20: {
                10: 0.2,
                30: 0.5
            }
        }
        self.evaluator = LookupTableEvaluator('LookupTest', self.table)

    def test_typename(self):
        self.assertEqual(self.evaluator.get_typename(), 'lookup')

    def test_evaluate(self):
        self.assertEqual(self.evaluator.get_name(), 'LookupTest')
        obj10 = IntegerObject(10)
        obj20 = IntegerObject(20)
        obj30 = IntegerObject(30)
        obj40 = IntegerObject(40)
        self.assertEqual(self.evaluator.evaluate(obj20, obj20), 1)
        self.assertEqual(self.evaluator.evaluate(obj40, obj40), 1)
        self.assertEqual(self.evaluator.evaluate(obj10, obj20), 0.4)
        self.assertEqual(self.evaluator.evaluate(obj20, obj10), 0.2)
        self.assertEqual(self.evaluator.evaluate(obj10, obj30), 0.3)
        self.assertEqual(self.evaluator.evaluate(obj20, obj30), 0.5)
        self.assertEqual(self.evaluator.evaluate(obj40, obj20), 0)
        self.assertEqual(self.evaluator.evaluate(obj20, obj40), 0)

    def test_to_serializable(self):
        serializable = self.evaluator.to_serializable()
        self.assertEqual(serializable.get('name'), 'LookupTest')
        self.assertEqual(serializable.get('type'), 'lookup')
        self.assertDictEqual(serializable.get('table'), self.table)


if __name__ == '__main__':
    unittest.main()
