from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

import json


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
        usr = {'name': str(url['name']),
               'url': str(url['url'])}
        existing_urls.append(usr)

    return render_template("index.html", existing=json.dumps(existing_urls))

if __name__ == '__main__':
    #remove debug=True for production!
    app.run(host='0.0.0.0', port=8080, debug=True)
