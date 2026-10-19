# EMERGENCY DISPATCH RECORD SEARCH

from Student_Specific_Inputs import *


def get_student_inputs():
    last_name = LAST_NAME.strip()
    student_id = STUDENT_ID.strip()
    artist = FAVORITE_ARTIST.strip()

    digits = [int(c) for c in student_id if c.isdigit()]
    name_letters = [c for c in last_name.upper() if c.isalpha()]
    artist_letters = [c for c in artist.upper() if c.isalpha()]
    if not digits or not name_letters or not artist_letters:
        raise SystemExit("Invalid values: STUDENT_ID needs digits; names need letters.")

    return {
        "LAST_NAME": last_name,
        "STUDENT_ID": student_id,
        "FAVORITE_ARTIST": artist,
        "SEED_DIGIT": digits[-1],
        "ID_SUM": sum(digits),
        "NAME_LENGTH": len(name_letters),
        "ARTIST_LENGTH": len(artist_letters),
        "ARTIST_SUM": sum(ord(c) - 64 for c in artist_letters),  # A=1 .. Z=26
    }


# ---------- Data generation ----------
N = 10  # number of incident records


def generate_data(s):
    base = 1000 + s["ID_SUM"]
    step = s["NAME_LENGTH"] + s["ARTIST_LENGTH"]          # >= 2, so values are unique
    original = [base + i * step for i in range(N)]        # numerical order

    rot = max(1, s["SEED_DIGIT"])                          # rotation point (0 -> 1)
    rotated = original[rot:] + original[:rot]              # front moved to the end

    k = (s["ID_SUM"] + s["ARTIST_SUM"]) % (N + 1)          # k == N -> not in list
    target = base + k * step
    return original, rotated, rot, target


# ---------- Searches ----------
def rotated_binary_search(arr, target):
    """Returns (index, comparisons). One comparison = one probe of arr[mid]."""
    lo, hi, comps = 0, len(arr) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if arr[mid] == target:
            return mid, comps
        if arr[lo] <= arr[mid]:                            # left half is sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                              # right half is sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1, comps


def linear_search(arr, target):
    """Returns (index, comparisons). One comparison = one element checked."""
    comps = 0
    for i, v in enumerate(arr):
        comps += 1
        if v == target:
            return i, comps
    return -1, comps


# ---------- Main ----------
def main():
    s = get_student_inputs()
    original, rotated, rot, target = generate_data(s)

    b_idx, b_comps = rotated_binary_search(rotated, target)
    l_idx, l_comps = linear_search(rotated, target)

    print("\n=== STUDENT-SPECIFIC INPUTS ===")
    print(f"LAST_NAME={s['LAST_NAME']}  STUDENT_ID={s['STUDENT_ID']}  "
          f"FAVORITE_ARTIST={s['FAVORITE_ARTIST']}")
    print(f"SEED_DIGIT={s['SEED_DIGIT']}  ID_SUM={s['ID_SUM']}  "
          f"NAME_LENGTH={s['NAME_LENGTH']}  ARTIST_LENGTH={s['ARTIST_LENGTH']}  "
          f"ARTIST_SUM={s['ARTIST_SUM']}")

    print(f"Rotation point: first {rot} record(s) moved to the end of the list")

    print("\n=== ASSESSMENT DATA ===")
    print(f"Original Dataset: {original}")
    print(f"Rotated Dataset: {rotated}")
    print(f"Target Incident: {target}")
    if b_idx == -1:
        print("Position: NOT FOUND in rotated list")
    else:
        print(f"Position: index {b_idx} in rotated list (original index {(b_idx + rot) % N})")
    print(f"Comparison Counts: Binary={b_comps}")
    print(f"Linear Search comparison count: {l_comps}")
    print("Time and space complexity: Binary O(log n)/O(1); Linear O(n)/O(1)")
    result = f"found at index {b_idx}" if b_idx != -1 else "not found"
    print(f"Final Output: Incident {target} {result} "
          f"(Binary={b_comps}, Linear={l_comps} comparisons)")


if __name__ == "__main__":
    main()
