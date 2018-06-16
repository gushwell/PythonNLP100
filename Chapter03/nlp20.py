# 第3章: 正規表現
import json
import gzip

def extract(title):
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf8') as fin:
        for line in fin:
            jsd = json.loads(line)
            if jsd['title'] == title:
                return jsd['text']
    return ''

def main():
    article = extract('イギリス')
    with open('england-article.txt', 'w', encoding='utf8') as fout:
        fout.write(article)

if __name__ == '__main__':
    main()
