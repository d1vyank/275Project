import graph
from get_page import *
from htmlparser import *
from urllib.parse import urlparse


def find_edges(g,md):
	for key in md.keys():
		try:
			filename,html,headers = get_page(key)
		except:
			print(key)
			continue	
		s = str(html.read())
		parser.links = []
		parser.feed(s)
		for link in parser.links:
			#Ignore URLs with specified IDs
			if link[0] == '#':
				continue
			#Ignore javascript
			elif link[0:10] == 'javascript':
				continue
			#Ignore files and scripts	
			elif link[0:2] == '//':
				continue		
			#Handle URLs with relative paths
			elif link[0] == '/':
				scheme, netloc, path, params, query, fragment = urlparse(key)
				link = scheme +'://' + netloc + link
			#Ignore protocols other than http
			elif link[0-4] != 'http':
				continue
			if link in g.vertices():
				if key != link and g.is_edge((key,link)) == False:
					g.add_edge((key, link))
	return g			