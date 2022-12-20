import dataclasses
import functools
import math
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from statistics import median
from typing import Any, Callable, Iterable

Evaluator = Callable[[Any, Any], float]

PropertyEvaluatorMapping = namedtuple(
    "PropertyEvaluatorMapping",
    {"property_name", "evaluator"},
)

WeightedPropertyEvaluatorMapping = namedtuple(
    "WeightedPropertyEvaluatorMapping",
    {"property_name", "weight", "evaluator"},
)


def case_average_evaluator(mappings: Iterable[WeightedPropertyEvaluatorMapping], query: Any, case: Any) -> float:
    divider = 0
    similarity_sum = 0
    for property_name, weight, evaluator in mappings:
        query_value = getattr(query, property_name)
        if query_value is None:
            continue
        divider += weight
        case_value = getattr(case, property_name)
        similarity_sum += weight * evaluator(query_value, case_value)
    if divider <= 0:
        return 0
    return similarity_sum / divider


def case_euclidean_evaluator(mappings: Iterable[PropertyEvaluatorMapping], query: Any, case: Any) -> float:
    similarity_sum = 0
    for property_name, evaluator in mappings:
        query_value = getattr(query, property_name)
        if query_value is None:
            continue
        case_value = getattr(case, property_name)
        similarity = evaluator(query_value, case_value)
        if similarity <= 0:
            continue
        similarity_sum += similarity**2
    return math.sqrt(similarity_sum)


def case_min_evaluator(mappings: Iterable[PropertyEvaluatorMapping], query: Any, case: Any) -> float:
    similarity_result = 0
    for property_name, evaluator in mappings:
        query_value = getattr(query, property_name)
        if query_value is None:
            continue
        case_value = getattr(case, property_name)
        similarity = evaluator(query_value, case_value)
        if similarity <= 0:
            continue
        similarity_result = min(similarity_result, similarity)
    return similarity_result


def case_max_evaluator(mappings: Iterable[PropertyEvaluatorMapping], query: Any, case: Any) -> float:
    similarity_result = 0
    for property_name, evaluator in mappings:
        query_value = getattr(query, property_name)
        if query_value is None:
            continue
        case_value = getattr(case, property_name)
        similarity = evaluator(query_value, case_value)
        if similarity <= 0:
            continue
        similarity_result = max(similarity_result, similarity)
    return similarity_result


def case_median_evaluator(mappings: Iterable[PropertyEvaluatorMapping], query: Any, case: Any) -> float:
    divider = 0
    similarity_results = []
    for property_name, evaluator in mappings:
        query_value = getattr(query, property_name)
        if query_value is None:
            continue
        case_value = getattr(case, property_name)
        similarity = evaluator(query_value, case_value)
        if similarity <= 0:
            continue
        similarity_results.append(similarity)
    if divider <= 0:
        return 0
    return median(similarity_results)


def _contains(query: Any, bulk: set[Any], evaluator: Evaluator) -> float:
    count = 0
    similarity_sum = 0
    for element in bulk:
        similarity = evaluator(query, element)
        if similarity == 1:
            return 1
        similarity_sum += similarity
        count += 1
    if count == 0:
        return 0
    return similarity_sum / count


def set_query_inclusion_evaluator(query: set[Any], case: set[Any], evaluator: Evaluator) -> float:
    size_of_query = len(query)
    if size_of_query == 0:
        return 0
    current = functools.reduce(lambda e1, e2: e1 + _contains(e2, case, evaluator), [0, *query])
    return float(current) / size_of_query


def set_case_inclusion_evaluator(query: set[Any], case: set[Any], evaluator: Evaluator) -> float:
    return set_query_inclusion_evaluator(case, query, evaluator)


def set_intermediate_inclusion(query: set[Any], case: set[Any], evaluator: Evaluator) -> float:
    a = set_query_inclusion_evaluator(case, query, evaluator)
    b = set_query_inclusion_evaluator(query, case, evaluator)
    return (a + b) / 2


def _calculate_distance(v1: float, v2: float, max_distance: float, cyclic: bool) -> float:
    result = abs(v2 - v1)
    if cyclic and result > max_distance:
        return 2 * max_distance - result
    return result


