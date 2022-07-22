
import mysql.connector as mysql_conn
import psycopg2
import os
from types import SimpleNamespace


class DatabaseService:

    def __init__(self):
        self.Error = None

    def create_connection(self):
        """ Create a connection to db server """
        pass

    def create_db_connection(self, user=None, password=None, db_name=None):
        """ Create a connection to a single database """
        pass

    def check_user_db_rights(self, user=None, password=None, db_name=None):
        """Verify user rights to db"""

    # Create or check user exists database
    def create_database(self, db_name=None, user=None, password=None):
        """Create a database with user details"""
        pass

    def check_db_connection(self):
        """Validates if one is able to connect to Database server returns True or False"""
        pass


class MysqlDbService(DatabaseService):
    def __init__(self):
        super(DatabaseService, self).__init__()
        self.Error = mysql_conn.Error

    def create_connection(self):
        try:
            super_connection = mysql_conn.connect(
                host=os.getenv('ADMIN_MYSQL_HOST'),
                user=os.getenv('ADMIN_MYSQL_USER'),
                password=os.getenv('ADMIN_MYSQL_PASSWORD'),
                port=os.getenv('ADMIN_MYSQL_PORT', '')
            )
            return super_connection
        except self.Error as e:
            print(e)
            return False

    def create_db_connection(self, user=None, password=None, db_name=None):
        try:
            user_connection = mysql_conn.connect(
                host=os.getenv('ADMIN_MYSQL_HOST'),
                user=user,
                password=password,
                port=os.getenv('ADMIN_MYSQL_PORT', ''),
                database=db_name
            )
            return user_connection
        except self.Error as e:
            print(e)
            return False

    def check_db_connection(self):
        try:
            super_connection = self.create_connection()
            if not super_connection:
                return False
            return True
        except self.Error as e:
            return False
        finally:
            if not super_connection:
                return False
            if (super_connection.is_connected()):
                super_connection.close()

    def get_server_status(self):
        try:
            connection = self.cSreate_connection()
            if not connection:
                return False
            cursor = connection.cursor()
            cursor.execute("SHOW GLOBAL STATUS")
            # cursor.fetchall()
            return {
                'status': 'success',
                'data': 'online'
            }
        except self.Error:
            return {
                'status': 'error',
                'message': 'Error has occured'}

        finally:
            if not connection:
                return {
                    'status': 'error',
                    'message': 'Unable to connect to database'}
            if (connection.is_connected()):
                cursor.close()
                connection.close()


class PostgresqlDbService(DatabaseService):

    def __init__(self):
        super(DatabaseService, self).__init__()
        self.Error = psycopg2.Error

    def create_connection(self):
        try:
            super_connection = psycopg2.connect(
                host=os.getenv('ADMIN_PSQL_HOST'),
                user=os.getenv('ADMIN_PSQL_USER'),
                password=os.getenv('ADMIN_PSQL_PASSWORD'),
                port=os.getenv('ADMIN_PSQL_PORT', '')
            )
            super_connection.autocommit = True
            return super_connection
        except self.Error as e:
            print(e)
            return False

    def check_db_connection(self):
        try:
            super_connection = self.create_connection()
            if not super_connection:
                return False
            return True
        except self.Error as e:
            return False
        finally:
            if not super_connection:
                return False
            super_connection.close()

    def create_db_connection(self, user=None, password=None, db_name=None):
        try:
            user_connection = psycopg2.connect(
                host=os.getenv('ADMIN_PSQL_HOST'),
                user=user,
                password=password,
                port=os.getenv('ADMIN_PSQL_PORT', ''),
                database=db_name
            )
            return user_connection
        except self.Error as e:
            print(e)
            return False

    def get_server_status(self):
        try:
            connection = self.create_connection()
            if not connection:
                return False
            cursor = connection.cursor()
            cursor.execute("SELECT pg_is_in_recovery()")

            for db in cursor:
                if db[0]:
                    return {
                        'status': 'failed',
                        'message': 'in recovery'}
                else:
                    return {
                        'status': 'success',
                        'message': 'online'}
        except self.Error:
            return {
                'status': 'error',
                'message': 'Error has occured'}
        finally:
            if not connection:
                return {
                    'status': 'error',
                    'message': 'Unable to connect to database'}

            cursor.close()
            connection.close()
