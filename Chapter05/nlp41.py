import re

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def toList(self):
        return [self.surface, self.base, self.pos, self.pos1]

class Chunk:
    def __init__(self, number, dst):
        self.number = number
        self.morphs = []
        self.dst = dst
        self.srcs = []

    def print(self):
        print(self.number)
        print([x.toList() for x in self.morphs])
        print(self.dst, self.srcs)
        print()

def analyze():
    article = []
    sentence = []
    chunk = None
    with open('neko.txt.cabocha', 'r', encoding='utf8') as fin:
        for line in fin:
            words = re.split(r'\t|,|\n| ', line)
            if line[0] == '*':
                num = int(words[1])
                destNo = int(words[2].rstrip('D'))
                chunk = Chunk(num, destNo)
                sentence.append(chunk)
            elif words[0] == 'EOS':
                if sentence:
                    for index, c in enumerate(sentence, 0):
                        sentence[c.dst].srcs.append(index)
                    article.append(sentence)
                sentence = []
            else:
                chunk.morphs.append(Morph(
                    words[0],
                    words[7],
                    words[1],
                    words[2],
                ))
    return article

def main():
    article = analyze()
    for c in article[8]:
        c.print()

if __name__ == '__main__':
    main()
