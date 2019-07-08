# import cache
import networkx

LABEL_VIZ = False # if label_viz, then label the visualization so that the vertices are data
EDGE_VIZ = False # if true, then label the edges of the visualization with their function names
GRAPH = networkx.DiGraph()
NUM_THREADS = 20
MAX_LP_SIZE = 16
GLOBAL_ID_COUNTER = 0 # id counter for elements
