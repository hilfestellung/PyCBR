import csv
import dataclasses
import functools
import json
import sys
import time
from dataclasses import dataclass
from typing import Any, Iterable, Iterator

from cbrlib import casebase, evaluators
from cbrlib.casebase import ReasoningRequest
from cbrlib.evaluators import (
    Evaluator,
    NumericEvaluationOptions,
    WeightedPropertyEvaluatorMapping, FunctionCalculationParameter,
)

whiskey_colours = [
    "straw",  # "Stroh",
    "pale-straw",  # "blass-strohig",
    "pale-gold",  # "blass-gold",
    "peat",  # "Torf",
    "dark-amber",  # "dunkel-amber",
    "deep-amber",  # "tief-bernstein",
    "full-amber",  # "voll-bernstein",
    "honey",  # "Honig"
    "gold",  # "gold",
    "amber",  # "bernsteinfarben",
    "mid-amber",  # "mittel-bernstein",
    "pale-amber",  # "blass-bernsteinfarben",
    "light-amber",  # "hell-bernstein",
    "rich",  # "reich",
    "deep",  # "tief",
    "dark",  # "dunkel",
    "medium",  # "mittel",
    "full",  # "voll",
    "warm",  # "warm",
    "light",  # "hell",
    "pale",  # "blass",
    "bright",  # "hell",
    "water",  # "Wasser",
    "haze",  # "Dunst",
]


@dataclass(slots=True, frozen=True)
class Whiskey:
    distillery: str = dataclasses.field(default=None)
    age: int = dataclasses.field(default=None)
    proof: float = dataclasses.field(default=None)
    sweetness: int = dataclasses.field(default=None)
    peatiness: int = dataclasses.field(default=None)
    availability: int = dataclasses.field(default=None)
    colour: str = dataclasses.field(default=None)
    nose: str = dataclasses.field(default=None)
    flavour_palette: str = dataclasses.field(default=None)
    finish: str = dataclasses.field(default=None)


def age_evaluator() -> Evaluator:
    options = NumericEvaluationOptions(min_=0, max_=100)
    return functools.partial(evaluators.numeric_evalator, options)


def rating_evaluator() -> Evaluator:
    options = NumericEvaluationOptions(min_=0, max_=10, if_less=FunctionCalculationParameter(tolerance=1.0),
                                       if_more=FunctionCalculationParameter(tolerance=1.0))
    return functools.partial(evaluators.numeric_evalator, options)


def whiskey_colour_evaluator() -> Evaluator:
    options = NumericEvaluationOptions(min_=0, max_=len(whiskey_colours) - 1)
    evaluator = functools.partial(evaluators.numeric_evalator, options)
    return functools.partial(evaluators.total_order_evaluator, whiskey_colours, evaluator)


def whiskey_evaluator() -> Evaluator:
    mappings = (
        WeightedPropertyEvaluatorMapping("distillery", 1, evaluators.equality_evaluator),
        WeightedPropertyEvaluatorMapping("age", 1, age_evaluator()),
        WeightedPropertyEvaluatorMapping("sweetness", 1, rating_evaluator()),
        WeightedPropertyEvaluatorMapping("peatiness", 1, rating_evaluator()),
        WeightedPropertyEvaluatorMapping("availability", 1, rating_evaluator()),
        WeightedPropertyEvaluatorMapping("colour", 1, whiskey_colour_evaluator()),
    )
    return functools.partial(evaluators.case_average_evaluator, mappings)


def raw_whiskeys() -> Iterator[dict[str, Any]]:
    with open("./data/Whiskey.csv", "r") as fd:
        csv_reader = csv.DictReader(fd, delimiter=";", lineterminator="\n")
        fields = dataclasses.fields(Whiskey)
        for r in csv_reader:
            # noinspection PyTypeChecker
            row: dict[str, str] = r
            for f in fields:
                if f.type != str:
                    row[f.name] = f.type(row[f.name])
            yield row


def load_whiskeys() -> Iterable[Whiskey]:
    result: list[Whiskey] = []
    for row in raw_whiskeys():
        whiskey = Whiskey(**row)
        result.append(whiskey)
    return result


def _serializer(obj: Any) -> Any:
    if isinstance(obj, set):
        return list(obj)
    elif dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    raise TypeError()


def _extract_values() -> None:
    values = {}
    for row in raw_whiskeys():
        for k, v in row.items():
            values.setdefault(k, set()).add(v)
    print(json.dumps(values, indent=2, default=_serializer))


def main() -> None:
    whiskeys = load_whiskeys()
    start = time.perf_counter()
    result = casebase.infer(
        whiskeys,
        ReasoningRequest(
            Whiskey(
                age=25,
                colour="peat",
                sweetness=10,
                peatiness=0,
            ),
            limit=5,
            threshold=0.4,
        ),
        whiskey_evaluator(),
    )
    runtime = time.perf_counter() - start
    # print(json.dumps(result, indent=2, default=_serializer))
    print(f"Reasoning took {(runtime * 1000):1.3}ms", file=sys.stderr)


if __name__ == "__main__":
    main()
    # _extract_values()
