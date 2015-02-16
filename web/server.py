from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

import json
import urllib2


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGO_DBNAME'] = "mainAPP"

#connection = MongoClient('localhost', 27017)
connection = MongoClient(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

@app.route('/', methods=['GET'])
def index():
    db = connection['mainAPP']
    collection = db.urls
    urls = collection.find()
    existing_urls = []

    for url in urls:
        usr = {'url': str(url['url'])}
        existing_urls.append(usr)

    return render_template("index.html", existing=json.dumps(existing_urls))

@app.route('/add_url', methods=['GET', 'POST'])
def add_url():
    req_data = json.loads(request.data)
    db = connection['mainAPP']
    collection = db.urls
    DBurl = collection.find_one({'url': req_data['url']})
    url = req_data['url']
    # check  what offer the user clicked and if he used it before

    if request.method == 'POST':
        try:
            response = urllib2.urlopen(url)

            if (DBurl and DBurl["url"]==response.url):
                app.logger.debug(DBurl['offer'])
                return "invalidUrl"
            else:
                req_data['url'] = response.url
                collection.insert(req_data)
                return "inserted"

        except Exception as e:
            app.logger.debug(e)
            return "invalidUrl"

if __name__ == '__main__':
    #remove debug=True for production!
    app.run(host='0.0.0.0', port=8080, debug=True)
