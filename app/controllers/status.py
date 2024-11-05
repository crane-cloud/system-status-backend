
import os
from flask_restful import Resource
from app.helpers.status import get_client_status_infor, get_cluster_status_info, get_database_status_infor, get_prometheus_status_info
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
import json
from datetime import datetime
from app.models.cluster import Cluster
from app.models.status import Status
from app.schemas.status import StatusSchema
from app.helpers.cache_helper import cache
from app.models import db
from sqlalchemy import func


class SystemStatusView(Resource):
    @cache.cached()
    def get(self):
        try:
            app_status = cache.get('app_status')
        except Exception:
            return dict(status='fail', message='Unable to reach the redis db'), 500

        # return app_status
        if app_status:
            return dict(status='success', data=app_status), 200

        # get cranecloud status
        front_end_url = os.getenv('CLIENT_BASE_URL', None)
        backend_end_url = os.getenv('BACKEND_BASE_URL', None)
        apps_list = [
            {'name': 'cranecloud-frontend', 'url': front_end_url},
            {'name': 'cranecloud-backend', 'url': backend_end_url},
        ]
        cranecloud_status = get_client_status_infor(apps_list)

        # get clusters status
        clusters = Cluster.find_all()
        clusters_status = None
        prometheus_status = None
        if clusters:
            clusters_status = get_cluster_status_info(clusters)
            prometheus_status = get_prometheus_status_info(clusters)

        # get database status
        database_status = get_database_status_infor()

        # get MIRA status
        mira_apps_list = [
            {'name': 'mira-frontend',
             'url': os.getenv('MIRA_FRONTEND_URL', None)},
            {'name': 'mira-backend',
             'url': os.getenv('MIRA_BACKEND_URL', None)},
        ]
        mira_status = get_client_status_infor(mira_apps_list)

        # get Registry status
        habor_app = [
            {'name': 'habor-registry',
             'url': os.getenv('REGISTRY_URL', None)},
        ]
        registry_status = get_client_status_infor(habor_app)
        status_data = {
            'cranecloud_status': cranecloud_status,
            'clusters_status': clusters_status,
            'prometheus_status': prometheus_status,
            'database_status': database_status,
            'mira_status': mira_status,
            'registry': registry_status
        }
        cache.set('app_status', status_data)

        return dict(status='success', data=status_data), 200


