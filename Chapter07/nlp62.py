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

def countjapan():

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    keys = r.keys('*')
    count = 0
    for key in keys:
        v = r.get(key)
        if v == b'Japan':
            count = count + 1
    print(count)


def countjapan2():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    keys = r.scan_iter()
    count = 0
    for key in keys:
        v = r.get(key)
        if v == b'Japan':
            count = count + 1
    print(count)

def main():
    #register()
    countjapan2()



if __name__ == '__main__':
    main()
