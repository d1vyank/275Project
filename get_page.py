import urllib.request
from urllib.error import URLError, HTTPError


def get_page(url):
    import urllib.request

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