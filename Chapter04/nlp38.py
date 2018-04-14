import re
import matplotlib.pyplot as plt
 
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
 
def getHistogramData(words):
    hist = {}
    for word in words.items():
        if word[1] in hist.keys():
            hist[word[1]] += 1
        else:
            hist[word[1]] = 1
    return words
 
def plotHistgram(data):
    xs = [x[1] for x in data]

    plt.rcParams['font.family'] = 'Meiryo' 
 
    plt.hist(xs, bins=25, range=(1, 25))
    plt.xlim(xmin=1, xmax=25)
    plt.xlabel('単語の出現頻度')
    plt.ylabel('単語の種類数')
    plt.show()
 
def main():
    article = analyze()
    words = getFrequency(article)
    histData = getHistogramData(words)
    sortedData = sorted(histData.items(), key=lambda x: x[1], reverse=True)
    print(sortedData[0:20])

    plotHistgram(sortedData)
 
if __name__ == '__main__':
    main()