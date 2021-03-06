from xml.etree import ElementTree

def getWords():
    xdoc = ElementTree.parse('nlp.txt.xml')
    root = xdoc.getroot()
    sentences = root.find('document/sentences')
    for e in sentences.findall('sentence/tokens/token/word'):
        yield e


def main():
    with open('result53.txt', 'w', encoding='utf8') as w:
        for word in getWords():
            w.write(f'{word.text}\n')
       
if __name__ == '__main__':
    main()
