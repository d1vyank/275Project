from urllib.parse import urlparse

from get_page import *
from htmlparser import *

"""
This function fetches each url and feeds the html page to the parser. The parser
looks for hyperlinks within the page. After validating the link, it is added to the graph.
"""

def find_edges(g, md):
    for key in md.keys():
        try:
            filename, html, headers = get_page(key)
        except:
            #Print URLs that could not be fetched
            print(key)
            continue
        try:
        	#Read html file
            s = str(html.read())
            parser.links = []
            parser.feed(s)
        except:
            print("Invalid HTML file")
            print(key)
            continue
        for link in parser.links:
            if link == '':
                continue
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
                link = scheme + '://' + netloc + link
            #Ignore protocols other than http
            elif link[0 - 4] != 'http':
                continue
            if link in g.vertices():
                if key != link and g.is_edge((key, link)) == False:
                    g.add_edge((key, link))
    return g