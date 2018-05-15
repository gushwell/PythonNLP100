import re
import os
import functools
import pydot_ng as pydot

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

def toDot(sentence):
    edges = []
    for chunk in sentence:
        if chunk.dst >= 0:
            edges.append((chunk.concatMorphs(), sentence[chunk.dst].concatMorphs()))
    return edges

def main():
    graph = pydot.Dot(graph_type='digraph')
    graph.set_node_defaults(fontname='Meiryo UI', fontsize='10')

    article = analyze()
    for s, t in toDot(article[4]):
        graph.add_edge(pydot.Edge(s, t))
    graph.write_png('result44.png')

if __name__ == '__main__':
    main()
