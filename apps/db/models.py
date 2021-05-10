import uuid

import sqlalchemy as sa

from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base

# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

from app import db

Base = declarative_base()
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


class Uploads(db.Model):
    __tablename__ = 'uploads'

    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    status = db.Column(db.String())
    task_id = sa.Column(db.Integer())


class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(UUIDType, db.ForeignKey("uploads.id", ondelete="restrict"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    latitude = db.Column(sa.String(), nullable=False)
    longitude = db.Column(sa.String(), nullable=False)
    address = db.Column(sa.String())
