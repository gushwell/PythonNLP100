from xml.etree import ElementTree

class CoreferenceAnalyser:
    def __init__(self, filepath):
        xdoc = ElementTree.parse(filepath)
        root = xdoc.getroot()
        self.sentences = root.find('document/sentences')
        self.coreference = root.find('document/coreference')

    def enumCoreference(self):
        for e in self.coreference:
            yield e

    # mentionのtext内容をrepresentativeMentionの内容に置き換える
    def replaceMention(self, mention, representativeMention):
        sentenceid = mention.find('sentence').text
        startid = mention.find('start').text
        endid = str(int(mention.find('end').text) - 1)
        targetSentence = self.sentences.find("sentence[@id='" + sentenceid  + "']")
        startToken = targetSentence.find("tokens/token[@id='" + startid + "']")
        endToken = targetSentence.find("tokens/token[@id='" + endid + "']")

        text = representativeMention.find('text').text

        startword = startToken.find('word')
        startword.text = '「{}({}'.format(text, startword.text)
        endword = endToken.find('word')
        endword.text = endword.text + ')」'

    def replaceAll(self):
        for cf in self.enumCoreference():
            rm = cf.find("mention[@representative='true']")
            for m in cf.findall('mention'):
                if 'representative' in m.attrib:
                    continue
                self.replaceMention(m, rm)

    def writeText(self):
        with open('result56.txt', 'w', encoding='utf8') as w:
            prev = ''
            for e in self.sentences.findall('sentence/tokens/token'):
                word = e.find('word').text
                if word == '-LRB-':
                    word = '('
                elif word == '-RRB-':
                    word = ')'
                if word == '.':
                    w.write(word + '\n')
                elif word == ',' or word == '?' or word == '\'' or word == ')':
                    w.write(word)
                elif word == '(':
                    prev = word
                else:
                    if prev == '(':
                        w.write(' (' + word)
                    else:
                        w.write(' ' + word)
                    prev = ''

def main():
    ca = CoreferenceAnalyser('nlp.txt.xml')
    ca.replaceAll()
    ca.writeText()

if __name__ == '__main__':
    main()
