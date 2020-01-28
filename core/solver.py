import operator
import core.state as state
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import numpy as np

# import viz
OPERATORS = [
    'add', 'mul', 'sub', 'mod', 'truediv', 'lt', 'le', 'eq', 'ne',
    'gt', 'ge', 'getitem', 'contains'
    ]
# you can do contains, but you can't do len or "in"

class DataNode:
    def __init__(self, data, is_input=False):
        self.id = state.GLOBAL_ID_COUNTER
        state.GLOBAL_ID_COUNTER += 1
        self.data = data
        if state.LABEL_VIZ:
            state.GRAPH.add_node(self.id, label=str(self.data))
        else:
            state.GRAPH.add_node(self.id)

    def __str__(self):
        children = str(list(state.GRAPH.successors(self.id)))
        return "ID: %s, Data: %s, Children: %s" % (self.id, self.data, children)

    def mark_as_output(self):
        state.PROGRAM.mark_output(self.id)
    
    def exp(self):
        val = np.exp(self.data)
        child = DataNode(val)
        _add_edge(self.id, child.id, "exp")
        return child

def _add_edge(a_id, b_id, label):
    if state.EDGE_VIZ:
        state.GRAPH.add_edge(a_id, b_id, label=label)
    else:
        state.GRAPH.add_edge(a_id, b_id)

def _binaryoperator(func):
    name = func.__name__
    def inner(self, other):
        if isinstance(other, DataNode):
            val = func(self.data, other.data)
            child = DataNode(val)
            _add_edge(other.id, child.id, name)
            _add_edge(self.id, child.id, name)
        else: # other is just a constant
            child = DataNode(func(self.data, other))
            _add_edge(self.id, child.id, name)
        return child
    return inner

def genop(nodes, func):
    name = func.__name__
    data = [v.data for v in nodes]
    val = func(data)
    child = DataNode(val)
    for v in nodes:
        _add_edge(v.id, child.id, name)
    id_vals = [v.id for v in nodes] + [child.id]
    return child
    
for name in OPERATORS:
    setattr(DataNode, "__%s__" % name, _binaryoperator(getattr(operator, name))) # apply operators

def transform_array(_arr):
    return [DataNode(a) for a in _arr]

def cumulative_bin_op(arr, opname):
    fn = getattr(operator, opname)
    assert len(arr) > 0
    curr = arr[0]
    for i in range(1, len(arr)):
        new_val = fn(curr, arr[i])
        curr = new_val
    return curr

def render(outname="out.png"):
    P = to_agraph(state.GRAPH)
    P.layout(prog='dot')
    P.draw(outname)

def stats():
    degree_vec = state.GRAPH.in_degree()
    degree_vec = [u[1] for u in degree_vec]
    print("num nodes:", len(degree_vec), "max degree", np.max(degree_vec))


def adjacency_matrix(directed=False):
    if directed:
        return nx.adjacency_matrix(state.GRAPH)
    else:
        return nx.adjacency_matrix(state.GRAPH.to_undirected())
    
