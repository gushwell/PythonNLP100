import re

def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()

def getCategories(article):
    for s in article.split('\n'):
        if re.match(r'\[\[Category:.*\]\]', s):
            yield s

def main():
    # england-article.txtは、問題20(nlp20.py)で作成したファイル
    article = readArticle('england-article.txt')    
    for cat in getCategories(article):
        print(cat)

if __name__ == '__main__':
    main()
