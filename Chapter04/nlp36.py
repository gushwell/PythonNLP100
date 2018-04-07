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
 
def getFrequency(lines):
    words = {}
    for sentense in lines:
        for word in sentense:
            if word['pos'] == '記号':
                continue
            if word['surface'] in words.keys():
                words[word['surface']] += 1
            else:
                words[word['surface']] = 1
    return words
 
def main():
    article = analyze()
    words = getFrequency(article)
    sortedwords = sorted(words.items(), key=lambda x: x[1], reverse=True)
    for i in range(0, 100):
        print(i, sortedwords[i][0], sortedwords[i][1])
 
if __name__ == '__main__':
    main()
