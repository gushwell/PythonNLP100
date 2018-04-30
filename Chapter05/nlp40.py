import re

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def print(self):
        print([self.surface, self.base, self.pos, self.pos1])

def analyze():
    article = []
    sentence = []
    with open('neko.txt.cabocha', 'r', encoding='utf8') as fin:
        for line in fin:
            words = re.split(r'\t|,|\n| ', line)
            if words[0] == '*':
                continue
            elif words[0] == 'EOS':
                if sentence:
                    article.append(sentence)
                sentence = []
            else:
                sentence.append(Morph(
                    words[0],
                    words[7],
                    words[1],
                    words[2],
                ))
    return article

def main():
    article = analyze()
    for morph in article[3]:
        morph.print()

if __name__ == '__main__':
    main()
