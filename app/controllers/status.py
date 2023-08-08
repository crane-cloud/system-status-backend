
import os
from flask_restful import Resource
from app.helpers.status import get_client_status_infor, get_cluster_status_info, get_database_status_infor, get_prometheus_status_info
from flask import request
from app.models.cluster import Cluster


class SystemStatusView(Resource):

    def get(self):
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

        return dict(status='success', data={
            'cranecloud_status': cranecloud_status,
            'clusters_status': clusters_status,
            'prometheus_status': prometheus_status,
            'database_status': database_status,
            'mira_status': mira_status,
            'registry': registry_status
        }), 200
