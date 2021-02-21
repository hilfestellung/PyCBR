import unittest

from cbrlib.evaluation.AssemblyAverageEvaluator import AssemblyAverageEvaluator
from cbrlib.evaluation.AssemblyEuclideanEvaluator import AssemblyEuclideanEvaluator
from cbrlib.evaluation.AssemblyMaxEvaluator import AssemblyMaxEvaluator
from cbrlib.evaluation.AssemblyMinEvaluator import AssemblyMinEvaluator
from cbrlib.evaluation.LookupTableEvaluator import LookupTableEvaluator
from cbrlib.model.AssemblyClass import AssemblyClass
from cbrlib.model.Attribute import Attribute
from cbrlib.model.EnumerationPredicate import EnumerationPredicate
from cbrlib.model.FloatClass import FloatClass
from cbrlib.model.RangePredicate import RangePredicate
from cbrlib.model.StringClass import StringClass
from cbrlib.utils.serializer import to_json_string


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        color_class = StringClass('SimpleColor')
        self.colors = [
            color_class.create_object('red'),
            color_class.create_object('green'),
            color_class.create_object('yellow'),
            color_class.create_object('blue'),
            color_class.create_object('orange'),
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
        self.evaluators = dict()
        color_evaluator = LookupTableEvaluator('ColorCircle', {
            'red': {
                'orange': 0.7,
                'yellow': 0.4
            },
            'orange': {
                'red': 0.5,
                'yellow': 0.5
            }
        })
        self.evaluators['color'] = {
            'weight': 1.0,
            'evaluator': color_evaluator
        }

    def test_average(self):
        assembly_evaluator = AssemblyAverageEvaluator('AverageTest', self.evaluators)
        self.assertEqual(assembly_evaluator.get_typename(), 'assembly-average')
        query1 = self.assembly_class.create_object({'color': 'red'})
        query2 = self.assembly_class.create_object({'color': 'red', 'price': 1000})
        query3 = self.assembly_class.create_object({'color': 'red', 'price': 999})
        query4 = self.assembly_class.create_object({'color': 'orange', 'price': 1000})
        case = self.assembly_class.create_object({'id': '1', 'color': 'red', 'price': 1000})
        self.assertEqual(assembly_evaluator.evaluate(query1, case), 1)
        self.assertEqual(assembly_evaluator.evaluate(query2, case), 1)
        self.assertEqual(assembly_evaluator.evaluate(query3, case), 0.5)
        self.assertEqual(assembly_evaluator.evaluate(query4, case), 0.75)

    def test_min(self):
        assembly_evaluator = AssemblyMinEvaluator('AverageTest', self.evaluators)
        query1 = self.assembly_class.create_object({'color': 'red'})
        query2 = self.assembly_class.create_object({'color': 'red', 'price': 1000})
        query3 = self.assembly_class.create_object({'color': 'orange', 'price': 999})
        query4 = self.assembly_class.create_object({'color': 'orange', 'price': 1000})
        case = self.assembly_class.create_object({'id': '1', 'color': 'red', 'price': 1000})
        self.assertEqual(assembly_evaluator.evaluate(query1, case), 1)
        self.assertEqual(assembly_evaluator.evaluate(query2, case), 1)
        self.assertEqual(assembly_evaluator.evaluate(query3, case), 0.5)
        self.assertEqual(assembly_evaluator.evaluate(query4, case), 0.5)

    def test_max(self):
        assembly_evaluator = AssemblyMaxEvaluator('AverageTest', self.evaluators)
        query1 = self.assembly_class.create_object({'color': 'red'})
        query2 = self.assembly_class.create_object({'color': 'red', 'price': 1000})
        query3 = self.assembly_class.create_object({'color': 'orange', 'price': 999})
        query4 = self.assembly_class.create_object({'color': 'red', 'price': 999})
        case1 = self.assembly_class.create_object({'id': '1', 'color': 'red', 'price': 1000})
        case2 = self.assembly_class.create_object({'id': '2', 'color': 'orange', 'price': 1000})
        self.assertEqual(assembly_evaluator.evaluate(query1, case1), 1)
        self.assertEqual(assembly_evaluator.evaluate(query2, case1), 1)
        self.assertEqual(assembly_evaluator.evaluate(query3, case1), 0.5)
        self.assertEqual(assembly_evaluator.evaluate(query4, case2), 0.7)

    def test_euclidean(self):
        assembly_evaluator = AssemblyEuclideanEvaluator('AverageTest', self.evaluators)
        query1 = self.assembly_class.create_object({'color': 'red'})
        query2 = self.assembly_class.create_object({'color': 'red', 'price': 1000})
        query3 = self.assembly_class.create_object({'color': 'orange', 'price': 999})
        query4 = self.assembly_class.create_object({'color': 'red', 'price': 999})
        case1 = self.assembly_class.create_object({'id': '1', 'color': 'red', 'price': 1000})
        case2 = self.assembly_class.create_object({'id': '2', 'color': 'orange', 'price': 1000})
        self.assertEqual(assembly_evaluator.evaluate(query1, case1), 1)
        self.assertEqual(assembly_evaluator.evaluate(query2, case1), 1)
        self.assertEqual(assembly_evaluator.evaluate(query3, case1), 0.5)
        self.assertEqual(assembly_evaluator.evaluate(query4, case2), 0.7)

    def test_to_serializable(self):
        assembly_evaluator = AssemblyEuclideanEvaluator('AverageTest', self.evaluators)
        print(to_json_string(assembly_evaluator))


if __name__ == '__main__':
    unittest.main()
