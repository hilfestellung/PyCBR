import dataclasses
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

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


class Casebase(Generic[C]):
    def __init__(self, case_type: Type[C]) -> None:
        self._case_type = case_type
        self._cases: set[C] = set()
        self._field_names = [desc.name for desc in dataclasses.fields(case_type)]

    def add_case(self, case: C) -> None:
        if case is None:
            return
        if not isinstance(case, self._case_type):
            raise ValueError(f"A case object must be of type {self._case_type}.")
        self._cases.add(case)

    def remove_case(self, case: C) -> None:
        if case is None:
            return
        self._cases.remove(case)

    def infer(self, request: ReasoningRequest[C], evaluator: Evaluator) -> ReasoningResponse[C]:
        offset = request.offset
        threshold = request.threshold
        limit = request.limit
        calculations = [
            r
            for r in sorted(
                map(lambda c: Result(evaluator(request.query, c), c), self._cases),
                key=lambda r: r.similarity,
                reverse=True,
            )
            if r.similarity >= threshold
        ]
        return ReasoningResponse(
            total_number_of_hits=len(calculations),
            hits=calculations[offset:offset + limit],  # fmt: skip
        )
