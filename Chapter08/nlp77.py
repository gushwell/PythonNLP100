import re
from nltk import stem
#import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, \
     f1_score, precision_score, recall_score
from sklearn.externals import joblib

class Stopwords:
    words = [ \
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
    def __init__(self):
        self.stemmer = stem.PorterStemmer()
        self.validreg = re.compile(r'^[-=!@#$%^&*()_+|;";,.<>/?]+$')
        self.splitreg = re.compile(r'\s|,|\.|\(|\)|\'|/|\'|\[|\]|-')

    def isValid(self, word):
        if word == '' or len(word) <= 2:
            return False
        if self.validreg.match(word):
            return False
        return not Stopwords.exists(word)

    def getFromLine(self, line):
        array = self.splitreg.split(line)
        # こういう時はlambda キーワードいらないんですね。
        words = filter(self.isValid, array)
        xs = map(self.stemmer.stem, words)
        return xs

    def enumerate(self, filename, encoding):
        with open(filename, 'r', encoding=encoding) as fin:
            for line in fin:
                sentiment = line[:3]
                yield sentiment, self.getFromLine(line[3:])

class SentimentAnalyser:
    def __init__(self):
        self.cv = CountVectorizer(encoding='utf-8')
        self.lr = LogisticRegression(solver='sag', max_iter=10000)

    # LogisticRegression を使い学習する
    def fit(self, X_train, y_train):
        X_train_cv = self.cv.fit_transform(X_train)
        self.lr.fit(X_train_cv, y_train)

    # LogisticRegression を使い予測する
    def predict(self, X_test):
        x = self.cv.transform(X_test)
        return self.lr.predict(x)

    # 予測し、分類毎に確率を得る
    def predict_proba(self, X_test):
        x = self.cv.transform(X_test)
        return self.lr.predict_proba(x)

    # 学習済みデータをロードする
    def load(self):
        self.cv = joblib.load('chapter08/cv73.learn')
        self.lr = joblib.load('chapter08/lr73.learn')

    # 学習済みデータを保存する
    def save(self):
        # 学習したデータを保存する
        joblib.dump(self.cv, 'chapter08/cv73.learn')
        joblib.dump(self.lr, 'chapter08/lr73.learn')

    # 学習に利用するデータを取り出す
    # y[] は、センチメント
    # X[] は、素性データ
    @staticmethod
    def getFeatureData(filename):
        X = []
        y = []
        sf = SentimentFeatures()
        for sentiment, features in sf.enumerate(filename,'utf-8'):
            y.append(1.0 if sentiment[0] == '+' else 0.0)
            X.append(' '.join(features))
        return X, y

def main():
    sa = SentimentAnalyser()
    sa.load()
    X_test, y_test = sa.getFeatureData('chapter08/sentiment.txt')
    y_test_pred = sa.predict(X_test)
    print('正解率 accuracy:', accuracy_score(y_test, y_test_pred))
    print('適合率 precision:', precision_score(y_test, y_test_pred))
    print('再現率 recall:', recall_score(y_test, y_test_pred))
    print('F1スコア f1_score:', f1_score(y_test, y_test_pred))

    print(classification_report(y_test, y_test_pred))

if __name__ == '__main__':
    main()
