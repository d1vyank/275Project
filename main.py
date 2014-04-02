from load_graph import *
from find_edges import *

if __name__ == "__main__":
    g, md = load_graph('history.csv')
    g = find_edges(g, md)