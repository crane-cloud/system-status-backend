from flask_restful import Api
from app.controllers import (IndexView, SystemStatusView)


api = Api()

# Index route
api.add_resource(IndexView, '/')

api.add_resource(SystemStatusView, '/api/v1/statuses')
