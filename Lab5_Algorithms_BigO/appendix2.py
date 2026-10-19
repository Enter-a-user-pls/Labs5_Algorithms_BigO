# UNIVERSITY ENROLLMENT RECORDS

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
        "ARTIST_SUM": sum(ord(c) - 64 for c in artist_letters),
    }


# ---------- Data generation ----------
SIZE = 6  # records per department


def generate_data(s):
    # Dataset A: starts at ID_SUM, increases by SEED_DIGIT + 1
    a = [s["ID_SUM"] + i * (s["SEED_DIGIT"] + 1) for i in range(SIZE)]
    # Dataset B: starts at NAME_LENGTH, increases by ARTIST_LENGTH
    b = [s["NAME_LENGTH"] + i * s["ARTIST_LENGTH"] for i in range(SIZE)]
    return a, b


# ---------- Merge ----------
def merge_sorted(a, b):
    """Returns (merged, comparisons). One comparison = a[i] vs b[j]."""
    merged, i, j, comps = [], 0, 0, 0
    while i < len(a) and j < len(b):
        comps += 1
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged, comps


def is_ordered(lst):
    return all(lst[k] <= lst[k + 1] for k in range(len(lst) - 1))


# ---------- Main ----------
def main():
    s = get_student_inputs()
    a, b = generate_data(s)
    merged, comps = merge_sorted(a, b)

    ok = is_ordered(merged) and len(merged) == len(a) + len(b) \
        and sorted(a + b) == merged

    print("\n=== STUDENT-SPECIFIC INPUTS ===")
    print(f"LAST_NAME={s['LAST_NAME']}  STUDENT_ID={s['STUDENT_ID']}  "
          f"FAVORITE_ARTIST={s['FAVORITE_ARTIST']}")
    print(f"SEED_DIGIT={s['SEED_DIGIT']}  ID_SUM={s['ID_SUM']}  "
          f"NAME_LENGTH={s['NAME_LENGTH']}  ARTIST_LENGTH={s['ARTIST_LENGTH']}  "
          f"ARTIST_SUM={s['ARTIST_SUM']}")

    print("\n=== ASSESSMENT DATA ===")
    print(f"Department A dataset: {a}")
    print(f"Department B dataset: {b}")
    print(f"Consolidated dataset: {merged}")
    print(f"Number of records before and after consolidation: "
          f"{len(a)} + {len(b)} = {len(a) + len(b)} -> {len(merged)}")
    print(f"Comparison count: {comps}")
    print(f"Ordering verification: {'PASSED (ascending, no records lost)' if ok else 'FAILED'}")
    print("Time and space complexity: Time O(m+n); Space O(m+n)")
    print(f"Final Output: {len(merged)} records consolidated in {comps} comparisons")


if __name__ == "__main__":
    main()
