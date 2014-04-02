from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])


parser = MyHTMLParser()