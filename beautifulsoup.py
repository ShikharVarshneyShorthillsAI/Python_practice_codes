from bs4 import BeautifulSoup


class HTMLParser:
    def __init__(self, html_doc):
        """Initialize with HTML content and parse it using BeautifulSoup."""
        self.soup = BeautifulSoup(html_doc, 'lxml')

    def prettify_html(self):
        """Returns a formatted (pretty) version of the HTML."""
        return self.soup.prettify()

    def extract_paragraphs(self):
        """Extracts and returns all <p> tag contents."""
        return [p.text for p in self.soup.find_all('p')]



# Sample HTML
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters</p>
<p class="poem" align="center"> twinkle twinkle little star</p>
</body></html>
"""

# Usage
if __name__ == "__main__":
    parser = HTMLParser(html_doc)

    # Prettify HTML
    print("Formatted HTML:\n", parser.prettify_html())

    # Extract paragraphs
    print("\nExtracted Paragraphs:")
    for para in parser.extract_paragraphs():
        print(para)
