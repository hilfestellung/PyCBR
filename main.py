from cbrlib.reasoning.Reasoner import InferenceOptions
from cbrlib.utils.serializer import to_json_string
from cbrlib.evaluation.AssemblyAverageEvaluator import AssemblyAverageEvaluator
from cbrlib.evaluation.LookupTableEvaluator import LookupTableEvaluator
from cbrlib.evaluation.NumberInterpolationEvaluator import NumberInterpolationMetrics, NumberInterpolation, \
    NumberInterpolationEvaluator
from cbrlib.model.AssemblyClass import AssemblyClass
from cbrlib.model.Attribute import Attribute
from cbrlib.model.EnumerationPredicate import EnumerationPredicate
from cbrlib.model.FloatClass import FloatClass
from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.RangePredicate import RangePredicate

from cbrlib.model.StringClass import StringClass
from cbrlib.reasoning.LinearReasoner import LinearReasoner

from functools import reduce

from random import choice, randint
import timeit

class NumberInterpolationMode(object):
    pass


def sample_model():
    price_class = FloatClass('Price')
    price_min = price_class.create_object(10)
    price_max = price_class.create_object(100000)
    price_class.set_predicate(RangePredicate(price_min, price_max))

    metrics = NumberInterpolationMetrics()
    metrics.tolerance_if_less = 0.0
    metrics.origin = price_min.get_value()
    metrics.use_origin = True
    metrics.tolerance_if_less = 0.3
    metrics.tolerance_if_more = 0.1
    metrics.linearity_if_less = 0.5
    metrics.linearity_if_more = 3
    metrics.set_interpolation_if_less(NumberInterpolation.Sigmoid)
    metrics.set_interpolation_if_more(NumberInterpolation.Sigmoid)
    real_behaviour = NumberInterpolationEvaluator('RealBehaviour',
                                                  price_min.get_value(), price_max.get_value(), metrics)

    mileage_class = IntegerClass('Mileage')
    mileage_min = mileage_class.create_object(0)
    mileage_max = mileage_class.create_object(1000000)
    mileage_class.set_predicate(RangePredicate(mileage_min, mileage_max))

    mileage_evaluator = NumberInterpolationEvaluator('MileageDefault',
                                                     mileage_min.get_value(), mileage_max.get_value(), metrics)
    brand_class = StringClass('Brand')
    brands = ['Opel', 'Daimler Benz', 'BMW', 'VW']
    brand_class.set_predicate(EnumerationPredicate(
        map(lambda b: brand_class.create_object(b), brands)))

    brand_similarity = {
        'Opel': {
            'VW': 0.6,
            'BMW': 0.3,
            'Daimler Benz': 0.1
        },
        'Daimler Benz': {
            'BMW': 0.8,
            'VW': 0.4,
            'Opel': 0.1
        },
        'BMW': {
            'Daimler Benz': 0.8,
            'VW': 0.6,
            'Opel': 0.1
        },
        'VW': {
            'BMW': 0.8,
            'Daimler Benz': 0.8,
            'Opel': 0.6,
        }
    }
    brand_evaluator = LookupTableEvaluator('Brand', brand_similarity)

    used_car_class = AssemblyClass('UsedCar', [
        Attribute('price', price_class),
        Attribute('mileage0', mileage_class),
        Attribute('mileage1', mileage_class),
        Attribute('mileage2', mileage_class),
        Attribute('mileage3', mileage_class),
        Attribute('mileage4', mileage_class),
        Attribute('brand', brand_class)
    ])
    cars = []
    for c in range(1000000):
        cars.append({
            'price': randint(10, 100000),
            'mileage0': randint(0, 1000000),
            'mileage1': randint(0, 1000000),
            'mileage2': randint(0, 1000000),
            'mileage3': randint(0, 1000000),
            'mileage4': randint(0, 1000000),
            'brand': choice(brands)
        })
    reasoner = LinearReasoner(map(lambda c: used_car_class.read_object(c), cars), AssemblyAverageEvaluator('UsedCarEvaluator', {
        'price': {
            'weight': 2,
            'evaluator': real_behaviour
        },
        'mileage': {
            'weight': 1,
            'evaluator': mileage_evaluator
        },
        'brand': {
            'weight': 1,
            'evaluator': brand_evaluator
        }
    }))
    price = randint(10, 100000)
    mileage0 = randint(0, 1000000)
    mileage1 = randint(0, 1000000)
    mileage2 = randint(0, 1000000)
    mileage3 = randint(0, 1000000)
    mileage4 = randint(0, 1000000)
    brand = choice(brands)
    loops = 100000
    repetitions = 5
    task = timeit.Timer(lambda: reasoner.infer(
        used_car_class.read_object({
            'price': price,
            'mileage0': mileage0,
            'mileage1': mileage1,
            'mileage2': mileage2,
            'mileage3': mileage3,
            'mileage4': mileage4,
            'brand': brand
        }), InferenceOptions({
            'skip': 0,
            'limit': 10
        })
        ))
    measures = task.repeat(repetitions, loops)
    best = reduce(lambda c, n: min(c, n), measures)
    worst = reduce(lambda c, n: max(c, n), measures)
    print(measures)
    print(f'{loops} loops, best of {repetitions}: {best*1000} ms per loop, worst of {repetitions}: {worst*1000} ms per loop')


if __name__ == '__main__':
    sample_model()
