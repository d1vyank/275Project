from html.parser import HTMLParser

"""
We overwrite the HTMLparser to look for hyperlinks and store a list of links on the page
"""

class MyHTMLParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])


parser = MyHTMLParser()