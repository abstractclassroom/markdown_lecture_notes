#create identity matrix



def swap_permutation(matrix, swap_perm):
    n = len(matrix)
    new_matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            new_matrix[i][j] = matrix[i][swap_perm[j]-1]
    return new_matrix

def print_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        print(matrix[i])

def matrix_mult(a,b):
    n = len(a)
    return [[sum([a[i][k]*b[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]

def check_if_identity(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 1 if i == j else 0:
                return False
    return True

def transpose(matrix):
    n = len(matrix)
    return [[matrix[j][i] for j in range(n)] for i in range(n)]

def check_if_matrix_equal(a,b):
    n = len(a)
    for i in range(n):
        for j in range(n):
            if a[i][j] != b[i][j]:
                return False
    return True

def print_nonzero_elements(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                print("Element at position ({},{}) is {}".format(i,j,matrix[i][j]))

identity =  [[1 if i == j else 0 for j in range(64)] for i in range(64)]

swap_perm_ip = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

swap_perm_fp = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

initial_permutation = swap_permutation(identity, swap_perm_ip)
final_permutation = swap_permutation(identity, swap_perm_fp)

print_matrix(initial_permutation)

print("Check if identity :",check_if_identity(matrix_mult(initial_permutation, final_permutation)))

print("Same Matrix? : ",check_if_matrix_equal(initial_permutation, transpose(final_permutation)))

print_nonzero_elements(initial_permutation)