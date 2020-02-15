import sys
sys.path.append('..')
import numpy as np
import core.solver as solver 
import core.state as state 

def matmult(n, alltogether=False):
    transformA = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    transformB = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))

    result = []
    for i in range(n):
        row = []
        for j in range(n):
            a_row = transformA[i,:]
            b_row = transformB[:, j]
            if alltogether:
                vals = np.multiply(a_row, b_row)
                row.append(solver.genop(vals, np.sum))
            else:
                row.append(np.dot(a_row, b_row))
        result.append(row)

def strassen_matmult(N, alltogether=False):
    n = 2**N
    transformA = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    transformB = np.array(solver.transform_array(list(range(n*n)))).reshape((n,n))
    strassen_helper(transformA, transformB, alltogether=alltogether)

def sum_matrices(mats_list):
    if isinstance(mats_list[0], np.ndarray):
        x, y = mats_list[0].shape
        results = np.array([[None for i in range(y)] for j in range(x)])
        for i in range(x):
            for j in range(y):
                results[i, j] = solver.genop([m[i, j] for m in mats_list], np.sum)
    else:
        results = solver.genop(mats_list, np.sum)
    return results

def strassen_helper(A,B, alltogether=False):
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

    if alltogether:
        C11 = sum_matrices([M1, M4, M5, M7]) #((M1 + M4) - M5) + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = sum_matrices([M1, M2, M3, M6]) # ((M1 - M2) + M3) + M6
    else:
        C11 = ((M1 + M4) - M5) + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = ((M1 - M2) + M3) + M6
    if isinstance(C11, np.ndarray):
        first_row = np.concatenate([C11, C12], axis=1)
        second_row = np.concatenate([C21, C22], axis=1)
        return np.concatenate([first_row, second_row], axis=0)
    else:
        return np.array([[C11, C12], [C21, C22]])

if __name__ == "__main__":
    strassen_matmult(1, alltogether=True)
    solver.render("strassen_mamult_out.png")