import re
from collections import namedtuple

def analyze():
    lines = []
    sentence = []
    with open('neko.txt.mecab', 'r', encoding='utf8') as fin:
        for line in fin:
            words = re.split(r'\t|,|\n', line)
            if words[0] == 'EOS':
                # if len(sentense) > 0: って書いたらpylintに怒られた
                if sentence:
                    lines.append(sentence)
                    sentence = []
                continue
            sentence.append({
                "surface": words[0],
                "base": words[7],
                "pos": words[1],
                "pos1": words[2],
            })
    return lines

def extractNounphrases(lines):
    Morpheme = namedtuple('Morpheme', ['surface', 'pos'])
    for sentense in lines:
        prev2 = Morpheme('', '')
        prev1 = Morpheme('', '')
        for word in sentense:
            if word['pos'] == '名詞' and prev1.surface == 'の' and \
               prev1.pos == '助詞' and prev2.pos == '名詞':
                yield prev2.surface + prev1.surface + word['surface']
            prev2 = prev1
            prev1 = Morpheme(word['surface'], word['pos'])

def main():
    article = analyze()
    nouns = [surface for surface in extractNounphrases(article)]
    print(nouns[:50])

if __name__ == '__main__':
    main()
