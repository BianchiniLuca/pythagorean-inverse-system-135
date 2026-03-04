from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

from .validators import Bigram

Symbol = int


@dataclass(frozen=True)
class SeedConstraints:
    symbols: Tuple[Symbol, ...] = (1, 3, 5)
    cyclic: bool = True
    forbidden_bigrams: Optional[Set[Bigram]] = None


def count_seeds(length: int, constraints: SeedConstraints) -> int:
    """
    Count admissible cyclic seeds of a given length over constraints.symbols.

    Constraints:
      - no repeated adjacent bigrams (cyclic, i.e., last->first included)
      - optional forbidden bigrams (e.g., {(1,1), (5,5)} if you want)
    """
    L = length
    if L < 1:
        raise ValueError("length must be >= 1")

    symbols = constraints.symbols
    cyclic = constraints.cyclic
    forbidden = constraints.forbidden_bigrams or set()

    if L == 1:
        return len(symbols)

    used: Set[Bigram] = set()
    seq: List[Symbol] = []

    def rec(pos: int) -> int:
        if pos == L:
            if cyclic:
                closing = (seq[-1], seq[0])
                if closing in forbidden or closing in used:
                    return 0
            return 1

        total = 0
        for s in symbols:
            if pos == 0:
                seq.append(s)
                total += rec(pos + 1)
                seq.pop()
            else:
                bg = (seq[-1], s)
                if bg in forbidden or bg in used:
                    continue
                seq.append(s)
                used.add(bg)
                total += rec(pos + 1)
                used.remove(bg)
                seq.pop()
        return total

    return rec(0)


def count_until_extinction(
    constraints: SeedConstraints,
    L_min: int = 1,
    L_max: int = 64,
) -> Tuple[Dict[int, int], Optional[int]]:
    counts: Dict[int, int] = {}
    extinction_L: Optional[int] = None

    for L in range(L_min, L_max + 1):
        c = count_seeds(L, constraints)
        counts[L] = c
        if c == 0:
            extinction_L = L
            break

    return counts, extinction_L