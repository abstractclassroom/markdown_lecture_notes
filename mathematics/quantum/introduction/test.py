import cmath as cm

a0 = [
    [1,0],
    [0,1]
]

a1 = [
    [0,-1],
    [1,0]
]

a2 = [
    [-1,0],
    [0,-1]
]

a3 = [
    [0,1],
    [-1,0]
]

a4 = [
    [1,0],
    [0,-1]
]

a5 = [
    [0,1],
    [1,0]
]

a6 = [
    [-1,0],
    [0,1]
]

a7 = [
    [0,-1],
    [-1,0]
]

mats = [a0,a1,a2,a3,a4,a5,a6,a7]

def matrix_mult(a,b):
    return [[sum([a[i][k]*b[k][j] for k in range(2)]) for j in range(2)] for i in range(2)]

for i in range(8):
    for j in range(8):
        result = matrix_mult(mats[i],mats[j])
        #determine which matrix is the result of the multiplication of a_i and a_j
        for k in range(8):
            if result == mats[k]:
                print("a{} * a{} = a{}".format(i,j,k))
                break
    print("\n\n\n")


