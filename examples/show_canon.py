import argparse


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Print canon voices with delayed entry (initial silence only), then the SAME continuous seed (no internal rests)."
    )
    ap.add_argument("--seed", required=True, help="Seed as digits, e.g. 11315335")
    ap.add_argument("--voices", type=int, required=True, help="Number of voices (e.g. 8)")
    ap.add_argument("--d", type=int, default=1, help="Canon distance d (default: 1)")
    ap.add_argument("--cycles", type=int, default=6, help="How many seed cycles to print (default: 6)")
    ap.add_argument("--pad", default="-", help="Char for not-yet-entered time (default: '-')")
    args = ap.parse_args()

    seed = args.seed.strip()
    if not seed.isdigit():
        raise SystemExit("ERROR: --seed must be digits only, e.g. 11315335")

    n = args.voices
    d = args.d
    cycles = args.cycles

    if n < 1:
        raise SystemExit("ERROR: --voices must be >= 1")
    if d < 1:
        raise SystemExit("ERROR: --d must be >= 1")
    if cycles < 1:
        raise SystemExit("ERROR: --cycles must be >= 1")

    line = seed * cycles  # continuous, no spaces

    for k in range(n):
        delay = k * d
        prefix = args.pad * delay
        print(f"V{k+1}: {prefix}{line}")


if __name__ == "__main__":
    main()