class SystemStatusSeriesView(Resource):
    def post(self):
        # get cranecloud status
        front_end_url = os.getenv('CLIENT_BASE_URL', None)
        backend_end_url = os.getenv('BACKEND_BASE_URL', None)
        apps_list = [
            {'name': 'cranecloud-frontend', 'url': front_end_url},
            {'name': 'cranecloud-backend', 'url': backend_end_url},
        ]
        cranecloud_status = get_client_status_infor(apps_list)

        # get clusters status
        clusters = Cluster.find_all()
        clusters_status = None
        prometheus_status = None
        if clusters:
            clusters_status = get_cluster_status_info(clusters)
            prometheus_status = get_prometheus_status_info(clusters)

        # get database status
        database_status = get_database_status_infor()

        # get MIRA status
        mira_apps_list = [
            {'name': 'mira-frontend',
             'url': os.getenv('MIRA_FRONTEND_URL', None)},
            {'name': 'mira-backend',
             'url': os.getenv('MIRA_BACKEND_URL', None)},
        ]
        mira_status = get_client_status_infor(mira_apps_list)

        # get Registry status
        habor_app = [
            {'name': 'habor-registry',
             'url': os.getenv('REGISTRY_URL', None)},
        ]
        registry_status = get_client_status_infor(habor_app)

        # Cranecloud status
        for item in cranecloud_status["data"]:
            name = item["app_name"]
            app_status = item["status"]
            description = item.get("data", {}).get("message", None)
            app_url = item['app_url']

            status_entry = Status(
                name=name,
                parent_name="cranecloud_status",
                status=app_status,
                description=json.dumps(description),
                url=app_url
            )
            db.session.add(status_entry)
        try:
            # Database_status
            
            for item in database_status["data"]:
                name = item["database_name"]
                app_status = item["status"]
                description = item.get("data", {}).get("message", None)
                status_entry = Status(
                    name=name,
                    parent_name="database_status",
                    status=app_status,
                    description=json.dumps(description)
                )
                db.session.add(status_entry)

            # Prometheus_status
            if prometheus_status:
                for item in prometheus_status["data"]:
                    name = item["cluster_name"]
                    app_status = item["status"]
                    description = item["prometheus_status"]

                    prometheus_status_entry = Status(
                        name=name,
                        parent_name="prometheus_status",
                        status=app_status,
                        description=json.dumps(description)
                    )
                    db.session.add(prometheus_status_entry)

            # clusters_status
            if clusters_status:
                for item in clusters_status["data"]:
                    name = item["cluster_name"]
                    app_status = item["status"]
                    description = item["cluster_status"]

                    cluster_status_entry = Status(
                        name=name,
                        parent_name="cluster_status",
                        status=app_status,
                        description=json.dumps(description)
                    )
                    db.session.add(cluster_status_entry)

            # Mira_status
            for item in mira_status["data"]:
                name = item["app_name"]
                app_status = item["status"]
                description = item["data"]
                app_url = item['app_url']

                mira_status_entry = Status(
                    name=name,
                    parent_name="mira_status",
                    status=app_status,
                    description=json.dumps(description),
                    url=app_url
                )
                db.session.add(mira_status_entry)

            # Registry_status
            for item in registry_status["data"]:
                name = item["app_name"]
                app_status = item["status"]
                app_url = item['app_url']

                description = item["data"]

                registry_status_entry = Status(
                    name=name,
                    parent_name="registry_status",
                    status=app_status,
                    description=json.dumps(description),
                    url=app_url
                )
                db.session.add(registry_status_entry)

            db.session.commit()

            status_data = {
                'cranecloud_status': cranecloud_status,
                'clusters_status': clusters_status,
                'prometheus_status': prometheus_status,
                'database_status': database_status,
                'mira_status': mira_status,
                'registry': registry_status
            }

            return dict(status='success', data=status_data), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return dict(status='fail', message=f'Internal Server Error'), 500

    def get(self):
        status_schema = StatusSchema(many=True)
        series = bool(request.args.get('series', False))
        series_type = request.args.get('type')
        start = request.args.get('start', None)
        end = request.args.get('end', None)

        query = Status.query
        if series_type:
            statuses = query.filter(Status.name.like(
                f'%{series_type}%') | Status.parent_name.like(f'%{series_type}%'))

        if start:
            start_datetime = datetime.fromtimestamp(int(float(start)))
            query = query.filter(
                Status.date_created >= start_datetime)

        if end:
            end_datetime = datetime.fromtimestamp(int(float(end)))
            query = query.filter(
                Status.date_created <= end_datetime)

        statuses = query.all()

        validated_status_data, errors = status_schema.dumps(statuses)

        clusters_data_list = json.loads(validated_status_data)

        if errors:
            return dict(status='fail', message=errors,
                        data=dict(statuses=clusters_data_list)), 409

        if series:
            # Prepare series data for graphing
            graph_data = []
            for entry in clusters_data_list:
                graph_data.append({
                    'timestamp': datetime.strptime(entry['date_created'], "%Y-%m-%dT%H:%M:%S.%f").timestamp(),
                    'name': entry['name'],
                    'parent_name': entry['parent_name'],
                    'status': entry['status']
                })

            return dict(status='Success', data=dict(graph_data=graph_data)), 200

        return dict(status='Success',
                    data=dict(statuses=clusters_data_list)), 200

class SystemStatusUptime(Resource):
    def get(self):

        resource_name = request.args.get('resource_name')

        if not resource_name:
            return dict(status='fail', message=f"Please send a resource name",
                        data=None), 400
    
        total_count = Status.query.filter_by(name=resource_name).count()
        
        success_count = Status.query.filter_by(name=resource_name, status='success').count()
        
        # If there are no records, return a specific message, prevent division by 0
        if total_count == 0:
            return dict(status='fail', message=f"No records found for resource '{resource_name}'",
                        data=None), 404
        
        # Calculate uptime percentage
        uptime_percentage = (success_count / total_count) * 100 if total_count else 0

        
        up_time={
            "resource_name": resource_name,
            "uptime_percentage": round(uptime_percentage, 2)
        }
        return dict(status='Success',
                    data=dict(uptime=up_time)), 200