def _calculate_max_distance(v: float, max_distance: float, origin: float, use_origin: bool) -> float:
    if use_origin:
        return abs(v - origin)
    return max_distance


def _is_less(v1: float, v2: float, max_distance: float, cyclic: bool) -> bool:
    less = v1 < v2
    if cyclic:
        if less:
            left_distance = v2 - v1
        else:
            left_distance = 2 * max_distance - v1 + v2
        right_distance = 2 * max_distance - left_distance
        return left_distance < right_distance
    return less


def _interpolate_polynom(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    elif linearity == 0:
        return 0
    return pow(1 - stretched_distance, 1 / linearity)


def _interpolate_root(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    elif linearity == 0:
        return 1
    return pow(1 - stretched_distance, linearity)


def _interpolate_sigmoid(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    if stretched_distance < 0.5:
        if linearity == 0:
            return 1
        return 1 - pow(2 * stretched_distance, 1 / linearity) / 2
    if linearity == 0:
        return 0
    return pow(2 - 2 * stretched_distance, 1 / linearity) / 2


class NumberInterpolation(Enum):
    POLYNOM = 1
    SIGMOID = 2
    ROOT = 3


_interpolations = {
    NumberInterpolation.POLYNOM: _interpolate_polynom,
    NumberInterpolation.ROOT: _interpolate_root,
    NumberInterpolation.SIGMOID: _interpolate_sigmoid,
}


@dataclass(slots=True, frozen=True)
class NumericEvaluationOptions:
    min_: float
    max_: float

    origin: float = dataclasses.field(default=0)
    use_origin: bool = dataclasses.field(default=False)

    cyclic: bool = dataclasses.field(default=False)

    equal_if_less: float = dataclasses.field(default=0.0)
    tolerance_if_less: float = dataclasses.field(default=0.5)
    linearity_if_less: float = dataclasses.field(default=1.0)
    interpolation_if_less: NumberInterpolation = dataclasses.field(default=NumberInterpolation.POLYNOM)

    equal_if_more: float = dataclasses.field(default=0.0)
    tolerance_if_more: float = dataclasses.field(default=0.5)
    linearity_if_more: float = dataclasses.field(default=1.0)
    interpolation_if_more: NumberInterpolation = dataclasses.field(default=NumberInterpolation.POLYNOM)

    def __post_init__(self) -> None:
        min_ = self.min_
        max_ = self.max_
        if max_ < min_:
            max_, min_ = min_, max_
        object.__setattr__(self, "min_", min_)
        object.__setattr__(self, "max_", max_)

    @property
    @functools.lru_cache(maxsize=1)
    def max_distance(self) -> float:
        return self.max_ - self.min_

    @functools.lru_cache(maxsize=1)
    def get_interpolation_if_more(self):
        return _interpolations[self.interpolation_if_more]

    @functools.lru_cache(maxsize=1)
    def get_interpolation_if_less(self):
        return _interpolations[self.interpolation_if_less]


def numeric_evalator(options: NumericEvaluationOptions, query: float, case: float) -> float:
    distance = _calculate_distance(query, case, options.max_distance, options.cyclic)
    max_distance = _calculate_max_distance(query, options.max_distance, options.origin, options.use_origin)
    if max_distance == 0:
        return 1
    relative_distance = distance / max_distance
    if relative_distance < 1:
        if _is_less(case, query, options.max_distance, options.cyclic):
            equal = options.equal_if_less
            tolerance = options.tolerance_if_less
            linearity = options.linearity_if_less
            interpolation = options.get_interpolation_if_less()
        else:
            equal = options.equal_if_more
            tolerance = options.tolerance_if_more
            linearity = options.linearity_if_more
            interpolation = options.get_interpolation_if_more()
        if relative_distance <= equal:
            return 1
        elif relative_distance >= tolerance:
            return 0
        else:
            stretched_distance = (relative_distance - equal) / (tolerance - equal)
            return interpolation(stretched_distance, linearity)
    return 0


def total_order_evaluator(ordering: list[str], evaluator: Evaluator, query: str, case: str) -> float:
    query_index = ordering.index(query)
    case_index = ordering.index(case)
    return evaluator(query_index, case_index)


def equality_evaluator(query: Any, case: Any) -> float:
    if query is None or case is None or query != case:
        return 0
    return 1
