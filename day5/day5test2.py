from typing import List, Tuple

def merge_intervals(intervalsA: List[Tuple[int, int, int]], intervalsB: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Merge two lists of intervals. Only overlapping intervals are considered.
    If an interval in intervalsB overlaps with intervalsA, it takes priority.
    Parts of intervalsB that do not overlap with any interval in intervalsA are dropped.
    """
    result = []

    for a_start, a_end, a_diff in intervalsA:
        a_index = a_start
        while a_index <= a_end:
            overlap_found = False
            for b_start, b_end, b_diff in intervalsB:
                if b_start <= a_index <= b_end:
                    # Overlap found, use intervalsB's diff
                    overlap_end = min(b_end, a_end)
                    result.append((a_index, overlap_end, b_diff))
                    a_index = overlap_end + 1
                    overlap_found = True
                    break
            
            if not overlap_found:
                # No overlap, use intervalsA's diff
                next_b_start = min([b_start for b_start, _, _ in intervalsB if b_start > a_index], default=a_end + 1)
                result.append((a_index, min(a_end, next_b_start - 1), a_diff))
                a_index = next_b_start

    return sorted(result, key=lambda x: x[0])

# Example usage
intervalsA = [(1, 12, 0), (15, 20, 0)]
intervalsB = [(5, 8, 12), (21, 22, 13)]
intervalsMerged = merge_intervals(intervalsA, intervalsB)
print(intervalsMerged)
