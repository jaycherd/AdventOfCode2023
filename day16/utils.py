from typing import List





def generate_matrix[T](f_name: str) -> List[List[T]]:
    mat : List[List[T]] = []
    try:
        with open(f_name,'r')as file:
            for line in (list(line.strip()) for line in file):
                mat.append(line)
    except FileNotFoundError:
        print(f"file {f_name} not found")
    return mat