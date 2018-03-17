import json
import re
import urllib.request
import urllib.parse

def readArticle(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        return fin.read()

def getImageFileName(article):
    basicInfo = re.search(r'\{\{基礎情報(.+?)\}\}\n', article, re.DOTALL).group(1)
    pat = r'^\|国旗画像\s*=\s*(.+?)\n'
    reg = re.compile(pat, re.MULTILINE | re.DOTALL)
    m = reg.search(basicInfo)
    return m.group(1)

def getImage(finename):
    url = 'https://ja.wikipedia.org/w/api.php?' \
        + 'action=query' \
        + '&format=json' \
        + '&titles=File:' + urllib.parse.quote(finename) \
        + '&prop=imageinfo' \
        + '&iiprop=url'
    with urllib.request.urlopen(url) as res:
        #x = res.read()
        #y = x.decode()
        #js = json.loads(y)
        data = json.loads(res.read().decode())
        # print(data)
        return data['query']['pages']['-1']['imageinfo'][0]['url']


def main():
    # england-article.txtは、問題20(nlp20.py)で作成したファイル
    article = readArticle('england-article.txt')  
    fname = getImageFileName(article)
    print(getImage(fname))

if __name__ == '__main__':
    main()
