import re

def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()

def getBasicInfo(article):
    basicInfo = re.search(r'\{\{基礎情報(.+?)\}\}\n', article, re.DOTALL).group(1)
    pat = r'^\|(.+?)\s*=\s*(.+?)(?<!<br/>)\n'
    reg = re.compile(pat, re.MULTILINE | re.DOTALL)
    wdict = {}
    for k, v in reg.findall(basicInfo):
        wdict[k] = v
    return wdict

def main():
    article = readArticle('england-article.txt')    
    dic = getBasicInfo(article)
    dic = sorted(dic.items(), key=lambda x: x[0])
    for item, v in dic:
        print(item, ':', v)

if __name__ == '__main__':
    main()