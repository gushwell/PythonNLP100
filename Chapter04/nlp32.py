import re
 
def analyze():
    lines = []
    sentence = []
    with open('neko.txt.mecab', 'r', encoding='utf8') as fin:
        for line in fin:
            words = re.split(r'\t|,|\n', line)
            if words[0] == 'EOS':
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

def extractVerbs(lines):
    for sentense in lines:
        seq = filter(lambda w: w['pos'] == '動詞', sentense)
        yield from map(lambda w: (w['surface'], w['base']), seq)

def main():
    article = analyze()
    verbs = [(surface, base) for surface, base in extractVerbs(article)]
    print(verbs[:50])

if __name__ == '__main__':
    main()
