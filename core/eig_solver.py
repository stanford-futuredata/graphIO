import numpy as np 
from networkx.linalg.laplacianmatrix import laplacian_matrix, normalized_laplacian_matrix
from scipy.sparse.linalg import eigs as sparse_eigs
import core.state as state
import networkx as nx

def _get_inputs():
    G = state.GRAPH
    n = len(state.GRAPH.nodes)
    in_degrees = G.in_degree()
    input_enc = np.array([in_degrees[i] == 0 for i in range(n)]).reshape(n,1)
    return input_enc

def _adjust_weights():
    G = state.GRAPH
    out_degrees = G.out_degree()
    for u, v, d in G.edges(data=True):
        deg = out_degrees[u]
        d['weight_out'] = 1/deg

def _get_lap_mat():
    _adjust_weights()
    return laplacian_matrix(state.GRAPH.to_undirected(), weight="weight_out")

def _get_laplacian_spectrum(k=None):
    # get the k smallest eigenvalues of the laplacian
    lap = _get_lap_mat()
    if k is None:
        k = len(state.GRAPH.nodes()) - 2
    lambdas = sparse_eigs(lap, k=k, return_eigenvectors=False, which="SR") # get k smallest eigenvalues
    return np.real(np.sort(lambdas))

def _compute_w_eigs(n, k):
    eig_vals = np.ones(k) * np.floor(n/k)
    for i in range(n % k):
        eig_vals[i] += 1
    return eig_vals

def _laplacian_spectral_bound(lambdas, M):
    # given lambdas, compute the spectral bound
    G = state.GRAPH
    k, n = len(lambdas), len(G.nodes)
    k_vals = list(range(2,k))
    def compute_bound(i):
        w_eigs = _compute_w_eigs(n, i)
        return np.dot(w_eigs, lambdas[:i]) - 2*i*M
    vals = [compute_bound(i) for i in k_vals]
    maxval = np.max(vals)
    maxk = k_vals[np.argmax(vals)]
    return maxval, maxk

def count_inputs_outputs():
    G = state.GRAPH
    n = len(G.nodes)
    out_degrees = G.out_degree()
    in_degrees = G.in_degree()
    count = 0
    for i in range(n):
        if in_degrees[i] == 0 or out_degrees[i] == 0:
            count += 1
    return count

def compute_eigenvalue_bound(M_vals, k=None):
    disk_count = count_inputs_outputs()
    print(disk_count)
    lambdas = _get_laplacian_spectrum(k)
    return disk_count, [_laplacian_spectral_bound(lambdas, M) for M in M_vals]
