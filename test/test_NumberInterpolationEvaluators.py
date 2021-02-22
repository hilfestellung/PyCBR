import unittest

from cbrlib.evaluation.NumberInterpolationEvaluator import NumberInterpolationEvaluator, NumberInterpolationMetrics
from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.utils.serializer import to_json_string


class TestNumberInterpolationEvaluators(unittest.TestCase):

    def setUp(self) -> None:
        self.integer_class = IntegerClass('Integer')

    def test_default(self):
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000)
        query = self.integer_class.read_object(500)
        case1 = self.integer_class.read_object(100)
        case2 = self.integer_class.read_object(200)
        case3 = self.integer_class.read_object(250)
        case4 = self.integer_class.read_object(300)
        case5 = self.integer_class.read_object(400)
        case6 = self.integer_class.read_object(500)
        self.assertAlmostEqual(number_evaluator.evaluate(query, case1), 0.2)
        self.assertAlmostEqual(number_evaluator.evaluate(case1, query), 0.2)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case2), 0.4)
        self.assertAlmostEqual(number_evaluator.evaluate(case2, query), 0.4)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case3), 0.5)
        self.assertAlmostEqual(number_evaluator.evaluate(case3, query), 0.5)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case4), 0.6)
        self.assertAlmostEqual(number_evaluator.evaluate(case4, query), 0.6)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case5), 0.8)
        self.assertAlmostEqual(number_evaluator.evaluate(case5, query), 0.8)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case6), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case6, query), 1)

    def test_high_linearity(self):
        metrics = NumberInterpolationMetrics()
        metrics.linearity_if_less = 3.0
        metrics.linearity_if_more = 3.0
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000, metrics)
        query = self.integer_class.read_object(500)
        case1 = self.integer_class.read_object(50)
        case2 = self.integer_class.read_object(100)
        case3 = self.integer_class.read_object(200)
        case4 = self.integer_class.read_object(300)
        case5 = self.integer_class.read_object(400)
        case6 = self.integer_class.read_object(500)
        self.assertAlmostEqual(number_evaluator.evaluate(query, case1), 0.46415888)
        self.assertAlmostEqual(number_evaluator.evaluate(case1, query), 0.46415888)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case2), 0.58480354)
        self.assertAlmostEqual(number_evaluator.evaluate(case2, query), 0.58480354)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case3), 0.73680629)
        self.assertAlmostEqual(number_evaluator.evaluate(case3, query), 0.73680629)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case4), 0.84343266)
        self.assertAlmostEqual(number_evaluator.evaluate(case4, query), 0.84343266)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case5), 0.92831776)
        self.assertAlmostEqual(number_evaluator.evaluate(case5, query), 0.92831776)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case6), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case6, query), 1)

    def test_low_linearity(self):
        metrics = NumberInterpolationMetrics()
        metrics.linearity_if_less = 0.5
        metrics.linearity_if_more = 0.5
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000, metrics)
        query = self.integer_class.read_object(500)
        case1 = self.integer_class.read_object(100)
        case2 = self.integer_class.read_object(200)
        case3 = self.integer_class.read_object(300)
        case4 = self.integer_class.read_object(400)
        case5 = self.integer_class.read_object(450)
        case6 = self.integer_class.read_object(500)
        self.assertAlmostEqual(number_evaluator.evaluate(query, case1), 0.04)
        self.assertAlmostEqual(number_evaluator.evaluate(case1, query), 0.04)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case2), 0.16)
        self.assertAlmostEqual(number_evaluator.evaluate(case2, query), 0.16)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case3), 0.36)
        self.assertAlmostEqual(number_evaluator.evaluate(case3, query), 0.36)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case4), 0.64)
        self.assertAlmostEqual(number_evaluator.evaluate(case4, query), 0.64)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case5), 0.81)
        self.assertAlmostEqual(number_evaluator.evaluate(case5, query), 0.81)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case6), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case6, query), 1)

    def test_equality(self):
        metrics = NumberInterpolationMetrics()
        metrics.linearity_if_less = 0.5
        metrics.linearity_if_more = 0.5
        metrics.equal_if_less = 0.1
        metrics.equal_if_more = 0.1
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000, metrics)
        query = self.integer_class.read_object(500)
        case1 = self.integer_class.read_object(100)
        case2 = self.integer_class.read_object(200)
        case3 = self.integer_class.read_object(300)
        case4 = self.integer_class.read_object(400)
        case5 = self.integer_class.read_object(450)
        case6 = self.integer_class.read_object(500)
        self.assertAlmostEqual(number_evaluator.evaluate(query, case1), 0.06249999)
        self.assertAlmostEqual(number_evaluator.evaluate(case1, query), 0.06249999)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case2), 0.25)
        self.assertAlmostEqual(number_evaluator.evaluate(case2, query), 0.25)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case3), 0.5625)
        self.assertAlmostEqual(number_evaluator.evaluate(case3, query), 0.5625)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case4), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case4, query), 1)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case5), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case5, query), 1)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case6), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case6, query), 1)

    def test_tolerance(self):
        metrics = NumberInterpolationMetrics()
        metrics.tolerance_if_more = 0.3
        metrics.tolerance_if_less = 0.3
        metrics.linearity_if_less = 0.5
        metrics.linearity_if_more = 0.5
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000, metrics)
        query = self.integer_class.read_object(500)
        case1 = self.integer_class.read_object(200)
        case2 = self.integer_class.read_object(250)
        case3 = self.integer_class.read_object(300)
        case4 = self.integer_class.read_object(350)
        case5 = self.integer_class.read_object(400)
        case6 = self.integer_class.read_object(500)
        self.assertAlmostEqual(number_evaluator.evaluate(query, case1), 0)
        self.assertAlmostEqual(number_evaluator.evaluate(case1, query), 0)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case2), 0.02777777)
        self.assertAlmostEqual(number_evaluator.evaluate(case2, query), 0.02777777)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case3), 0.11111111)
        self.assertAlmostEqual(number_evaluator.evaluate(case3, query), 0.11111111)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case4), 0.25)
        self.assertAlmostEqual(number_evaluator.evaluate(case4, query), 0.25)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case5), 0.44444444)
        self.assertAlmostEqual(number_evaluator.evaluate(case5, query), 0.44444444)

        self.assertAlmostEqual(number_evaluator.evaluate(query, case6), 1)
        self.assertAlmostEqual(number_evaluator.evaluate(case6, query), 1)

    def test_to_serializable(self):
        metrics = NumberInterpolationMetrics()
        metrics.tolerance_if_more = 0.3
        metrics.tolerance_if_less = 0.3
        metrics.linearity_if_less = 0.5
        metrics.linearity_if_more = 0.5
        number_evaluator = NumberInterpolationEvaluator('NumberEvaluationTest', 0, 1000, metrics)
        print(to_json_string(number_evaluator.to_serializable()))


if __name__ == '__main__':
    unittest.main()
