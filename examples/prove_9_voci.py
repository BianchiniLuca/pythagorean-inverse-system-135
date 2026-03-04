from pythagorean_inverse_system_135.canon import CanonConstraints, find_one_seed


def main() -> None:
    n_voices = 9
    d = 1

    # Convenzione del progetto: L = number of voices
    length = n_voices

    cons = CanonConstraints(
        symbols=(1, 3, 5),
        cyclic=True,
        unique_bigrams=True,
        forbid_11_and_55_same_slice=True,
        slice_unique_bigrams=False,
    )

    seed = find_one_seed(length=length, n_voices=n_voices, d=d, cons=cons)

    print(f"n_voices={n_voices}, d={d}, length={length}")
    if seed is None:
        print("RESULT: IMPOSSIBLE (no valid seed exists under the constraints).")
    else:
        print("RESULT: FOUND A SEED (this would contradict the claimed limit).")
        print("seed:", seed)


if __name__ == "__main__":
    main()