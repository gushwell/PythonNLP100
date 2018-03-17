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
        v = re.sub(r"''('|''')([^']+?)''+", r"\2", v)
        v = re.sub(r"\[\[(?:[^\]]+\|)?([^:]+?)\]\]", r"\1", v)
        v = re.sub(r"\[http(?:[^\]]+? )?(.+?)\]", r"\1", v)
        v = re.sub(r"#REDIRECT \[\[([^\[]+?)\]\]", r"\1", v)
        v = re.sub(r"^===*\s*(.+)\s*=", r"\1", v)
        v = re.sub(r"^(?:\*|#|;)+\s*([^\n]+?)$", r"\1", v, flags=re.MULTILINE)
        v = re.sub(r"{{(?:[^\{]+\|)?([^\|]+?)}}", r"\1", v)
        v = re.sub(r"<[^>]+>", r" ", v)
        wdict[k] = v

    return wdict


def main():
    # england-article.txtは、問題20(nlp20.py)で作成したファイル
    article = readArticle('england-article.txt')    
    dic = getBasicInfo(article)
    dic = sorted(dic.items(), key=lambda x: x[0])
    for item, v in dic:
        print(item, ':', v)

if __name__ == '__main__':
    main()