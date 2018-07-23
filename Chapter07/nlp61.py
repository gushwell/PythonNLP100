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

def enumKeys():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    v = r.get('The Silhouettes').decode()
    print(v)
    v = r.get('The Wanderers').decode()
    print(v)
    v = r.get('桑田佳祐').decode()
    print(v)


def main():
    #register()
    enumKeys()



if __name__ == '__main__':
    main()
