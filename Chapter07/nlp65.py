import json
import pymongo
from bson.objectid import ObjectId

def ObjectIdToStr(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(repr(o) + " is not suported")

def find(name):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['MusicBrainzDb']
    co = db['artists']
    return co.find({'name': name})

def printArtist(artist):
    print('')
    #print(json.dumps(artist, indent=4,  sort_keys=True, default=ObjectIdToStr))
    print(json.dumps(artist, indent=4, ensure_ascii=False, sort_keys=True))

def main():
    for d in find('Queen'):
        printArtist(d)

if __name__ == '__main__':
    main()
