import numpy as np
from icecream import ic
DEFAULT_FILENAME = "input.txt"
def read_chars(filename = DEFAULT_FILENAME):
    res = []
    res.append([])
    with open(filename, "r") as f:
        for li in f:
            if li.strip() == "":
                res.append([])
            else:
                res[-1].append(np.array([*li.strip()]))
    return res
def solve(mat):
  count1 = 0
  count2 = 0
  pairs = np.zeros(mat.shape[0], dtype=int)
  errors = np.zeros(mat.shape[0], dtype=int)
  for i in range(mat.shape[0]):
    for j in range(i+1, mat.shape[0], 2):
      num_matches = np.sum(mat[i] == mat[j])
      if num_matches >= (mat.shape[1] - 1):
        rows_before = (i + j + 1) // 2
        pairs[rows_before] += 1
        errors[rows_before] += mat.shape[1] - num_matches
  for ind, hit in enumerate(pairs):
    target = min(ind, mat.shape[0] - ind)
    if target > 0 and hit == target and errors[ind] == 0:
      count1 += ind
    if target > 0 and hit == target and errors[ind] == 1:
      count2 += ind
  return count1, count2

sol1 = 0
sol2 = 0
values = [np.array(a) for a in read_chars()]
for mat in values:
  count1, count2 = solve(mat)
  sol1 += 100 * count1
  sol2 += 100 * count2
  mat = mat.transpose((1, 0))
  count1, count2 = solve(mat)
  sol1 += count1
  sol2 += count2
print(f"Part 1: {sol1}")
print(f"Part 2: {sol2}")