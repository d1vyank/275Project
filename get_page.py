import urllib.request
from urllib.error import URLError, HTTPError

"""
This function fetches URLs using  urllib.
"""
def get_page(url):
    #Retrieve page
    try:
        local_filename, headers = urllib.request.urlretrieve(url)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        html = open(local_filename, encoding="UTF8")
        return local_filename, html, headers