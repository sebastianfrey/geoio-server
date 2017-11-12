from flask import Flask
from flask_restful import Api

import server.resources as Resources

APP = Flask(__name__)
API = Api(APP)


API.add_resource(Resources.Services, '/')
API.add_resource(Resources.ConvexHull, '/convexHull')

if __name__ == '__main__':
    APP.run(debug=True)
