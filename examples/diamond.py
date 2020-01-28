import numpy as np
import sys
sys.path.append('..')
import core.solver  as solver
from core.eig_solver import compute_eigenvalue_bound

def diamond_dag(n):
    arr = np.array([None for _ in range(n*n)]).reshape(n,n)
    in_val = solver.DataNode(0)
    arr[0,0] = in_val
    for i in range(0,n):
        for j in range(0,n):
            if i==0 and j==0:
                continue
            if i + j >= n:
                continue
            prevleft = 1
            prevdown = 1
            if i == 0:
                arr[i,j] = arr[i, j-1] + 1
            elif j == 0:
                arr[i,j] = arr[i-1, j] + 1
            else:
                arr[i,j] = arr[i-1, j] + arr[i, j-1]

diamond_dag(50)
# solver.render("out.png")
print(compute_eigenvalue_bound([4,5,6], 5))