from flask_migrate import Migrate
from app.models import db
from server import app
from flask.cli import FlaskGroup

# import models


# register app and db with migration class
cli = FlaskGroup(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)

# cli.add_command('db', MigrateCommand)

if __name__ == '__main__':
    cli()
