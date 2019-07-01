from collections import defaultdict
import math
import networkx as nx
import numpy as np
import metis
import core.state as state
from multiprocessing import Pool
import functools
def get_dead_anc(G, x):
    # return the dead ancestors
    ancestors = nx.ancestors(G,x)
    def check_dead(u):
        for v in G.successors(u):
            if v not in ancestors:
                return False
        return True

    dead_anc = set()
    for anc in ancestors:
        if check_dead(anc):
            dead_anc.add(anc)
    return dead_anc, ancestors

def transformGraph(G, x):
    dead_anc, ancestors = get_dead_anc(G, x)
    desc = nx.descendants(G, x)
    V = set(G.nodes)
    V_prime = V - dead_anc.union(desc)
    G_ = nx.DiGraph()
    # 1
    G_.add_node("s")
    G_.add_node("t")

    # 2
    for v in V_prime:
        G_.add_edge("%d_h" % v, "%d_t" % v, weight=1)

    # 3
    U = ancestors.intersection(V_prime)
    for u in U:
        G_.add_edge("s", "%d_h" % u, weight=1)
    
    # 4, 6
    G_prime = nx.subgraph(G, V_prime)
    for (u,v) in G_prime.edges():
        G_.add_edge("%d_t" % u, "%d_h" % v, weight=1)
        G_.add_edge("%d_h" % v, "%d_h" % u, weight=np.infty)
    
    # 5
    for (u,v) in G.edges():
        if u in V_prime and v in desc:
            G_.add_edge("%d_t" % u, "t", weight=1)
    return G_

def find_max_min_st_cut(G_):
    nodes = list(G_.nodes)
    val = nx.minimum_cut_value(G_, "s", "t", capacity="weight")
    return val

def worker(x, G):
    G_ = transformGraph(G, x)
    return find_max_min_st_cut(G_)

def subdag(G, M):
    W = 0
    n = len(G.nodes)
    arr = list(G.nodes)
    with Pool(state.NUM_THREADS) as p: 
        fn = functools.partial(worker, G=G)
        result = p.map(fn, arr)
    #for x in arr:
    #    W = max(W, find_max_min_st_cut(transformGraph(G, x)))
    W = max(result)
    return max(0, 2*(W-M))

def partition(M, parts):
    G = state.GRAPH
    n = len(G.nodes)
    #parts = math.ceil(float(n)/(2*M))
    #parts = math.ceil(float(n)/(2*M))
    if parts == 1:
        return [G]
    else:
        _, parts = metis.part_graph(G.to_undirected(), nparts=parts, objtype="cut")
        partitions = defaultdict(list)
        for i, p in enumerate(parts):
            partitions[p].append(i)
        graphs = []
        for p_list in partitions.values():
            induced_graph_G = G.subgraph(p_list)
            graphs.append(induced_graph_G.copy())
        return graphs

def get_elango_bound_helper(M, parts):
    partitions = partition(M, parts)
    result = 0
    for p in partitions:
        interm_result = subdag(p, M)
        result += interm_result
    return result

def get_elango_bound(M):
    """
    n = math.ceil(len(state.GRAPH.nodes)/float(2*M))
    best_val = 0
    for parts in range(2,3):
        val = get_elango_bound_helper(M, parts)
        print(parts, val)
        if val < best_val:
            break
        else:
            best_val = val
    return best_val
    """
    return get_elango_bound_helper(M, 1)
