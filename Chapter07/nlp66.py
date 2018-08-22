import pymongo

def countJapan():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['MusicBrainzDb']
    co = db['artists']
    count = co.find({'area': 'Japan'}).count()
    print(count)

def main():
    countJapan()

if __name__ == '__main__':
    main()
