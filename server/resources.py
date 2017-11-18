import json
import sys

from flask import request
from flask_restful import reqparse, Resource
from server.algorithms import convex_hull

SERVICES = {'error': 'failed to load'}

with open('services.json') as services_json:
    SERVICES = json.load(services_json)

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('')

def abort(message, code=500):
    return {'error': message, 'code': code}

class Services(Resource):
    """Resource for server information"""
    def get(self):
        """Returns the server information"""
        return SERVICES

class ConvexHull(Resource):
    """Resource for handling convex hull"""
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('collection', type=dict, location='json', required=True)
        super(ConvexHull, self).__init__()

    def post(self):
        """The convex hull handler"""
        args = self.reqparse.parse_args()
        try:
            return convex_hull(args.collection)
        except Exception as error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                'filename': exc_traceback.tb_frame.f_code.co_filename,
                'lineno'  : exc_traceback.tb_lineno,
                'name'    : exc_traceback.tb_frame.f_code.co_name,
                'message' : error
            }

            return abort(str(traceback_details))
