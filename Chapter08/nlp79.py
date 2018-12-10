import re
from nltk import stem
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

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
        for sentiment, features in sf.enumerate(filename, 'utf-8'):
            y.append(1.0 if sentiment[0] == '+' else 0.0)
            X.append(' '.join(features))
        return X, y

# 参考URL http://ohke.hateblo.jp/entry/2017/08/25/230000

def main():
    sa = SentimentAnalyser()
    X, y = sa.getFeatureData('chapter08/sentiment.txt')
    # 5分割交差検定を行うためにデータを分割する
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # ベクターに変換
    #X_train_cv = sa.trainToVector(X_train)
    #X_test_cv = sa.testToVector(X_test)

    # 学習
    sa.fit(X_train, y_train)

    # 予測
    pp = sa.predict_proba(X_test)
    print(pp[:, 1])
    print()
    print(pp[:5, 1])

    # +1の予測確率を取り出す  [:, 1] は、1列目のすべてのデータ
    pred_positive = sa.predict_proba(X_test)[:, 1]

    # ある閾値の時の適合率、再現率, 閾値の値を取得
    precisions, recalls, thresholds = precision_recall_curve(y_test, pred_positive)

    # 0から1まで0.05刻みで○をプロット
    for i in range(21):
        close_point = np.argmin(np.abs(thresholds - (i * 0.05)))
        plt.plot(precisions[close_point], recalls[close_point], 'o')

    # 適合率-再現率曲線
    plt.plot(precisions, recalls)
    plt.xlabel('Precision')
    plt.ylabel('Recall')

    plt.show()
    input()

if __name__ == '__main__':
    main()
