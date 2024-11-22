from flask_restful import Api
from app.controllers import (
    IndexView, SystemStatusView, SystemStatusSeriesView, ClusterView, ClusterDetailView, SystemStatusUptime)


api = Api()

# Index route
api.add_resource(IndexView, '/')

api.add_resource(SystemStatusView, '/api/v1/statuses')
api.add_resource(SystemStatusSeriesView, '/api/v1/statuses/series')
api.add_resource(SystemStatusUptime, '/api/v1/uptime')

# clusters routes
api.add_resource(ClusterView, '/api/v1/clusters')
api.add_resource(ClusterDetailView, '/api/v1/clusters/<cluster_id>')
