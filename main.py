from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors

import server.resources as Resources

APP = Flask(__name__)
API = Api(APP)

API.decorators = [cors.crossdomain(origin='*', headers=['accept', 'Content-Type'])] 


API.add_resource(Resources.Services, '/')
API.add_resource(Resources.ConvexHull, '/convexHull')

if __name__ == '__main__':
    APP.run(debug=True)
