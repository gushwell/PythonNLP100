import re
import functools

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

    def concatMorphs(self):
        seq = filter(lambda x: x.pos != '記号', self.morphs)
        return functools.reduce(lambda x, y: x + y.surface, seq, '')

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

def findNouns(sentence):
    for chunk in sentence:
        for m in chunk.morphs:
            if m.pos == '名詞':
                yield chunk
                break

def makePath(sentence, chunk):
    curr = sentence[chunk.number]
    path = []
    while curr.dst >= 0:
        path.append(curr.concatMorphs())
        curr = sentence[curr.dst]
    path.append(curr.concatMorphs())
    return path

def enumPath(article):
    for sentence in article:
        for chunk in findNouns(sentence):
            path = makePath(sentence, chunk)
            if len(path) >= 2:
                yield path

def main():
    article = analyze()
    with open('result48.txt', 'w', encoding='utf8') as w:
        for path in enumPath(article):
            w.write('{}\n'.format(' -> '.join(path)))

if __name__ == '__main__':
    main()
