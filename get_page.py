import urllib.request

def get_page():
	import urllib.request
	local_filename, headers = urllib.request.urlretrieve('http://python.org/')
	html = open(local_filename)
	return local_filename, html