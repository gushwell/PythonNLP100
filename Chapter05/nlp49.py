import re
import sys
import copy
import functools

# 形態素を表すクラス
class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def toList(self):
        return [self.surface, self.base, self.pos, self.pos1]

# 文節を表すクラス （複数の形態素からなる）
class Chunk:
    def __init__(self, number, dst):
        self.number = number
        self.morphs = []
        self.dst = dst
        self.srcs = []

    def hasNoun(self):
        for m in self.morphs:
            if m.pos == '名詞':
                return True
        return False

    def concatMorphs(self):
        seq = filter(lambda x: x.pos != '記号', self.morphs)
        return functools.reduce(lambda x, y: x + y.surface, seq, '')

# 文章をsentenceに分割する。ひとつのsentenceは、Chunk(文節)の配列からなる
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
                if destNo == -1:
                    destNo = num + 1
                chunk = Chunk(num, destNo)
                sentence.append(chunk)
            elif words[0] == 'EOS':
                if sentence:
                    sentence.append(Chunk(sys.maxsize, -1))
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

# 名詞句(Chunk)のペアを列挙する
def enumPairs(sentence):
    count = len(sentence)
    for i in range(count):
        for j in range(i+1, count):
            if sentence[i].hasNoun() and sentence[j].hasNoun():
                yield sentence[i], sentence[j]

# ciからのパスの中にcjが含まれているかを調べる
def containsOther(ci, cj, sentence):
    curr = ci
    while curr.dst >= 0:
        if curr == cj:
            return True
        curr = sentence[curr.dst]
    return False

# ciからのパスとcjからのパスが出会う番号を返す
def connectedPoint(ci, cj, sentence):
    k = ci.dst
    while k >= 0:
        curr = cj
        while curr.dst >= 0:
            if curr.number == k:
                return k
            curr = sentence[curr.dst]
        k = sentence[k].dst
    return -1

# chunkの名詞の部分を to で指定した値に変更（オリジナルは変更しない）
def replaceTo(to, chunk):
    dup = copy.deepcopy(chunk)
    for m in dup.morphs:
        if m.pos == '名詞':
            m.surface = to
            break
    return dup

# 'Xで -> 始めて -> 人間という -> Y' というパス文字列を生成
def makePath1(ci, cj, sentence):
    path = []
    curr = replaceTo('X', ci)
    while curr.number < cj.number:
        path.append(curr.concatMorphs())
        curr = sentence[curr.dst]
    path.append('Y')
    return '{}'.format(' -> '.join(path))

# 'Xは | Yという -> ものを | 見た' という形式のパス文字列を生成
def makePath2(ci, cj, ck, sentence):
    ci = replaceTo('X', ci)
    cj = replaceTo('Y', cj)
    p1 = ci.concatMorphs()
    list1 = []
    curr = cj
    while curr.number < ck.number:
        list1.append(curr.concatMorphs())
        curr = sentence[curr.dst]
    p2 = '{}'.format(' -> '.join(list1))
    list2 = []
    curr = ck
    while curr.dst > 0:
        list2.append(curr.concatMorphs())
        curr = sentence[curr.dst]
    p3 = '{}'.format(' -> '.join(list2))
    return '{} | {} | {}'.format(p1, p2, p3)

# １センテンスから、パスを列挙する
def extractPaths(sentence):
    for ci, cj in enumPairs(sentence):
        if containsOther(ci, cj, sentence):
            yield makePath1(ci, cj, sentence)
        else:
            k = connectedPoint(ci, cj, sentence)
            if k > 0:
                yield makePath2(ci, cj, sentence[k], sentence)

# ファイルを読み込み、1センテンス毎に、extractPathsを呼び出し、Path(複数)を取り出し、ファイルに出力
def main():
    article = analyze()
    with open('result49.txt', 'w', encoding='utf8') as w:
        for sentence in article:
            for path in extractPaths(sentence):
                w.write(path + '\n')

if __name__ == '__main__':
    main()
