import urllib.request
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse

def get_icon(url):
	scheme, netloc, path, params, query, fragment = urlparse(url)
	link = scheme + '://' + netloc + '/favicon.ico'
	site_name = netloc.split('.')
	if site_name[0] == 'www':
		name = site_name[1]
	else:
		name = site_name[0]
	path = 'images/' + name + '.png'		
	try:
		local_filename, headers = urllib.request.urlretrieve(link, path)
	except HTTPError as e:
		icon_path = 'images/default.png'
	except URLError as e:
		icon_path = 'images/default.png'
	else:
		icon_path = local_filename
	return icon_path		    
        			
	