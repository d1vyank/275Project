import graph
import csv

def load_graph(filename = str()):	
	# open File
	file = open(filename , 'r')
	# define graph object
	g = graph.Graph()
	# metadata stores Page titles and URLs
	md = {}
	
	# read file
	reader = csv.reader(file, skipinitialspace=True)
	for row in reader:
		g.add_vertex(row[4])
		md[row[4]] = row[2]
	
	
	return g, md	
	