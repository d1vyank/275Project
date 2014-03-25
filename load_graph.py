import graph

def load_graph(filename = str()):	
	#Open File
	file = open(filename , 'r')
	# Define graph object and metadata dict
	g = graph.Graph()
	# Metadata dict to store Page titles and URLs
	md = {}
	
	# Read file
	for line in file:
		# Remove trailing white spaces and split comma separated values
		line = line.rstrip()
		values = line.split(',')
		g.add_vertex(values[2])
		md[values[2]] = values[4]
		
	return g, md	
	