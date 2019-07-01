import numpy as np
import core.solver as solver 
import core.state as state 

def matmult(n):
    transformA = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    transformB = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))

    result = []
    for i in range(n):
        row = []
        for j in range(n):
            a_row = transformA[i,:]
            b_row = transformB[:, j]
            row.append(np.dot(a_row, b_row))
        result.append(row)

def matmultTogether(n):
    transformA = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    transformB = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            a_row = transformA[i,:]
            b_row = transformB[:, j]
            vals = np.multiply(a_row, b_row)
            row.append(solver.genop(vals, np.sum))
        result.append(row)

def strassen_matmult(N):
    n = 2**N
    transformA = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    transformB = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    strassen_helper(transformA, transformB)

def strassen_helper(A,B):
    N = A.shape[0]
    assert (A.shape[0] == B.shape[0])
    assert N%2 == 0 or N==1
    if N == 1:
        return A[0,0] * B[0,0]
    n = int(N/2)
    def splitmat(X):
        return [[X[:n, :n], X[n:, :n]], [X[:n, n:], X[n:, n:]]]
    A_mats = splitmat(A)
    B_mats = splitmat(B)
    M1 = strassen_helper(A_mats[0][0] + A_mats[1][1], B_mats[0][0] + B_mats[1][1])
    M2 = strassen_helper(A_mats[1][0] + A_mats[1][1], B_mats[0][0])
    M3 = strassen_helper(A_mats[0][0], B_mats[0][1] - B_mats[1][1])
    M4 = strassen_helper(A_mats[1][1], B_mats[1][0] - B_mats[0][0])
    M5 = strassen_helper(A_mats[0][0] + A_mats[0][1], B_mats[1][1])
    M6 = strassen_helper(A_mats[1][0] - A_mats[0][0], B_mats[0][0] + B_mats[0][1])
    M7 = strassen_helper(A_mats[0][1] - A_mats[1][1], B_mats[1][0] + B_mats[1][1])

    C11 = ((M1 + M4) - M5) + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = ((M1 - M2) + M3) + M6
    return np.array([[C11, C12], [C21, C22]])
