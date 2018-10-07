import re
from nltk import stem
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib

class Stopwords:
    words = [
        'a', 'about', 'all', 'an', 'and', 'any', 'are', 'as', \
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


class SentimentAnalyser:
    def __init__(self):
        self.cv = CountVectorizer(encoding='utf-8')
        self.lr = LogisticRegression(solver='sag', max_iter=10000)

    # LogisticRegression を使い学習する
    def fit(self, X_train, y_train):
        X_train_cv = self.cv.fit_transform(X_train)
        self.lr.fit(X_train_cv, y_train)

    # 学習済みデータを保存する
    def save(self):
        # 学習したデータを保存する
        joblib.dump(self.cv, 'chapter08/cv73.learn')
        joblib.dump(self.lr, 'chapter08/lr73.learn')

    # 学習に利用するデータを取り出す
    # X[] は、素性データ
    # y[] は、センチメント （正解データ)
    @staticmethod
    def getFeatureData(filename):
        X = []
        y = []
        sf = SentimentFeatures(filename)
        for sentiment, features in sf.enumerate():
            y.append(1.0 if sentiment[0] == '+' else 0.0)
            X.append(' '.join(features))
        return X, y

def main():
    sa = SentimentAnalyser()
    X_train, y_train = sa.getFeatureData('chapter08/sentiment.txt')
    sa.fit(X_train, y_train)
    sa.save()

if __name__ == '__main__':
    main()
