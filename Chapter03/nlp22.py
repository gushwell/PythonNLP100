import re

def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()

def getCategories(article):
    for s in article.split('\n'):
        m = re.match(r'\[\[Category:([^|]*)(|.*)?\]\]', s)
        if m:
            yield m.group(1)

def main():
    article = readArticle('england-article.txt')    
    for cat in getCategories(article):
        print(cat)

if __name__ == '__main__':
    main()
