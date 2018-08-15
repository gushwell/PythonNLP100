import json
import pymongo

def enumdata():
    with open('artist.json', 'r', encoding='utf8') as fin:
        for line in fin:
            jsd = json.loads(line)
            yield jsd

def register():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['MusicBrainzDb']
    artists = db['artists']
    for data in enumdata():
        artists.insert(data)
    artists.create_index([('name', pymongo.ASCENDING)])
    artists.create_index([('aliases.name', pymongo.ASCENDING)])
    artists.create_index([('tags.value', pymongo.ASCENDING)])
    artists.create_index([('rating.value', pymongo.ASCENDING)])


def main():
    register()

if __name__ == '__main__':
    main()
