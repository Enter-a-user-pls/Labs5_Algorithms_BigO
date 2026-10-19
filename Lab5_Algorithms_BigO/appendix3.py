# E-COMMERCE ORDER PROCESSING


from Student_Specific_Inputs import *
import random
import time




# ---------- Data generation ----------
N = 10  # number of orders


def generate_data(s):
    base = 1000 + s["ID_SUM"]
    step = s["NAME_LENGTH"] + s["SEED_DIGIT"] + 1
    orders = [base + i * step for i in range(N)]            # generated order numbers

    sorted_in = orders[:]
    reverse_in = orders[::-1]

    rng = random.Random(s["ARTIST_SUM"] * 1000 + s["ID_SUM"])  # reproducible
    random_in = orders[:]
    while random_in in (sorted_in, reverse_in):
        rng.shuffle(random_in)
    return orders, {"Sorted": sorted_in, "Reverse": reverse_in, "Random": random_in}


# ---------- Sorting algorithms: each returns (list, comparisons, movements) ----------
def bubble_sort(data):
    a, comps, moves = data[:], 0, 0
    for i in range(len(a) - 1):
        swapped = False
        for j in range(len(a) - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                moves += 1
                swapped = True
        if not swapped:                                     # early exit -> O(n) best case
            break
    return a, comps, moves


def selection_sort(data):
    a, comps, moves = data[:], 0, 0
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            moves += 1
    return a, comps, moves


def insertion_sort(data):
    a, comps, moves = data[:], 0, 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps, moves


ALGOS = {"Bubble": bubble_sort, "Selection": selection_sort, "Insertion": insertion_sort}
CONDS = ["Sorted", "Reverse", "Random"]


def avg_time_us(func, data, reps=2000):
    start = time.perf_counter()
    for _ in range(reps):
        func(data)
    return (time.perf_counter() - start) / reps * 1e6


# ---------- Main ----------
def main():
    s = get_student_inputs()
    orders, inputs = generate_data(s)

    res = {}  # (algo, cond) -> (sorted_list, comps, moves, time_us)
    for an, af in ALGOS.items():
        for cn in CONDS:
            out, c, m = af(inputs[cn])
            res[(an, cn)] = (out, c, m, avg_time_us(af, inputs[cn]))

    all_ok = all(r[0] == sorted(orders) for r in res.values())

    def row(idx, fmt="{}"):
        return " ".join(
            f"{an[:3]}=" + "/".join(fmt.format(res[(an, cn)][idx]) for cn in CONDS)
            for an in ALGOS)

    obs = []
    for an in ALGOS:
        ops = {cn: res[(an, cn)][1] + res[(an, cn)][2] for cn in CONDS}
        obs.append(f"{an[:3]}={min(ops, key=ops.get)[:3]}/{max(ops, key=ops.get)[:3]}")

    print("\n=== STUDENT-SPECIFIC INPUTS ===")
    print(f"LAST_NAME={s['LAST_NAME']}  STUDENT_ID={s['STUDENT_ID']}  "
          f"FAVORITE_ARTIST={s['FAVORITE_ARTIST']}")
    print(f"SEED_DIGIT={s['SEED_DIGIT']}  ID_SUM={s['ID_SUM']}  "
          f"NAME_LENGTH={s['NAME_LENGTH']}  ARTIST_LENGTH={s['ARTIST_LENGTH']}  "
          f"ARTIST_SUM={s['ARTIST_SUM']}")

    print("\n=== ASSESSMENT DATA (columns = Sorted/Reverse/Random) ===")
    print(f"Generated order dataset: {orders}")
    print(f"Sorted input: {inputs['Sorted']}")
    print(f"Reverse input: {inputs['Reverse']}")
    print(f"Random input: {inputs['Random']}")
    print(f"Comparison counts: {row(1)}")
    print(f"Movement counts: {row(2)}")
    print(f"Execution times (us): {row(3, '{:.1f}')}")
    print(f"Sorting verification: {'PASSED, all 9 runs correctly sorted' if all_ok else 'FAILED'}")
    print("Big O analysis: Bub O(n)-O(n^2); Sel O(n^2) always; Ins O(n)-O(n^2); Space O(1)")
    print(f"Best/worst case (Srt/Rev/Rnd): {' '.join(obs)}")
    print(f"Final Output: {res[('Insertion', 'Random')][0]}")


if __name__ == "__main__":
    main()
