import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

import pymongo

mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
mongodb_database = mongodb_client[os.getenv("MONGODB_DATABASE_NAME")]
mongodb_collection = mongodb_database[os.getenv("MONGODB_COLLECTION_NAME")]

app = Flask(__name__)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name = name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

        inoput_document = {
            "input": name
        }
        mongodb_collection.insert_one(input_document)

if __name__ == '__main__':
    app.run()
