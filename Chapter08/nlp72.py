import re
from nltk import stem

class Stopwords:
    words = ['a', 'about', 'all', 'an', 'and', 'any', 'are', 'as', \
            'at', 'be', 'been', 'but', 'by', 'can', 'could', 'do', \
            'does', 'for', 'from', 'has', 'have', 'he', 'her', 'his', \
            'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'made', \
            'make', 'may', 'me', 'my', 'no', 'not', 'of', 'on', 'one', \
            'or', 'out', 'she', 'should', 'so', 'some', 'than', 'that', \
            'the', 'their', 'them', 'there', 'then', 'they', 'this', \
            'those', 'to', 'too', 'us', 'was', 'we', 'what', 'when',\
            'which', 'who', 'with', 'would', 'you', 'your', ''
        ]

    @staticmethod
    def exists(word):
        return word in  Stopwords.words

class SentimentFeatures:
    def __init__(self, filename):
        self.filename = filename
        self.stemmer = stem.PorterStemmer()

    @staticmethod
    def isValid(word):
        if word == '' or len(word) <= 2:
            return False
        if re.match(r'^[-=!@#$%^&*()_+|;";,.<>/?]+$', word):
            return False
        return not Stopwords.exists(word)

    def getFromLine(self, line):
        sentiment = line[:3]
        array = re.split(r'\s|,|\.|\(|\)|\'|/|\'|\[|\]|-', line[3:])
        # こういう時はlambda キーワードいらないんですね。
        words = filter(self.isValid, array)
        xs = map(self.stemmer.stem, words)
        return sentiment, xs

    def enumerate(self):
        with open(self.filename, 'r') as fin:
            for line in fin:
                yield self.getFromLine(line)

def main():
    sf = SentimentFeatures('sentiment.txt')
    for sentiment, features in list(sf.enumerate())[:50]:
        print(sentiment, " ".join(features))

if __name__ == '__main__':
    main()
