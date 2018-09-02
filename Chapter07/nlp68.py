import json
import pymongo

def findDance():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['MusicBrainzDb']
    co = db['artists']
    return co.find({'tags.value': 'dance'}).sort('rating.count', pymongo.DESCENDING)

def main():
    for d in findDance()[0:10]:
        print('{} - {}'.format(d['name'], d['rating']['count']))
        #print(f'{d['name']} - {d['rating']['count']}')

if __name__ == '__main__':
    main()
