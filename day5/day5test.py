from typing import List, Tuple
from icecream import ic


def merge_intervals(intervalsA: List[Tuple[int, int, int]], intervalsB: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Merge two lists of intervals. Intervals from intervalsB have priority over intervalsA in case of overlap.
    Inclusive intervals are considered.
    """
    result = []
    usedB = [False] * len(intervalsB)

    for a_start, a_end, a_diff in intervalsA:
        a_index = a_start
        while a_index <= a_end:
            overlap = False
            for i, (b_start, b_end, b_diff) in enumerate(intervalsB):
                if b_start <= a_index <= b_end:
                    # Overlap found, use intervalsB's diff
                    if not usedB[i]:
                        result.append((max(a_index, b_start), b_end, b_diff))
                        usedB[i] = True
                    overlap = True
                    a_index = b_end + 1
                    break
            
            if not overlap:
                # No overlap, use intervalsA's diff
                next_b_start = min([b_start for b_start, _, _ in intervalsB if b_start > a_index], default=a_end + 1)
                result.append((a_index, min(a_end, next_b_start - 1), a_diff))
                a_index = next_b_start

    # Add remaining intervalsB that have not been used
    for i, (b_start, b_end, b_diff) in enumerate(intervalsB):
        if not usedB[i]:
            result.append((b_start, b_end, b_diff))

    return sorted(result, key=lambda x: x[0])

# Example usage
intervalsA = [(1, 12, 0), (15, 20, 0)]
intervalsB = [(5, 8, 12), (21, 22, 13)]
intervalsMerged = merge_intervals(intervalsA, intervalsB)
print(intervalsMerged)

