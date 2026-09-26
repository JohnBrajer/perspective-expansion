"""Reference implementation for John Brajer's Perspective Expansion framework.

The framework separates action-space expansion from action evaluation:
1. classify constraints,
2. preserve hard constraints,
3. challenge assumptions,
4. generate newly visible actions,
5. evaluate only after expansion.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, Sequence


class ConstraintKind(str, Enum):
    HARD = "hard"
    ASSUMED = "assumed"


@dataclass(frozen=True)
class Constraint:
    name: str
    kind: ConstraintKind
    rationale: str = ""


def perspective_expansion(
    constraints: Sequence[Constraint],
    baseline_actions: Sequence[str],
    generator: Callable[[Sequence[Constraint]], Iterable[str]],
) -> list[str]:
    """Return the expanded action set while preserving hard constraints."""
    hard = [c for c in constraints if c.kind is ConstraintKind.HARD]
    return list(dict.fromkeys([*baseline_actions, *generator(hard)]))


if __name__ == "__main__":
    constraints = [
        Constraint("budget <= 100", ConstraintKind.HARD),
        Constraint("must use the usual vendor", ConstraintKind.ASSUMED),
    ]
    print(perspective_expansion(
        constraints,
        ["buy from the usual vendor"],
        lambda hard: ["rent", "borrow", "buy used"],
    ))
