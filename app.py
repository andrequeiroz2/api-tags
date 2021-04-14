import os
from flask import Flask
from tags import database
from tags.api.tags.tags_route import init_tags_api
from flask_restful import Api


def create_app():
    app = Flask(__name__)

   
    app.config['SECRET_KEY'] = 'todo-api/api-tags:1.0'

    app.config['MONGODB_SETTINGS'] = {
         'db': 'tags',
         'host': 'mongodb://admin:passwordD21@mongodbtags:27017/tags?authSource=admin',
         
     }
    
    database.init_app(app)
    
    api = Api(app)
    init_tags_api(api)

    return app
