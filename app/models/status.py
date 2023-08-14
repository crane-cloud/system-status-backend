import os
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from app.models import db
from app.models.root_model import RootModel

class Status(RootModel):
    __tablename__ = 'status'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   server_default=sa_text("uuid_generate_v4()"))
    name = db.Column(db.String, nullable=False, unique=True)
    parent_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self,  name, parent_name, status, description = ''):
        """ initialize with email, username and password """
        self.name = name
        self.parent_name = parent_name
        self.status = status
        self.description = description
