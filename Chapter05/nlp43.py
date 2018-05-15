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

# chunkの中に、posで指定した品詞が含まれているかを確かめる
def contains(chunk, pos):
    return any(m.pos == pos for m in chunk.morphs)

## 名詞を含んだ文節が、動詞を含んだ文節に係るものを抜き出す。
def extract(article):
    for sentence in article:
        for chunk in sentence:
            if chunk.dst >= 0 and contains(chunk, '名詞'):
                target = sentence[chunk.dst]
                if contains(target, '動詞'):
                    yield chunk, target

## nounとverbをタブ区切りで表示する
def printPairs(wr, noun, verb):
    s = noun.concatMorphs()
    if s != '':
        t = verb.concatMorphs()
        wr.write("{}\t{}\n".format(s, t))

def main():
    article = analyze()
    with open('chapter05/result43.txt', 'w', encoding='utf8') as w:
        for noun, verb in extract(article):
            printPairs(w, noun, verb)

if __name__ == '__main__':
    main()
