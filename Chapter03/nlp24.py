import json
import re
 
def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()
 
def getMediaFfiles(article):
    reg = re.compile(r'(?:File|ファイル):([^\|]+)\|')
    for s in article.split('\n'):
        m = reg.search(s)
        if m:
            yield m.group(1)
 
def main():
    article = readArticle('england-article.txt')    
    for name in getMediaFfiles(article):
        print(name)
 
if __name__ == '__main__':
    main()