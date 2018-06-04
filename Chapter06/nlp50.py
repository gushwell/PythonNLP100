import re

def enumSentence():
    with open('nlp.txt', 'r', encoding='utf8') as fin:
        for line in fin:
            nl = re.sub(r'(\.|;|:|\?|!)(\s+)([A-Z])', r'\1\n\3', line)
            ss = re.split(r'\n', nl)
            for s in filter(lambda w: len(w) > 0, ss):
                yield s

def main():
    with open('result50.txt', 'w', encoding='utf8') as w:
        for sentence in enumSentence():
            w.write(sentence + '\n')

if __name__ == '__main__':
    main()
