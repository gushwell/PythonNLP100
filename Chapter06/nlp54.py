import re
from xml.etree import ElementTree

def getWords():
    xdoc = ElementTree.parse('nlp.txt.xml')
    root = xdoc.getroot()
    sentences = root.find('document/sentences')
    for e in sentences.findall('sentence/tokens/token'):
        yield e.find('word'), e.find('lemma'), e.find('POS')

def main():
    with open('result54.txt', 'w', encoding='utf8') as w:
        for word, lemma, pos in getWords():
            m = re.search(r'[A-Z]', pos.text)
            if m:
                w.write(f'{word.text}\t{lemma.text}\t{pos.text}\n')


if __name__ == '__main__':
    main()
