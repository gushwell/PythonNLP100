# 第4章: 形態素解析
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

def main():
    article = analyze()
    print(article[0])
    print()
    print(article[1])
    print()
    print(article[2])

if __name__ == '__main__':
    main()
