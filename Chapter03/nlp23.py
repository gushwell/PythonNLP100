import re

def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()

def getSections(article):
    for s in article.split('\n'):
        m = re.match(r'(=+)\s*([^=\s]+)\s*=+', s)
        if m:
            yield m.group(2), len(m.group(1)) - 1

def main():
    article = readArticle('england-article.txt')    
    for name, level in getSections(article):
        print(name, level)

if __name__ == '__main__':
    main()
