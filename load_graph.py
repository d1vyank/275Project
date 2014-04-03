import csv
from get_icon import *
import graph


def load_graph(filename=str()):
    # open File
    file = open(filename, 'r')
    # define graph object
    g = graph.Graph()
    # metadata stores URL : (Page Title, Icon path)
    md = {}

    # read file
    reader = csv.reader(file, skipinitialspace=True)
    for row in reader:
        g.add_vertex(row[4])
        md[row[4]] = (row[2], get_icon(row[4]))

    return g, md
