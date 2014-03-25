import graph
import csv

def load_graph(filename = str()):	
	#Open File
	file = open(filename , 'r')
	# Define graph object and metadata dict
	g = graph.Graph()
	# Metadata dict to store Page titles and URLs
	md = {}
	
	# Read file
	reader = csv.reader(file, skipinitialspace=True)
	for row in reader:
		g.add_vertex(row[2])
		md[row[2]] = row[4]
	
	
	return g, md	
	