import argparse

from pythagorean_inverse_system_135.canon import CanonConstraints, is_valid_seed


def iter_seeds(length: int, symbols=(1, 3, 5)):
    """Generate all sequences of given length over symbols (brute force)."""
    # Iterazione iterativa (senza recursion profonda)
    idx = [0] * length
    A = len(symbols)
    while True:
        yield [symbols[i] for i in idx]

        # increment in base A
        pos = length - 1
        while pos >= 0:
            idx[pos] += 1
            if idx[pos] < A:
                break
            idx[pos] = 0
            pos -= 1
        if pos < 0:
            return


def main():
    ap = argparse.ArgumentParser(
        description="List all valid cyclic seeds for a given number of voices (convention: length = voices)."
    )
    ap.add_argument("--voices", type=int, required=True, help="Number of voices (e.g., 2..8).")
    ap.add_argument("--d", type=int, default=1, help="Canon distance d (default: 1).")
    ap.add_argument("--limit", type=int, default=0, help="Stop after printing this many seeds (0 = no limit).")
    ap.add_argument("--quiet", action="store_true", help="Print only the total count.")
    args = ap.parse_args()

    n_voices = args.voices
    if n_voices < 1:
        raise SystemExit("ERROR: --voices must be >= 1")
    if n_voices >= 9:
        raise SystemExit("ERROR: voices >= 9 are structurally impossible here (vertical slices will force both 11 and 55). Use 1..8.")

    length = n_voices  # project convention

    # NOTE: 11 and 55 are not forbidden in the seed by themselves.
    # The only vertical prohibition enforced here is: never have (1,1) and (5,5) in the same slice.
    cons = CanonConstraints(
        symbols=(1, 3, 5),
        cyclic=True,
        unique_bigrams=True,
        forbid_11_and_55_same_slice=True,
        slice_unique_bigrams=False,
    )

    count = 0
    printed = 0

    for seq in iter_seeds(length=length, symbols=cons.symbols):
        if is_valid_seed(seq, n_voices=n_voices, d=args.d, cons=cons):
            count += 1
            if not args.quiet:
                print("".join(str(x) for x in seq))
                printed += 1
                if args.limit and printed >= args.limit:
                    break

    if args.quiet:
        print(count)


if __name__ == "__main__":
    main()