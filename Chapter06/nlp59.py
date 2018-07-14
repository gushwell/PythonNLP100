import re
from xml.etree import ElementTree
from NPExtractor import NPExtractor, Context

class NounPhrases:
    def __init__(self, filepath):
        xdoc = ElementTree.parse(filepath)
        root = xdoc.getroot()
        self.parses = root.findall('document/sentences/sentence/parse')

    def extract(self):
        with open('result59.txt', 'w', encoding='utf8') as w:
            for parse in self.parses:
                ctx = Context(parse.text)
                exp = NPExtractor()
                exp.parse(ctx)
                for p in ctx.nplist:
                    s = re.sub('-LRB-', '(', p)
                    s = re.sub('-RRB-',')', s)
                    w.write(s + '\n')

def main():
    nps = NounPhrases('nlp.txt.xml')
    nps.extract()

if __name__ == '__main__':
    main()
