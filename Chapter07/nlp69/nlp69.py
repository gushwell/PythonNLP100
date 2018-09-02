import pymongo
from flask import Flask, render_template, request

class SearchInfo:
    def __init__(self, name, area, tag):
        self.name = name
        self.area = area
        self.tag = tag

class Searcher:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['MusicBrainzDb']
        self.co = self.db['artists']

    def search(self, info):
        query = { '$and' : [ ]}
        if info.name != '':
            cond = []
            cond.append({ 'aliases.name': info.name })
            cond.append({ 'name': info.name })
            query['$and'].append({ '$or': cond })
        if info.area != '':
            query['$and'].append({ 'area': info.area })
        if info.tag != '':
            query['$and'].append({ 'tags.value': info.tag })
        q2 = self.co.find(query).sort('rating.count', pymongo.DESCENDING)
        return list(q2)[:100]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searcher = Searcher()
        results = searcher.search(SearchInfo(request.form['name'], request.form['area'], request.form['tag']))
        return render_template('result.html', artists=results) 
    else:
        return render_template('search.html') 

if __name__ == "__main__":
    app.run(debug=True)