from __future__ import annotations
import numpy as np
from functools import partial
from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator

def generate_np_matrix(f_name: str) -> Generator[List[List[str]],None,None]:
    try:
        mat = []
        with open(f_name,'r') as file:
            for line in (list(line.strip()) for line in file):
                if line:
                    mat.append(line)
                else:
                    yield np.array(mat,dtype=str)
                    mat = []
            if mat:
                yield np.array(mat,dtype=str)
    except FileNotFoundError:
        print(f"file {f_name} not found")

def is_reflection[T](imga: np.array[T,T], imgb: np.ndarray[T,T]) -> bool:
    return (imga==imgb).all()

string_diff = lambda a, b: sum(i != j for (i, j) in zip(a, b))

def is_symmetrical(arr: List[List[int]]):
	if len(arr) <= 1:
		return False
	for i in range(len(arr)//2):
		if arr[i] != arr[-i-1]:
			return False
	return True

def transposeArray(arr):
	return list(map(list, zip(*arr)))


def find_mirror(mat: List[List[str]]) -> int:
    for i in range(2):
        for row_num in range(len(mat)):
            if (row_num + 1) * 2 < len(mat):
                tmp = is_symmetrical(mat[:(row_num+1)*2])
            else:
                tmp = is_symmetrical(mat[-((len(mat)-1)-row_num)*2:])
            if tmp:
                 if i==1:
                      return row_num + 1
                 if i ==0:
                      return (row_num + 1)*100
        mat = transposeArray(mat) #now for the cols

def solve(mat: List[List[int]]) -> Tuple[int,int]:
    count = 0
    """shape specifies dimensions of array,
    dtype specs the dtype of elements in array
    note: mat.shape for a 2d np array is a tuple (num_rows, num_cols)"""
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
    return (count1, count2)

def part1(f_name: str) -> None:
    res1,res2 = 0,0
    for mat in generate_np_matrix(f_name=f_name):
        tmp1,tmp2 = solve(mat)
        res1 += tmp1*row_multiplier
        res2 += tmp2*row_multiplier
        mat = mat.transpose((1,0))
        tmp1,tmp2 = solve(mat)
        res1 += tmp1
        res2 += tmp2
    ic(res1,res2)
    # for mat in generate_matrix(f_name):
    




if __name__ == "__main__":
    row_multiplier = 100
    f_name1 = "test.txt"
    f_name2 = "input.txt"
    part1(f_name=f_name1)
    part1(f_name=f_name2)