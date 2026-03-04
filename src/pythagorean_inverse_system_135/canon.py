from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Set, Tuple

Symbol = int
Bigram = Tuple[Symbol, Symbol]


@dataclass(frozen=True)
class CanonConstraints:
    symbols: Tuple[Symbol, ...] = (1, 3, 5)
    cyclic: bool = True  # per noi sempre True
    # Vincolo orizzontale: non ripetere bigrammi nel ciclo
    unique_bigrams: bool = True
    # Vincolo verticale: vieta la co-occorrenza 11 e 55 nello stesso slice
    forbid_11_and_55_same_slice: bool = True
    # Opzionale: nello slice tutte le coppie devono essere diverse
    slice_unique_bigrams: bool = False


def cyclic_bigrams(seq: Sequence[Symbol]) -> List[Bigram]:
    """Return the list of cyclic bigrams for seq (includes last->first)."""
    L = len(seq)
    return [(seq[i], seq[(i + 1) % L]) for i in range(L)]


def has_unique_cyclic_bigrams(seq: Sequence[Symbol]) -> bool:
    bgs = cyclic_bigrams(seq)
    return len(set(bgs)) == len(bgs)


def slice_bigrams(seq: Sequence[Symbol], n_voices: int, d: int = 1) -> List[List[Bigram]]:
    """
    For each time index i (bigram index), compute the list of bigrams heard by each voice:
      voice k uses bigram at index (i - k*d) mod L
    where L = len(seq) = number of cyclic bigrams.
    """
    if n_voices < 1:
        raise ValueError("n_voices must be >= 1")
    if d < 1:
        raise ValueError("d must be >= 1")

    L = len(seq)
    bgs = cyclic_bigrams(seq)
    slices: List[List[Bigram]] = []
    for i in range(L):
        current: List[Bigram] = []
        for k in range(n_voices):
            idx = (i - k * d) % L
            current.append(bgs[idx])
        slices.append(current)
    return slices


def violates_vertical_11_55(seq: Sequence[Symbol], n_voices: int, d: int = 1) -> bool:
    """
    Returns True if there exists a slice containing both (1,1) and (5,5).
    """
    for sl in slice_bigrams(seq, n_voices=n_voices, d=d):
        s = set(sl)
        if (1, 1) in s and (5, 5) in s:
            return True
    return False


def violates_slice_uniqueness(seq: Sequence[Symbol], n_voices: int, d: int = 1) -> bool:
    """
    Returns True if there exists a slice where any bigram repeats (i.e., not all distinct).
    """
    for sl in slice_bigrams(seq, n_voices=n_voices, d=d):
        if len(set(sl)) != len(sl):
            return True
    return False


def is_valid_seed(seq: Sequence[Symbol], n_voices: int, d: int, cons: CanonConstraints) -> bool:
    if cons.cyclic is False:
        raise ValueError("This project assumes cyclic=True (infinite canon core).")

    # A) vincolo orizzontale
    if cons.unique_bigrams and not has_unique_cyclic_bigrams(seq):
        return False

    # B) vincoli verticali
    if cons.forbid_11_and_55_same_slice:
        if violates_vertical_11_55(seq, n_voices=n_voices, d=d):
            return False

    if cons.slice_unique_bigrams:
        if violates_slice_uniqueness(seq, n_voices=n_voices, d=d):
            return False

    return True


def find_one_seed(
    length: int,
    n_voices: int,
    d: int = 1,
    cons: Optional[CanonConstraints] = None,
) -> Optional[List[Symbol]]:
    """
    Find one cyclic sequence of given length over cons.symbols such that:
      - cyclic bigrams are unique (if enabled)
      - vertical constraints hold (if enabled)
    Returns the first found seed as a list, or None.
    """
    cons = cons or CanonConstraints()
    symbols = cons.symbols
    L = length

    # Limite duro: non puoi avere più bigrammi ciclici distinti di |A|^2
    max_bigrams = len(symbols) * len(symbols)
    if cons.unique_bigrams and L > max_bigrams:
        return None

    # Backtracking costruendo la sequenza, garantendo unicità dei bigrammi incrementale
    used: Set[Bigram] = set()
    seq: List[Symbol] = []

    def rec(pos: int) -> bool:
        if pos == L:
            # chiusura ciclo: aggiunge last->first come bigramma
            closing = (seq[-1], seq[0])
            if cons.unique_bigrams:
                if closing in used:
                    return False
                # non aggiungiamo permanentemente; basta testare
            # Test verticale finale
            return is_valid_seed(seq, n_voices=n_voices, d=d, cons=cons)

        for s in symbols:
            if pos == 0:
                seq.append(s)
                if rec(pos + 1):
                    return True
                seq.pop()
            else:
                bg = (seq[-1], s)
                if cons.unique_bigrams and bg in used:
                    continue
                seq.append(s)
                if cons.unique_bigrams:
                    used.add(bg)

                # pruning leggero: se vuoi, puoi mettere check verticali parziali,
                # ma per ora teniamolo semplice e corretto.

                if rec(pos + 1):
                    return True

                if cons.unique_bigrams:
                    used.remove(bg)
                seq.pop()
        return False

    ok = rec(0)
    return seq if ok else None