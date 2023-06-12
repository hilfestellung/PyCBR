import dataclasses
from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

from cbrlib.evaluators import Evaluator

C = TypeVar("C")


@dataclass(slots=True, frozen=True)
class ReasoningRequest(Generic[C]):
    query: C

    offset: int = dataclasses.field(default=0)
    limit: int = dataclasses.field(default=10)

    threshold: float = dataclasses.field(default=0.1)


@dataclass(slots=True, frozen=True)
class Result(Generic[C]):
    similarity: float
    case: C


@dataclass(slots=True, frozen=True)
class ReasoningResponse(Generic[C]):
    total_number_of_hits: int
    hits: list[Result]


def infer(casebase: Iterable[C], request: ReasoningRequest[C], evaluator: Evaluator) -> ReasoningResponse[C]:
    threshold = request.threshold
    calculations = [
        r
        for r in sorted(
            map(lambda c: Result(evaluator(request.query, c), c), casebase),
            key=lambda r: r.similarity,
            reverse=True,
        )
        if r.similarity >= threshold
    ]

    offset = request.offset
    limit = request.limit
    return ReasoningResponse(
        total_number_of_hits=len(calculations),
        hits=calculations[offset:offset + limit],  # fmt: skip
    )
