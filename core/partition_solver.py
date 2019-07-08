import metis
from collections import defaultdict
import networkx as nx
import math
from os import path, mkdir
import numpy as np
import pickle as pkl
import cvxpy as cp
import core.state as state
import core.solver as solver

CHECKPOINT = False

class ILP_Bound:
    def __init__(self, verbose=True):
        self.M = None
        self.disk_count = None
        self.partitions = None # Adjacency + disk
        self.results = None # appended results
        self.out_pkl_dir = None
        self.verbose = verbose

    def load_and_continue(out_pkl_dir):
        """
        Load the current state and continue operation for computing the lower bound
        """
        assert path.isdir(out_pkl_dir), "the pickle directory does not exist"
        assert path.exists("%s/state.pkl" % out_pkl_dir), "the state pickle does not exist"
        assert path.exists("%s/results.pkl" % out_pkl_dir), "the result pickle does not exist"

        self.out_pkl_dir = out_pkl_dir
        ilp_state = pkl.load(open("%s/state.pkl" % self.out_pkl_dir, "rb"))
        self.M = ilp_state[0]
        self.disk_count = ilp_state[1]
        self.partitions = ilp_state[2]
        self.results = pkl.load(open("%s/results.pkl" % self.out_pkl_dir, "rb"))
        self._solve()
        return np.sum(self.results), self.disk_count
    
    def solve_lb(self, M, out_pkl_dir):
        """
        Solve for a lower bound (from scratch)
        """
        # solve the partition from scratch
        if CHECKPOINT:
            if not path.isdir(out_pkl_dir):
                mkdir(out_pkl_dir) # make the directory if it doesn't already exist
        self.out_pkl_dir = out_pkl_dir
        self.M = M
        self.partitions = self._partition_graph() # partition the graph
        k = len(self.partitions)
        self.results = [None for _ in range(k)]
        self._save_state()  
        self._save_results()
        self._solve()
        print("Disk count", self.disk_count)
        return np.sum(self.results), self.disk_count
        # ready to start solving
    
    def solve_ILP(self, M):
        A = solver.adjacency_matrix(directed=True)
        self._mark_sources_sinks()
        disk = np.array([d for _, d in state.GRAPH.nodes(data="disk")])
        return self._optimize(A, disk, M), self.disk_count

    def _save_state(self):
        # save M, disk count, and partitions
        ilp_state = [self.M, self.disk_count, self.partitions]
        if CHECKPOINT:
            pkl.dump(ilp_state, open("%s/state.pkl" % self.out_pkl_dir, "wb"))
    
    def _save_results(self):
        # save sum results
        if CHECKPOINT:
            pkl.dump(self.results, open("%s/results.pkl" % self.out_pkl_dir, "wb"))

    def _solve(self):
        k = len(self.partitions)
        for i in range(k):
            if self.results[i] is not None:
                # we already did this partition
                continue
            A, disk = self.partitions[i]
            self._debug("------optimizing partition %d --------" % i)
            _, result = self._optimize(A, disk, self.M)
            self.results[i] = result
            self._debug("------done optimizing partition %d with result %f ------" % (i, result))
            self._save_results() # save out the new state
        
    def _mark_sources_sinks(self):
        G = state.GRAPH
        n = len(state.GRAPH.nodes)
        out_degrees = G.out_degree()
        in_degrees = G.in_degree()
        self.disk_count = 0
        for i in range(n):
            if out_degrees[i] == 0 or in_degrees[i] == 0:
                G.nodes[i]["disk"] = 1
                self.disk_count += 1
            else:
                G.nodes[i]["disk"] = 0
        self._debug("Disk count: %d" % self.disk_count)

    def _debug(self, msg):
        if self.verbose:
            print(msg)

    
    def _partition_graph(self):
        self._mark_sources_sinks()
        n = len(state.GRAPH.nodes)
        parts = math.ceil(float(n)/state.MAX_LP_SIZE)
        if parts == 1: # only one part
            A = solver.adjacency_matrix(directed=True)
            disk = np.array([d for _, d in state.GRAPH.nodes(data="disk")])
            return [(A, disk)]
        U = state.GRAPH.to_undirected()
        _, parts = metis.part_graph(U, nparts=parts, objtype="cut", contig=True)
        partitions = defaultdict(list)
        for i, p in enumerate(parts):
            partitions[p].append(i)
        graph_partitions = []
        for p_list in partitions.values():
            induced_graph_G = state.GRAPH.subgraph(p_list)
            A = nx.adjacency_matrix(induced_graph_G)
            disk = np.array([d for _, d in induced_graph_G.nodes(data="disk")])
            graph_partitions.append((A, disk))
        
        return graph_partitions

    def _create_var(shape, is_mip, constraints):
        if is_mip:
            var = cp.Variable(shape=shape, integer=True)
        else:
            var = cp.Variable(shape=shape)
        constraints.append(var >= np.zeros(shape))
        constraints.append(var <= np.ones(shape))
        return var

    def _optimize(self, A, disk, M):
        n = A.shape[0]
        print(n)
        constraints = []
        X = cp.Variable(shape=(n,n), boolean=True)
        Y = cp.Variable(shape=(n,n), boolean=True)
        Z = cp.Variable(shape=n, boolean=True)
        W = cp.Variable(shape=(n,n), boolean=True)

        zero_v = np.zeros((n,1))
        one_v = np.ones((n,1))
        I = np.identity(n)
        Z_vec = cp.reshape(Z, (n, 1))

        # W constraints
        Y_prev = cp.hstack([zero_v, Y[:, :n-1]])
        Y_prev_not = np.ones((n,n)) - Y_prev
        constraints.append(np.zeros((n,n)) <= Y + Y_prev_not - 2*W )
        constraints.append(np.ones((n,n)) >= Y + Y_prev_not - 2*W )

        # permutation constraints
        constraints.append(cp.sum(X, axis=1) == np.ones(n))
        constraints.append(cp.sum(X, axis=0) == np.ones(n))

        # cache limit constraints
        for i in range(n):
            constraints.append(cp.sum(Y[:, i]) <= M) # cache limit
            constraints.append(cp.sum(X[:,:(i+1)], axis=1) >= Y[:, i]) # previous cache comparison
            constraints.append(W[:,i] <= X[:,i] + Z) # new cache elements must be less than disk + new elements
            constraints.append(W[:,i] >= X[:, i])
            constraints.append( Y[:, i:i+1] >= (A + I) @ X[:, i:i+1]) # adjacency constraint
            constraints.append(cp.sum(Y[:, i] - Y_prev[:, i]) >= 0) # can only maintain or increase cache size

        obj = cp.Minimize(cp.sum(Z) + cp.sum(W) - cp.sum(X))
        prob = cp.Problem(obj,constraints)
        prob.solve(solver=cp.GUROBI, verbose=True, Threads=state.NUM_THREADS)
        assert(prob.status in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE])
        return X.value, prob.value

def relabel_graph(X):
    G = state.GRAPH
    n = len(G.nodes)
    for i in range(n):
        num = np.argmax(X[:,i])
        G.nodes[i]['label'] = num
    solver.render()
