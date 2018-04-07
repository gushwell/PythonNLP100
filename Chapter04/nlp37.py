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

def plotBarChart(sortedwords):
    categories = [x[0] for x in sortedwords]
    xaxis = [x for x in range(10)]
    values = [x[1] for x in sortedwords]

    #plt.rcParams['font.family'] = 'AppleGothic' 
    plt.rcParams['font.family'] = 'Meiryo' 

    plt.bar(xaxis, values)
    plt.xticks(xaxis, categories)
    plt.show()

def main():
    article = analyze()
    words = getFrequency(article)
    sortedwords = sorted(words.items(), key=lambda x: x[1], reverse=True)[0:10]
    print(sortedwords)
    plotBarChart(sortedwords)

if __name__ == '__main__':
    main()
