import sys
sys.path.append('..')
import numpy as np
import core.solver as solver 
import core.state as state 

def stringify_binary(a):
    return ''.join([str(u) for u in a])

def tsp_helper(curr_encoding, nodes):
    neighbors = []
    for i in range(len(curr_encoding)):
        if curr_encoding[i] == 1:
            cp = np.copy(curr_encoding)
            cp[i] = 0
            neighbors.append(cp)
    neighboring_nodes = [nodes[stringify_binary(u)] for u in neighbors]
    if len(neighboring_nodes) > 0:
        new_node = solver.genop(neighboring_nodes, np.sum) # stand in for the DP step
    else:
        new_node = solver.DataNode(0)
    nodes[stringify_binary(curr_encoding)] = new_node

def tsp(n):
    nodes = {}
    start_enc = np.zeros(n)
    curr_list = [start_enc]
    queued = set([stringify_binary(start_enc)])
    while len(curr_list) > 0:
        curr_enc = curr_list.pop(0)
        tsp_helper(curr_enc, nodes)
        for i in range(len(curr_enc)):
            if curr_enc[i] == 0:
                cp = np.copy(curr_enc)
                cp[i] = 1
                cp_str = stringify_binary(cp)
                if cp_str not in queued:
                    curr_list.append(cp)
                    queued.add(cp_str)
    assert len(queued) == 2**n

if __name__ == "__main__":
    tsp(5)
    # strassen_matmult(1, alltogether=True)
    solver.render("hypercube.png")