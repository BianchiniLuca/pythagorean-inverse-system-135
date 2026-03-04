from __future__ import annotations

from typing import Iterable, Optional, Sequence, Set, Tuple

Bigram = Tuple[int, int]


def iter_bigrams(seq: Sequence[int], cyclic: bool) -> Iterable[Bigram]:
    """Yield adjacent bigrams. If cyclic=True, include last->first."""
    if len(seq) < 2:
        return
    for i in range(len(seq) - 1):
        yield (seq[i], seq[i + 1])
    if cyclic and len(seq) >= 2:
        yield (seq[-1], seq[0])


def has_repeated_bigrams(seq: Sequence[int], cyclic: bool) -> bool:
    seen: Set[Bigram] = set()
    for bg in iter_bigrams(seq, cyclic=cyclic):
        if bg in seen:
            return True
        seen.add(bg)
    return False


def violates_forbidden_bigrams(
    seq: Sequence[int],
    forbidden: Optional[Set[Bigram]],
    cyclic: bool,
) -> bool:
    if not forbidden:
        return False
    for bg in iter_bigrams(seq, cyclic=cyclic):
        if bg in forbidden:
            return True
    return False