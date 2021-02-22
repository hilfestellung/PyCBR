import unittest

from cbrlib.evaluation.SetEvaluator import SetEvaluationMode, SetEvaluator
from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.SetClass import SetClass
from cbrlib.utils.serializer import to_json_string


class TestSetEvaluator(unittest.TestCase):

    def setUp(self) -> None:
        self.integer_class = IntegerClass('Integer')
        self.set_class = SetClass('SetClass', element_class=self.integer_class)

    def test_case_inclusion(self):
        set_evaluator = SetEvaluator('SetEvaluatorTest', SetEvaluationMode.CaseInclusion)
        set1 = self.set_class.read_object({1, 2, 3})
        set2 = self.set_class.read_object({1, 2})
        self.assertEqual(set_evaluator.evaluate(set1, set2), 1)
        self.assertEqual(set_evaluator.evaluate(set2, set1), 0.6666666666666666)

    def test_query_inclusion(self):
        set_evaluator = SetEvaluator('SetEvaluatorTest', SetEvaluationMode.QueryInclusion)
        set1 = self.set_class.read_object({1, 2})
        set2 = self.set_class.read_object({1, 2, 3})
        self.assertEqual(set_evaluator.evaluate(set1, set2), 1)
        self.assertEqual(set_evaluator.evaluate(set2, set1), 0.6666666666666666)

    def test_query_inclusion(self):
        set_evaluator = SetEvaluator('SetEvaluatorTest', SetEvaluationMode.Intermediate)
        set1 = self.set_class.read_object({1, 2})
        set2 = self.set_class.read_object({1, 2, 3})
        self.assertEqual(set_evaluator.evaluate(set1, set2), 0.8333333333333333)
        self.assertEqual(set_evaluator.evaluate(set2, set1), 0.8333333333333333)

    def test_to_serializable(self):
        set_evaluator = SetEvaluator('SetEvaluatorTest', SetEvaluationMode.Intermediate)
        print(to_json_string(set_evaluator.to_serializable()))


if __name__ == '__main__':
    unittest.main()
