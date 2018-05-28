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

class Pair:
    def __init__(self, particle, paragraph):
        self.particle = particle
        self.paragraph = paragraph

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


def findVerbs(sentence):
    for chunk in sentence:
        for m in reversed(chunk.morphs):
            if m.pos == '動詞':
                yield m, chunk.number
                break

def findParticles(sentence, chunkNo):
    for chunk in sentence:
        if chunk.dst == chunkNo:
            nextMorph = Morph('', '', '', '')
            for m in reversed(chunk.morphs):
                if nextMorph.pos == '助詞':
                    yield m, nextMorph, chunk.concatMorphs()
                    break
                nextMorph = m

def enumPattern(article):
    for sentence in article:
        for v, num in findVerbs(sentence):
            pairlist = []
            obj = ''
            for part1, part2, para in findParticles(sentence, num):
                if part1.pos == '名詞' and part1.pos1 == 'サ変接続' and part2.surface == 'を':
                    obj = part1.surface + part2.surface
                else:
                    pairlist.append(Pair(part2.surface, para))
            if pairlist and obj != '':
                yield obj+v.base, sorted(pairlist, key=lambda x: x.particle)

def main():
    article = analyze()
    with open('result47.txt', 'w', encoding='utf8') as w:
        for v, pairList in enumPattern(article):
            w.write('{}\t{}\t{}\n'.format(v, ' '.join([x.particle for x in pairList]), \
                ' '.join([x.paragraph for x in pairList])))

if __name__ == '__main__':
    main()
