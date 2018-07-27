import json
import redis

# redisに接続する。ホスト、ポート、db番号を指定する
# r = redis.StrictRedis(host='localhost', port=6379, db=0)

# # キーと値をセットする
# r.set('key01', 'aaaa')

# # セットした値を取得する
# v = r.get('key01')

# # 文字列型に変換する
# v_str = v.decode()

# # 削除する
# r.delete('key01')

def printTag(r, name):
    v = r.get(name)
    if v != None:
        print('*' + name)
        tags = json.loads(v.decode())
        for tag in tags:
            print("{}\t{}".format(tag['value'], tag['count']))


def enumKv():
    with open('artist.json', 'r', encoding='utf8') as fin:
        for line in fin:
            jsd = json.loads(line)
            if 'tags' in jsd:
                yield jsd['name'], json.dumps(jsd['tags'])

def register():
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    r.flushdb()
    for k, v in enumKv():
        r.set(k, v)
    r.save()

def main():
    register()
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    printTag(r, 'George Winston')
    printTag(r, 'Mariah Carey')
    printTag(r, '松任谷由実')

if __name__ == '__main__':
    main()
