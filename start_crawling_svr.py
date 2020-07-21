import os
from flask import Flask, render_template, jsonify
from flask_restful import Api

from Controllers.RestController import RestController

CRAWLING_SVR_PORT = 20000

app = Flask(__name__)
api = Api(app)
api.add_resource(RestController, '/rest/<string:service_name>')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=CRAWLING_SVR_PORT , debug=True)
