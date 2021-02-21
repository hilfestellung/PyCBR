from cbrlib.utils.serializer import to_json_string
from cbrlib.evaluation.AssemblyAverageEvaluator import AssemblyAverageEvaluator
from cbrlib.evaluation.NumberInterpolationEvaluator import NumberInterpolationMetrics, NumberInterpolation, \
    NumberInterpolationEvaluator
from cbrlib.model.AssemblyClass import AssemblyClass
from cbrlib.model.Attribute import Attribute
from cbrlib.model.EnumerationPredicate import EnumerationPredicate
from cbrlib.model.FloatClass import FloatClass
from cbrlib.model.IntegerClass import IntegerClass
from cbrlib.model.RangePredicate import RangePredicate

from cbrlib.model.StringClass import StringClass
from cbrlib.reasoning.Reasoner import Reasoner


class NumberInterpolationMode(object):
    pass


def sample_model():
    price_class = FloatClass('Price')
    price_min = price_class.create_object(10)
    price_max = price_class.create_object(10000)
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
    brand_class.set_predicate(EnumerationPredicate(map(lambda b: brand_class.create_object(b), brands)))

    used_car_class = AssemblyClass('UsedCar', [
        Attribute('price', price_class),
        Attribute('mileage', mileage_class),
        Attribute('brand', brand_class)
    ])
    cars = [
        {
            'price': 3200,
            'mileage': 120000
        },
        {
            'price': 2700,
            'mileage': 170000
        },
        {
            'price': 2950,
            'mileage': 150000
        },
        {
            'price': 3100,
            'mileage': 99900
        },
        {
            'price': 3050,
            'mileage': 110000
        },
        {
            'price': 2400,
            'mileage': 210000
        },
    ]
    reasoner = Reasoner('UsedCar', map(lambda c: used_car_class.read_object(c), cars), AssemblyAverageEvaluator('', {
        'price': {
            'weight': 2,
            'evaluator': real_behaviour
        },
        'mileage': {
            'weight': 1,
            'evaluator': mileage_evaluator
        }
    }))
    print(to_json_string(reasoner.infer(used_car_class.read_object({
        'price': 3000,
        'mileage': 90000
    }))))


if __name__ == '__main__':
    sample_model()
