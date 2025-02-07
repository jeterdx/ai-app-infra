import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

import pymongo
from openai import AzureOpenAI


mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
mongodb_database = mongodb_client[os.getenv("MONGODB_DATABASE_NAME")]
mongodb_collection = mongodb_database[os.getenv("MONGODB_COLLECTION_NAME")]

azure_openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

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

        generated_description = call_aoai(name)
        insert_user_and_response_to_db(name, generated_description)

        return render_template('hello.html', name = name, generated_description = generated_description)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

def call_aoai(name):
    response = azure_openai_client.chat.completions.create(
        model=os.getenv("   "),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Write a 10 words explanation about {name}."},
        ]
    )
    generated_description = response.choices[0].message.content
    return generated_description

def insert_user_and_response_to_db(name, generated_description):
    input_document = {
        name: generated_description
    }
    mongodb_collection.insert_one(input_document)

if __name__ == '__main__':
    app.run()
